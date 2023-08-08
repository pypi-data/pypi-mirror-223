import os
from datetime import datetime

import pandas as pd


def filter_location(location_filter, columns_to_search, database):
    # Filter the database down using the location filter
    if isinstance(location_filter, str):
        location_filter = [location_filter]

    # These filters create issues when searching through KML filepaths
    no_kml_filters = ['bar', 'lindesay', 'donaldson', 'unumgar', 'koorelah']
    filters_avoid_kml = [element for element in location_filter if element in no_kml_filters]
    filters_for_kml = [element for element in location_filter if element not in no_kml_filters]

    columns_with_kml = [element for element in columns_to_search if 'kml' in element.lower()]
    columns_without_kml = [element for element in columns_to_search if 'kml' not in element.lower()]

    # Search for filters in each column
    filtered_df = pd.DataFrame()
    if len(filters_for_kml) != 0:
        for column in columns_with_kml:
            column_mask = pd.concat([database[column].str.contains(filter, case=False, na=False) for filter in
                                     filters_for_kml], axis=1).any(axis=1)
            concatenated_df = pd.concat([filtered_df, database[column_mask]])
            filtered_df = concatenated_df.drop_duplicates()

    if len(filters_avoid_kml) != 0:
        for column in columns_without_kml:
            column_mask = pd.concat([database[column].str.contains(filter, case=False, na=False) for filter in
                                     filters_avoid_kml], axis=1).any(axis=1)
            concatenated_df = pd.concat([filtered_df, database[column_mask]])
            filtered_df = concatenated_df.drop_duplicates()

    return filtered_df


def filter_datetime(database, columns_to_search):
    filtered_df = pd.DataFrame()
    # Remove entries after 28 June 2022
    date_string = '2022-06-28 09:30:00'
    format_string = '%Y-%m-%d %H:%M:%S'
    final_datetime = datetime.strptime(date_string, format_string)
    for column in columns_to_search:
        database[column] = pd.to_datetime(database[column])
        concatenated_df = pd.concat([filtered_df, database[database[column] < final_datetime]])
        filtered_df = concatenated_df.drop_duplicates()
    return filtered_df


def filter_species_names(database):
    species_to_keep = ['Wombat', 'Deer', 'Koala', 'Possum', 'Common Ringtail Possum', 'Glider',
                       'Common Brushtail Possum', 'Rabbit', 'Bandicoot', 'Glider', 'Pig', 'Sugar Glider', 'Microbat',
                       'Swamp Wallaby', 'Wallaby', 'Greater Glider', 'Yellow-bellied Glider', 'Bat', 'Flying-Fox',
                       'Rock Wallaby', 'Grey-headed Flying-Fox']
    return database[database['species_name'].isin(species_to_keep)]


def filter_target_species(detections, target_species, database_location):
    target_species_df = detections[detections['species_name'].str.contains(target_species, case=False, na=False)]
    target_species_df = target_species_df.drop(columns='species_name')
    target_species_df.to_csv(os.path.join(database_location, 'target_species_df.csv'), index=False)
    return target_species_df
