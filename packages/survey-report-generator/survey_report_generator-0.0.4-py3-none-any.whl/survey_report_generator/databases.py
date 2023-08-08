import pandas as pd
from shapely.geometry import Polygon
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy", message=".*Intel MKL WARNING.*")
import numpy as np
import os

from .filter_utils import filter_location, filter_datetime

pd.options.mode.chained_assignment = None  # default='warn'


def generate_survey_database(report):
    """
    This method filters the survey database to select rows only relevant to the selected survey location.
    """
    survey_match = pd.read_csv(os.path.join(report.database_location, 'original', 'survey_match.csv'))

    # Filter dates before 28 June 2022
    columns_to_search = ['survey_start', 'flight_date']
    survey_match = filter_datetime(survey_match, columns_to_search, report.start_date, report.end_date)

    # Extract entries that match the location filter
    columns_to_search = ['mission', 'location', 'location_id']
    if report.location_filter == 'Bar':
        columns_to_search = ['location_id']
    # columns_to_search = ['KML', 'kml_det_matches', 'mission', 'location', 'location_id']
    filtered_df = filter_location(report, columns_to_search, survey_match)

    # Filter out the relevant columns
    surveys = pd.DataFrame({
        'survey_start': filtered_df['survey_start'],
        'flight_date': filtered_df['flight_date'],
        'drone': filtered_df['drone'],
        'drone_height': filtered_df['drone_height'],
        'drone_speed': filtered_df['drone_speed'],
        'end_time': filtered_df['end_time'],
        'mission': filtered_df['mission'],
        'wind_speed': filtered_df['wind_speed'],
        'ground_temp': filtered_df['ground_temp'],
        'location': filtered_df['location'],
        'location_id': filtered_df['location_id'],
        'location_area': filtered_df['location_area'],
        'pilot': filtered_df['pilot']
    })
    surveys, locations = add_location_dataframe(surveys, report)
    surveys = add_survey_sites(surveys)
    return surveys, locations


def add_location_dataframe(surveys, report):
    # Integrate the area variable from the locations database
    location_dataframe = pd.read_csv(os.path.join(report.database_location, 'original', 'location_dataframe.csv'))
    locations = pd.DataFrame({
        'location_id': location_dataframe['location_id'],
        'area_nsew_box': location_dataframe['area_nsew_box'],
        'total_area': location_dataframe['total_area'], # area of the union of all plots (prevents double counting)
        'avg_area': location_dataframe['avg_area'], # average area of a kml
        'lat_min': location_dataframe['lat_min'],
        'lat_max': location_dataframe['lat_max'],
        'lon_min': location_dataframe['lon_min'],
        'lon_max': location_dataframe['lon_max']
    })
    survey_location_ids = surveys['location_id'].drop_duplicates().tolist()
    surveys = pd.merge(left=surveys, right=locations, on='location_id', validate='many_to_one')
    locations = locations[locations['location_id'].isin(survey_location_ids)]
    if surveys['total_area'].sum() == 0:
        raise Exception("The total area parameter is zero for all sites. This parameter is needed to create the "
                        "figures.")

    return surveys, locations


def add_survey_sites(surveys):
    survey_sites = []
    for idx, row in surveys.iterrows():
        valid_coordinates = (pd.notnull(row['lat_min']) and pd.notnull(row['lat_max']) and pd.notnull(row['lon_min'])
                             and pd.notnull(row['lon_max']))
        if valid_coordinates:
            coords = [
                (row['lon_min'], row['lat_min']),
                (row['lon_max'], row['lat_min']),
                (row['lon_max'], row['lat_max']),
                (row['lon_min'], row['lat_max'])
            ]
            survey_sites.append(Polygon(coords))
        else:
            survey_sites.append(np.nan)

    surveys['survey_sites'] = survey_sites
    return surveys.drop(columns=['lat_min', 'lat_max', 'lon_min', 'lon_max'])


