import os

import pandas as pd
import geopandas as gpd
import matplotlib.lines as mlines
from shapely.geometry import Point
from shapely.wkt import loads
import contextily as cx
import matplotlib.pyplot as plt
import numpy as np


def generate_figure(kmls, detections, filename, bbox=None, image=None, path_colour='magenta', alpha=0.5):
    """
    Generate a figure with flight paths and detections, and save it to a file. If no PIL.image is provided as a
    basemap, the method will add a geographic basemap from OpenStreetMap. If a PIL.image is provided, this will be
    used as the basemap.

    Args:
        kmls (DataFrame): DataFrame of KML flight paths.
        detections (DataFrame): DataFrame of detections.
        bbox (tuple): a tuple with 4 elements in the order (x_min, y_min, x_max, y_max) containing the
			coordinates for the area you want to extract from the map
        image (PIL.Image or None): Base map image. If None, a basemap will be added.
        filename (str): Name of the file to save the figure to.
    """
    # Switch to the 'Agg' backend
    plt.switch_backend('agg')

    # Create a new figure with a larger size
    fig, ax = plt.subplots(figsize=(12, 12))

    # Prepare an empty list for custom legend handles
    custom_handles = []

    # Overlay the flight paths and detections
    line_path = plot_flight_path(kmls, ax, path_colour=path_colour, alpha=alpha)
    custom_handles.append(line_path)

    detection_handles = plot_detections(detections, ax)
    custom_handles.extend(detection_handles)

    if image is not None:
        # Convert the PIL image to a NumPy array and display the image
        img = np.array(image)
        ax.imshow(img, extent=[bbox[0], bbox[2], bbox[1], bbox[3]])

    else:

        # Add terrain to map
        cx.add_basemap(ax, crs='EPSG:4326', source=cx.providers.OpenStreetMap.Mapnik)

    # Add the legend
    add_legend(ax, custom_handles)

    # Save the figure
    if not os.path.exists('figures'):
        # Create a new directory because it does not exist
        os.makedirs('figures')
    plt.savefig(os.path.join('figures', filename), dpi=600, bbox_inches='tight')

    # Switch back to the default backend
    plt.switch_backend('module://ipykernel.pylab.backend_inline')


def plot_flight_path(kmls, ax, path_colour='c', alpha=1.0):
    # Plots the kml flightpath on the figure
    if isinstance(kmls['linestring'].iloc[0], str):
        kmls['linestring'] = kmls['linestring'].apply(loads)
    line_gdf = gpd.GeoDataFrame(kmls, geometry='linestring', crs='EPSG:3308')
    line_gdf = line_gdf.to_crs(epsg='4326')
    line_gdf.plot(ax=ax, color=path_colour, zorder=1, alpha=alpha)
    line_patch = mlines.Line2D([], [], color=path_colour, markersize=10, linestyle='-',
                               label='Drone Survey Flight Plan', alpha=alpha)
    return line_patch


def plot_detections(detections, ax):
    if 'points' not in detections.columns:
        detections['points'] = detections.apply(lambda row: Point(row['lon'], row['lat']), axis=1)

    # Separates the detections databse into 3 sections and plots them in different colours
    confirmed_koala_detections = detections[(detections['species_name'] == 'Koala') &
                                            (detections['gt_outcome'] == 'confirmed')]
    koala_detections = detections[(detections['species_name'] == 'Koala') &
                                  (detections['gt_outcome'] != 'confirmed')]
    animal_detections = detections[detections['species_name'] != 'Koala']
    confirmed_koala_detections_gdf = gpd.GeoDataFrame(confirmed_koala_detections, geometry='points')
    koala_detections_gdf = gpd.GeoDataFrame(koala_detections, geometry='points')
    animal_detections_gdf = gpd.GeoDataFrame(animal_detections, geometry='points')
    # Get the area of the plot for scaling factor
    plot_area = ax.get_xlim()[1] - ax.get_xlim()[0]
    scaling_size = 2 / plot_area

    # Add checks here to plot only if there are any detections.
    if not animal_detections_gdf.empty:
        animal_detections_gdf.plot(ax=ax, color='black', markersize=scaling_size, zorder=2)

    if not koala_detections_gdf.empty:
        koala_detections_gdf.plot(ax=ax, color='yellow', markersize=scaling_size, zorder=3)

    if not confirmed_koala_detections_gdf.empty:
        confirmed_koala_detections_gdf.plot(ax=ax, color='red', markersize=scaling_size, zorder=4)

    # Create handles for legend
    animal_line = mlines.Line2D([], [], color='black', marker='o', markersize=10, linestyle='None',
                                label='Animal Detection')
    koala_line = mlines.Line2D([], [], color='yellow', marker='o', markersize=10, linestyle='None',
                               label='Koala Detection')
    confirmed_koala_line = mlines.Line2D([], [], color='red', marker='o', markersize=10, linestyle='None',
                                         label='Confirmed Koala Detection')

    custom_handles = [animal_line, koala_line, confirmed_koala_line]
    return custom_handles


def get_bounding_box(kmls, detections):
    """
    This method takes the flight path database and the detections database and measures the coordinates of the
    bounding box that covers the survey area for mapping

    Args:
        kmls (Pandas Dataframe): Filtered kml database for survey site of interest
        detections (Pandas Dataframe): Filtered detections database for survey site of interest

    Returns:
         A tuple containing minx, miny, maxx, maxy values for the bounds of the series as a whole
    """
    # Convert KMLs to GeoDataFrame
    if isinstance(kmls['linestring'].iloc[0], str):
        kmls['linestring'] = kmls['linestring'].apply(lambda x: loads(x))
    kmls_gdf = gpd.GeoDataFrame(kmls, geometry='linestring', crs='EPSG:3308')
    kmls_gdf = kmls_gdf.to_crs(epsg='4326')

    # Convert detections to GeoDataFrame
    if 'points' not in detections.columns:
        detections['points'] = detections.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
    detections_gdf = gpd.GeoDataFrame(detections, geometry='points')

    # Combine the GeoDataFrames
    combined_gdf = gpd.GeoSeries(pd.concat([kmls_gdf.geometry, detections_gdf.geometry]))

    # Find the bounding box
    bbox = combined_gdf.total_bounds
    return bbox


def add_legend(ax, custom_handles):
    # Set the legend outside the plot in the 'lower left' position
    legend = plt.legend(loc='upper left', fontsize='large', bbox_to_anchor=(0, -0.04), borderaxespad=0,
                        handles=custom_handles)

    # Customize the appearance of the legend
    legend.get_frame().set_facecolor('white')    # Set the background color to white
    legend.get_frame().set_edgecolor('black')    # Set the border color to black
    legend.get_frame().set_linewidth(1.0)        # Set the border linewidth

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Remove the default axes
    ax.set_axis_off()
    return ax


if __name__ == '__main__':
    kmls = pd.read_csv('databases/kmls.csv')
    detections = pd.read_csv('databases/detections.csv')
    generate_figure(kmls, detections, 'map.png')
