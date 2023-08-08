import os

import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy", message=".*Intel MKL WARNING.*")

from . import download_files
from .databases import generate_survey_database, generate_detections_database, \
    generate_airdata_database, generate_kml_database


class Report:
    """
    This class represents a report object and includes all variables necessary to extract relevant data to build a
    report.
    """

    def __init__(self, location_name, location_filter, target_species='koala', regex=False, case=False,
                 avoid_kmls=False, database_location='databases', start_date=None, end_date=None):
        """
        Args:
            location_name (str): The title of the report, this could be the official name of the location like
            'Kalateenee State Forest' or 'Bongil Bongil National Park'.
            location_filter (str): A keyword or code to filter the location by, for example, 'bongil', 'kalateenee' or
            'FR:KK64'.
            regex (bool): If set to true, the location filter inputs can be regular expressions.
            case (bool): If set to True, the search will only return entries in the same case as the location filter
            avoid_kmls (bool): If set to True, the location filter will avoid searching the kml columns.
            target_species (str): This is an optional input to change the focus of the report to an animal other
            than a koala, for example, 'glider'.
            database_location (str): Folder where the databases are stored
            start_date (str): a string in the format dd-mm-yyyy representing the earliest date you want to include
            end_date (str): a string in the format dd-mm-yyyy representing the latest date you want to include
        """
        # Initial report parameters
        self.location_name = location_name
        self.location_filter = location_filter
        self.target_species = target_species
        self.regex = regex
        self.case = case
        self.avoid_kmls = avoid_kmls
        self.database_location = database_location
        self.start_date = start_date
        self.end_date = end_date
        self.context = {
            'location_name': self.location_name,
            'target_species': self.target_species,
            'target_species_capitalised': self.target_species.capitalize()
        }

        # Dataframes that contain the summary information across all flora reserves
        if os.path.exists(os.path.join(database_location, 'summary')):
            self.surveys_summary = pd.read_csv(os.path.join(database_location, 'summary', 'surveys.csv'))
            self.locations_summary = pd.read_csv(os.path.join(database_location, 'summary', 'locations.csv'))
            self.detections_summary = pd.read_csv(os.path.join(database_location, 'summary', 'detections.csv'))
            self.detections_list_summary = pd.read_csv(os.path.join(database_location, 'summary', 'detections_list.csv'))
            self.species_list_summary = pd.read_csv(os.path.join(database_location, 'summary', 'species_list.csv'))
            self.airdata_summary = pd.read_csv(os.path.join(database_location, 'summary', 'airdata.csv'))
            self.table_df_summary = pd.read_csv(os.path.join(database_location, 'summary', 'table_df.csv'))

        # Dataframes that will be generated for each flora reserve
        self.airdata = None
        self.detections = None
        self.detections_list = None
        self.kmls = None
        self.locations = None
        self.species_list = None
        self.surveys = None
        self.table_df = None
        self.target_species_df = None

    def export_dataframes(self, location):
        """Exports all dataframe that have been generated to 'location' folder."""
        if self.airdata is not None:
            self.airdata.to_csv(os.path.join(location, 'airdata.csv'), index=False)
        if self.detections is not None:
            self.detections.to_csv(os.path.join(location, 'detections.csv'), index=False)
        if self.detections_list is not None:
            self.detections_list.to_csv(os.path.join(location, 'detections_list.csv'), index=False)
        if self.kmls is not None:
            self.kmls.to_csv(os.path.join(location, 'kmls.csv'), index=False)
        if self.locations is not None:
            self.locations.to_csv(os.path.join(location, 'locations.csv'), index=False)
        if self.species_list is not None:
            self.species_list.to_csv(os.path.join(location, 'species_list.csv'), index=False)
        if self.surveys is not None:
            self.surveys.to_csv(os.path.join(location, 'surveys.csv'), index=False)
        if self.table_df is not None:
            self.table_df.to_csv(os.path.join(location, 'table_df.csv'), index=False)
        if self.target_species_df is not None:
            self.target_species_df.to_csv(os.path.join(location, 'target_species_df.csv'), index=False)
        if self.table_df is not None:
            self.table_df.to_csv(os.path.join(location, 'table_df.csv'), index=False)

    def export_summary_dataframes(self, location):
        if self.detections_list_summary is not None:
            self.detections_list.to_csv(os.path.join(location, 'detections_list.csv'), index=False)
        if self.species_list_summary is not None:
            self.species_list.to_csv(os.path.join(location, 'species_list.csv'), index=False)
        if self.surveys_summary is not None:
            self.surveys_summary.to_csv(os.path.join(location, 'surveys.csv'), index=False)
        if self.locations_summary is not None:
            self.locations_summary.to_csv(os.path.join(location, 'locations.csv'), index=False)
        if self.detections_summary is not None:
            self.detections_summary.to_csv(os.path.join(location, 'detections.csv'), index=False)
        if self.airdata_summary is not None:
            self.airdata_summary.to_csv(os.path.join(location, 'airdata.csv'), index=False)
        if self.table_df_summary is not None:
            self.table_df_summary.to_csv(os.path.join(location, 'table_df.csv'), index=False)

    def generate_databases(self, download_databases):
        """Generates the main databases needed for filling the report"""
        if download_databases:
            download_files.download_databases(self.database_location)
        self.surveys, self.locations = generate_survey_database(self)
        self.detections = generate_detections_database(self)
        self.airdata = generate_airdata_database(self)
        self.kmls = generate_kml_database(self)
