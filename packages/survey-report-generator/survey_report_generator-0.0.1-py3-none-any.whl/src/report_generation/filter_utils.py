import os
from datetime import datetime

import pandas as pd


def filter_location(report, columns_to_search, database):
    filtered_df = pd.DataFrame()
    for column in columns_to_search:
        search_allowed = not ('kml' in column.lower() and report.avoid_kmls)
        if search_allowed:
            column_mask = database[column].str.contains(report.location_filter, case=report.case, regex=report.regex,
                                                        na=False)
            concatenated_df = pd.concat([filtered_df, database[column_mask]])
            filtered_df = concatenated_df.drop_duplicates()
    return filtered_df


def filter_datetime(database, columns_to_search, start_date=None, end_date=None):
    """
    Filters out any dates that come before start_date or after end_date in any of the columns in columns_to_search

    Args:
        database (Pandas Dataframe): the database to filter
        columns_to_search (list): a list containing the date columns to filter
        start_date (str): a string in the format dd-mm-yyyy representing the earliest date you want to include, or None
        end_date (str): a string in the format dd-mm-yyyy representing the latest date you want to include, or None
    """
    filtered_df = pd.DataFrame()

    if start_date:
        start_date = datetime.strptime(start_date, '%d-%m-%Y')

    if end_date:
        end_date = datetime.strptime(end_date, '%d-%m-%Y')

    for column in columns_to_search:
        database[column] = pd.to_datetime(database[column])

        if start_date and end_date:
            mask = (database[column] > start_date) & (database[column] < end_date)
        elif start_date:
            mask = (database[column] > start_date)
        elif end_date:
            mask = (database[column] < end_date)
        else:
            mask = pd.Series(True, index=database.index)  # No filtering

        concatenated_df = pd.concat([filtered_df, database[mask]])
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
