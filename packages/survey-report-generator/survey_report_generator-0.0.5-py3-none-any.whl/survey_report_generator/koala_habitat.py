from PIL import Image
from io import BytesIO
import requests
from matplotlib import pyplot as plt

from .figures_utils import get_bounding_box, generate_figure
import pandas as pd


def generate_koala_habitat_map(kmls, detections, file_name):
	bbox = get_bounding_box(kmls, detections)
	image = get_koala_habitat_map(bbox)
	generate_figure(kmls, detections, file_name, bbox, image)


def get_koala_habitat_map(bbox, size=(512, 512)):
	"""
	This method takes the bounding box coordinates of a survey area and returns a PIL Image of the NSW Koala Habitat
	Suitability Map at those coordinates.

	Args:
		bbox (tuple): a tuple with 4 elements in the order (x_min, y_min, x_max, y_max) containing the
			coordinates for the area you want to extract from the map
		size (tuple): a tuple with 2 elements in the order (width, height) specifying the size of the output image in pixels
	"""
	bounding_box = f'{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}'

	url = 'https://www.lmbc.nsw.gov.au/arcgis/rest/services/KoalaHabitat/KHSM_Koala_Habitat_Suitability/MapServer/export'
	params = {
		'bbox': bounding_box,
		'bboxSR': '4326',
		'imageSR': '4326',
		'size': f'{size[0]},{size[1]}',
		'layers': 'all:1,2,3,4,5,6,7',
		'timeRelation': 'esriTimeRelationOverlaps',
		'f': 'image'
	}

	response = requests.post(url, params=params)

	# Open the image using PIL
	image_bytes = response.content
	image = Image.open(BytesIO(image_bytes)).convert("RGBA")

	return image


def get_koala_habitat_info(lat, lon):
	"""
	This method takes the latitude and longitude coordinates and returns the information about the koala habitat
	at those coordinates.

	Args:
		lat (float): The latitude of the point of interest.
		lon (float): The longitude of the point of interest.
	"""

	url = 'https://www.lmbc.nsw.gov.au/arcgis/rest/services/KoalaHabitat/KHSM_Koala_Habitat_Suitability/MapServer/identify'
	params = {
		'geometry': f'{lon},{lat}',
		'geometryType': 'esriGeometryPoint',
		'sr': '4326',
		'layers': 'all:1,2,3,4,5,6,7',
		'tolerance': '0',
		'mapExtent': '0,0,0,0',
		'imageDisplay': '800,600,96',
		'returnGeometry': 'false',
		'f': 'json'
	}

	response = requests.post(url, params=params)
	json_response = response.json()

	# Normalize the JSON response into a dataframe
	df = pd.json_normalize(json_response['results'])

	# Drop rows where 'attributes.Class' is NaN
	df = df.dropna(subset=['attributes.Class value'])
	KHSM_df = pd.DataFrame({
		'KHSM_layerId': df['layerId'],
		'KHSM_class': df['attributes.Class value'],
		'KHSM_pixel_value': df['attributes.Pixel Value']
	})

	return KHSM_df


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

	# Create legend items for habitat layers
	habitat_colors = ['color1', 'color2', 'color3', 'color4', 'color5', 'color6', 'color7']
	habitat_labels = ['Label1', 'Label2', 'Label3', 'Label4', 'Label5', 'Label6', 'Label7']

	for color, label in zip(habitat_colors, habitat_labels):
		line = mlines.Line2D([], [], color=color, marker='o', markersize=10, linestyle='None', label=label)
		legend.legendHandles.append(line)

	# Remove the default axes
	ax.set_axis_off()
	return ax



if __name__ == '__main__':
	kmls = pd.read_csv('databases/kmls.csv')
	detections = pd.read_csv('databases/detections.csv')
	generate_koala_habitat_map(kmls, detections, 'koala-habitat-map.png')
