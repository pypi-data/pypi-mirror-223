import pandas as pd
from shapely.geometry import Polygon
import numpy as np
import os

import download_files
from .filter_utils_summary import filter_location, filter_datetime

pd.options.mode.chained_assignment = None  # default='warn'


def generate_databases(location_filter, database_location, download_databases, summary=False):
    if download_databases:
        download_files.download_databases(database_location)
    if not os.path.exists(os.path.join(database_location, 'summary')):
        os.makedirs(os.path.join(database_location, 'summary'))
    surveys, locations = generate_survey_database(location_filter, database_location, summary)
    detections = generate_detections_database(location_filter, surveys, database_location, summary)
    airdata = generate_airdata_database(location_filter, surveys, database_location, summary)
    kmls = generate_kml_database(location_filter, surveys, detections, database_location, summary)
    return surveys, locations, detections, airdata, kmls


def generate_survey_database(location_filter, database_location, summary):
    """
    This method filters the survey database to select rows only relevant to the selected survey location.
    """
    survey_match = pd.read_csv(os.path.join(database_location, 'original', 'survey_match.csv'))

    # Filter dates before 28 June 2022
    columns_to_search = ['survey_start', 'flight_date']
    survey_match = filter_datetime(survey_match, columns_to_search)

    # Extract entries that match the location filter
    columns_to_search = ['KML', 'kml_det_matches', 'mission', 'location', 'location_id']
    filtered_df = filter_location(location_filter, columns_to_search, survey_match)

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
        'location_area': filtered_df['location_area']
    })
    if summary:
        surveys.to_csv(os.path.join(database_location, 'surveys-pre.csv'), index=False)
    surveys, locations = add_location_dataframe(surveys, database_location, summary)
    surveys = add_survey_sites(surveys)
    if summary:
        surveys.to_csv(os.path.join(database_location, 'summary', 'surveys.csv'), index=False)
    else:
        surveys.to_csv(os.path.join(database_location, 'surveys.csv'), index=False)
    return surveys, locations


def add_location_dataframe(surveys, database_location, summary):
    # Integrate the area variable from the locations database
    location_dataframe = pd.read_csv(os.path.join(database_location, 'original', 'location_dataframe.csv'))
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
    if summary:
        locations.to_csv(os.path.join(database_location, 'summary', 'locations.csv'), index=False)
    else:
        locations.to_csv(os.path.join(database_location, 'locations.csv'), index=False)
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


def generate_detections_database(location_filter, surveys, database_location, summary):
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
    det_match = pd.read_csv(os.path.join(database_location, 'original', 'det_match.csv'))
    det_match = det_match.drop_duplicates()

    # Filter dates before 28 June 2022
    columns_to_search = ['detection_time']
    det_match = filter_datetime(det_match, columns_to_search)

    columns_to_search = ['KML', 'kml_matches', 'mission', 'location', 'location_id']
    filtered_df = filter_location(location_filter, columns_to_search, det_match)

    survey_location_ids = surveys['location_id'].drop_duplicates().tolist()
    column_mask = det_match['location_id'].isin(survey_location_ids)
    concatenated_df = pd.concat([filtered_df] + [det_match[column_mask]])
    filtered_df = concatenated_df.drop_duplicates()

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
    if summary:
        detections.to_csv(os.path.join(database_location, 'summary', 'detections.csv'), index=False)
    else:
        detections.to_csv(os.path.join(database_location, 'detections.csv'), index=False)
    return detections


def generate_airdata_database(location_filter, surveys, database_location, summary):
    airdata_matches = pd.read_csv(os.path.join(database_location, 'original', 'airdata_matches.csv'))

    # Filter dates before 28 June 2022
    columns_to_search = ['flight_start', 'start_time', 'finish_time']
    airdata_matches = filter_datetime(airdata_matches, columns_to_search)

    columns_to_search = ['kml_matches', 'surveyID', 'survey_location_id', 'kml_location']
    filtered_df = filter_location(location_filter, columns_to_search, airdata_matches)

    ids_to_filter = ['survey_location_id', 'kml_location_id']
    survey_location_ids = surveys['location_id'].drop_duplicates().tolist()
    for column in ids_to_filter:
        column_mask = airdata_matches[column].isin(survey_location_ids)
        concatenated_df = pd.concat([filtered_df, airdata_matches[column_mask]])
        filtered_df = concatenated_df.drop_duplicates()

    airdata = pd.DataFrame({
        'flight_start': filtered_df['flight_start'],
        'pilot': filtered_df['pilot'],
        'drone': filtered_df['drone'],
        'drone_type': filtered_df['drone_type'],
        'Ground Weather Summary': filtered_df['Ground Weather Summary'],
        'Ground Temperature (c)': filtered_df['Ground Temperature (c)'],
        'Ground Visibility (Kilometers)': filtered_df['Ground Visibility (Kilometers)'],
        'Ground Wind Speed': filtered_df['Ground Wind Speed'],
        'Ground Wind Direction': filtered_df['Ground Wind Direction'],
        'Cloud Cover': filtered_df['Cloud Cover'],
        'Avg Wind': filtered_df['Avg Wind']
    })
    if summary:
        airdata.to_csv(os.path.join(database_location, 'summary', 'airdata.csv'), index=False)
    else:
        airdata.to_csv(os.path.join(database_location, 'airdata.csv'), index=False)
    return airdata


def generate_kml_database(location_filter, surveys, detections, database_location, summary):
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
    kml_gdf = pd.read_csv(os.path.join(database_location, 'original', 'kml_gdf.csv'))

    columns_to_search = ['filename', 'location_id', 'mission', 'location']
    filtered_df = filter_location(location_filter, columns_to_search, kml_gdf)

    # Cross reference the other location_id's
    survey_location_ids = surveys['location_id'].drop_duplicates().tolist()
    detection_location_ids = detections['location_id'].drop_duplicates().tolist()
    # Creates a list of all combined location ids removing duplicates
    location_ids = list(set(survey_location_ids) | set(detection_location_ids))
    column_mask = kml_gdf['location_id'].isin(location_ids)
    concatenated_df = pd.concat([filtered_df, kml_gdf[column_mask]])
    filtered_df = concatenated_df.drop_duplicates()

    kmls = pd.DataFrame({
        'linestring': filtered_df['geometry'],
        'polygon': filtered_df['boxes'],
        'area': filtered_df['true_area'],
        'length': filtered_df['true_length']
    })
    if summary:
        kmls.to_csv(os.path.join(database_location, 'summary', 'kmls.csv'), index=False)
    else:
        kmls.to_csv(os.path.join(database_location, 'kmls.csv'), index=False)
    return kmls


if __name__ == '__main__':
    all_location_filters = ['willi', 'jellore', 'meryla', 'belanglo', 'olney', 'kuluwan', 'warrawolong', 'koreelah',
                            'corrabare', 'barrington', 'watagan', 'comleroy', 'lindesay', 'koreelah', 'donaldson',
                            'unumgar', 'bar', 'crescent', 'stockrington']

    # generate_databases(location_filter=all_location_filters, database_location='databases', download_databases=False,
    #                    summary=True)
    generate_databases(location_filter='bar', database_location='databases', download_databases=False,
                       summary=False)