def generate_detections_database(report):
    """
    This method filters the detections database to extract only relevant parameters and creates a second Pandas
    Dataframe which contains information about the target species.

    Args:
        location_filter (str/list): A keyword or code to filter the location by, for example, 'bongil', 'kalateenee' or
            'FR:KK64'. If regex is set to True you can also use regular expressions. Optionally, you can input a list
            containing multiple filters.
        surveys (Pandas Dataframe): The Dataframe exported from generate_surveys
        database_location (str): If the relevant databases are already downloaded, this specifies the path to the
            directory containing the databases
    """
    det_match = pd.read_csv(os.path.join(report.database_location, 'original', 'det_match.csv'))
    det_match = det_match.drop_duplicates()

    # Filter dates before 28 June 2022
    columns_to_search = ['detection_time']
    det_match = filter_datetime(det_match, columns_to_search, report.start_date, report.end_date)

    columns_to_search = ['mission', 'location', 'location_id']
    if report.location_filter == 'Bar':
        columns_to_search = ['location_id']
    # columns_to_search = ['KML', 'kml_matches', 'mission', 'location', 'location_id']
    filtered_df = filter_location(report, columns_to_search, det_match)

    # survey_location_ids = report.surveys['location_id'].drop_duplicates().tolist()
    # column_mask = det_match['location_id'].isin(survey_location_ids)
    # concatenated_df = pd.concat([filtered_df] + [det_match[column_mask]])
    # filtered_df = concatenated_df.drop_duplicates()

    # Extract the relevant columns
    filtered_df['detection_time'] = pd.to_datetime(filtered_df['detection_time'])
    filtered_df = filtered_df.sort_values('detection_time')
    filtered_df['date'] = pd.to_datetime(filtered_df['detection_time']).dt.date
    filtered_df['time'] = pd.to_datetime(filtered_df['detection_time']).dt.strftime("%-I:%M %p")
    detections = pd.DataFrame({
        'date': filtered_df['date'],
        'time': filtered_df['time'],
        'species_name': filtered_df['species_name'],
        'detection_count': filtered_df['detection_count'],
        'probability': filtered_df['probability'],
        'lat': filtered_df['drone_lat'],
        'lon': filtered_df['drone_lon'],
        'gt_outcome': filtered_df['gt_outcome'],
        'gt_method': filtered_df['gt_method'],
        'drone': filtered_df['drone'],
        'comments': filtered_df['comments'],
        'location': filtered_df['location'],
        'location_id': filtered_df['location_id']
    })
    return detections


def generate_airdata_database(report):
    airdata_matches = pd.read_csv(os.path.join(report.database_location, 'original', 'airdata_matches.csv'))

    # Filter dates before 28 June 2022
    columns_to_search = ['flight_start', 'start_time', 'finish_time']
    airdata_matches = filter_datetime(airdata_matches, columns_to_search, report.start_date, report.end_date)

    columns_to_search = ['kml_matches', 'surveyID', 'kml_location']
    filtered_df = filter_location(report, columns_to_search, airdata_matches)
    # filtered_df = pd.DataFrame()
    # ids_to_filter = ['survey_location_id', 'kml_location_id']
    # survey_location_ids = report.surveys['location_id'].drop_duplicates().tolist()
    # for column in ids_to_filter:
    #     column_mask = airdata_matches[column].isin(survey_location_ids)
    #     concatenated_df = pd.concat([filtered_df, airdata_matches[column_mask]])
    #     filtered_df = concatenated_df.drop_duplicates()

    airdata = pd.DataFrame({
        'flight_start': filtered_df['flight_start'],
        'start_time': filtered_df['start_time'],
        'finish_time': filtered_df['finish_time'],
        'pilot': filtered_df['pilot'],
        'drone': filtered_df['drone'],
        'drone_type': filtered_df['drone_type'],
        'survey_location_id': filtered_df['survey_location_id'],
        'kml_location_id': filtered_df['kml_location_id'],
        'kml_matches': filtered_df['kml_matches'],
        'surveyID': filtered_df['surveyID'],
        'kml_location': filtered_df['kml_location']
    })
    return airdata


# TODO: The kml databases are inaccurate because of the search methods. I don't actually use them in the project but
#  if I want to eventually, I would need to create them using location_ids rather than filter by name
def generate_kml_database(report):
    """
    This method filters the kml database to extract only high probability koalas (or another chosen animal
    filter) for the chosen survey location and selects only relevant columns for generating a report.

    Args:
        location_filter (str/list): A keyword or code to filter the location by, for example, 'bongil', 'kalateenee' or
            'FR:KK64'. If regex is set to True you can also use regular expressions. Optionally, you can input a list
            containing multiple filters.
        surveys (Pandas Dataframe): The Dataframe exported from generate_surveys
        detections (Pandas Dataframe): The Dataframe exported from generate_detections
        database_location (str): If the relevant databases are already downloaded, this specifies the path to the
            directory containing the databases
    """
    kml_gdf = pd.read_csv(os.path.join(report.database_location, 'original', 'kml_gdf.csv'))

    # columns_to_search = ['filename', 'location_id', 'mission', 'location']
    # filtered_df = filter_location(report, columns_to_search, kml_gdf)

    # Cross reference the other location_id's
    survey_location_ids = report.surveys['location_id'].drop_duplicates().tolist()
    detection_location_ids = report.detections['location_id'].drop_duplicates().tolist()
    # Creates a list of all combined location ids removing duplicates
    location_ids = list(set(survey_location_ids) | set(detection_location_ids))
    column_mask = kml_gdf['location_id'].isin(location_ids)
    filtered_df = kml_gdf[column_mask]

    kmls = pd.DataFrame({
        'filename': filtered_df['filename'],
        'linestring': filtered_df['geometry'],
        'polygon': filtered_df['boxes'],
        'area': filtered_df['true_area'],
        'length': filtered_df['true_length'],
        'location_id': filtered_df['location_id']
    })
    return kmls


# if __name__ == '__main__':

    # generate_databases(location_filter='bar', database_location='databases', download_databases=False,
    #                    summary=False)


    # generate_summary_databases(reports_list)