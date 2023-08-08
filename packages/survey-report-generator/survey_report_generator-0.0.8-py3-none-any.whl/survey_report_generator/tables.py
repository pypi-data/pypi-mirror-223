import math
import os

import pandas as pd
import numpy as np

from .filter_utils import filter_species_names, filter_target_species


def add_survey_results_table(report):
    target_species_df = filter_target_species(report.detections, report.target_species, report.database_location)
    target_species_df.loc[:, 'gt_outcome'] = target_species_df.gt_outcome.fillna('unvalidated')
    target_species_df.loc[:, 'gt_outcome'] = target_species_df.gt_outcome.replace('unconfirmed', 'unvalidated')
    target_species_df.loc[:, 'probability'] = target_species_df.probability.fillna('Null')
    table_df = target_species_df[['gt_outcome', 'detection_count', 'probability']]
    report.table_df = table_df

    # Fill the report.context dictionary with pivot table values
    pivot_table = pd.pivot_table(table_df, values='detection_count', index='probability', columns='gt_outcome',
                                 aggfunc=np.sum, fill_value=0, margins=True, margins_name='Total')

    for row_index, row in pivot_table.iterrows():
        for column_name in pivot_table.columns:
            key = f'{row_index}_{column_name}'
            cell_value = row[column_name]
            report.context[key] = int(cell_value)

    # Fill in entries that might be missing with a default value of 0
    possible_keys = ['Definite_confirmed', 'Definite_negative', 'Definite_unvalidated', 'Definite_Total',
                     'High_confirmed', 'High_negative', 'High_unvalidated', 'High_Total',
                     'Medium_confirmed', 'Medium_negative', 'Medium_unvalidated', 'Medium_Total',
                     'Low_confirmed', 'Low_negative', 'Low_unvalidated', 'Low_Total',
                     'Null_confirmed', 'Null_negative', 'Null_unvalidated', 'Null_Total',
                     'Total_confirmed', 'Total_negative', 'Total_unvalidated', 'Total_Total']

    [report.context.setdefault(key, 0) for key in possible_keys]

    # (Number of animals detected / number of repeat surveys) / number of hectares per plot = animals per hectare
    report.context['species_density'] = np.round((report.context['Total_Total'] / 50 / 25), 3)
    # (Number of animals confirmed / number of repeat surveys) / number of hectares per plot = animals per hectare
    report.context['confirmed_density'] = np.round((report.context['Total_confirmed'] / 50 / 25), 3)
    high_prob_confirmed = report.context['Definite_confirmed'] + report.context['High_confirmed']
    high_prob_total = report.context['Definite_Total'] + report.context['High_Total']
    # % of koalas that were labelled as high probability detections, validated as confirmed
    if high_prob_total != 0:
        validated_percentage = high_prob_confirmed / high_prob_total
    else:
        validated_percentage = 0

    report.context['validated_percentage'] = int(np.round(validated_percentage * 100, 0))


def add_survey_results_summary_table(report):
    target_species_df = filter_target_species(report.detections_summary, report.target_species,
                                              report.database_location)
    # koala_detections = koala_detections.dropna(subset=['probability'])
    target_species_df.loc[:, 'gt_outcome'] = target_species_df.gt_outcome.fillna('unvalidated')
    target_species_df.loc[:, 'gt_outcome'] = target_species_df.gt_outcome.replace('unconfirmed', 'unvalidated')
    target_species_df.loc[:, 'probability'] = target_species_df.probability.fillna('Null')
    table_df = target_species_df[['gt_outcome', 'detection_count', 'probability']]
    table_df.to_csv(os.path.join('databases', 'summary', 'table_df.csv'), index=False)

    # Fill the report.context dictionary with pivot table values
    pivot_table = pd.pivot_table(table_df, values='detection_count', index='probability', columns='gt_outcome',
                                 aggfunc=np.sum, fill_value=0, margins=True, margins_name='Total')

    for row_index, row in pivot_table.iterrows():
        for column_name in pivot_table.columns:
            key = f'{row_index}_{column_name}_summary'
            cell_value = row[column_name]
            report.context[key] = int(cell_value)

    # Fill in entries that might be missing with a default value of 0
    possible_keys = ['Definite_confirmed_summary', 'Definite_negative_summary', 'Definite_unvalidated_summary',
                     'Definite_Total_summary', 'High_confirmed_summary', 'High_negative_summary',
                     'High_unvalidated_summary', 'High_Total_summary', 'Medium_confirmed_summary',
                     'Medium_negative_summary', 'Medium_unvalidated_summary', 'Medium_Total_summary',
                     'Low_confirmed_summary', 'Low_negative_summary', 'Low_unvalidated_summary',
                     'Low_Total_summary', 'Null_confirmed_summary', 'Null_negative_summary',
                     'Null_unvalidated_summary', 'Null_Total_summary', 'Total_confirmed_summary',
                     'Total_negative_summary', 'Total_unvalidated_summary', 'Total_Total_summary']

    [report.context.setdefault(key, 0) for key in possible_keys]

    # (Number of animals detected / number of repeat surveys) / number of hectares per plot = animals per hectare
    report.context['species_density_summary'] = np.round((report.context['Total_Total_summary'] / 50 / 25), 3)
    # (Number of animals confirmed / number of repeat surveys) / number of hectares per plot = animals per hectare
    report.context['confirmed_density_summary'] = np.round((report.context['Total_confirmed_summary'] / 50 / 25), 3)
    high_prob_confirmed = report.context['Definite_confirmed_summary'] + report.context['High_confirmed_summary']
    high_prob_total = report.context['Definite_Total_summary'] + report.context['High_Total_summary']

    # % of koalas that were labelled as high probability detections, validated as confirmed
    if high_prob_total != 0:
        validated_percentage = high_prob_confirmed / high_prob_total
    else:
        validated_percentage = 0

    report.context['validated_percentage_summary'] = int(np.round(validated_percentage * 100, 0))


def add_site_details_table(report):
    report.context['num_plots'] = len(report.locations)
    report.context['num_pilots'] = max(report.airdata['pilot'].nunique(), report.surveys['pilot'].nunique())

    # The number of days surveyed
    surveys_unique_dates = pd.to_datetime(report.surveys['survey_start']).dt.date.nunique()
    detections_unique_dates = pd.to_datetime(report.detections['date']).dt.date.nunique()
    # Choose the higher count
    report.context['days_surveyed'] = max(surveys_unique_dates, detections_unique_dates)
    denom = report.context['num_pilots'] * report.context['days_surveyed']
    if denom == 0:
        plots_per_pilot_per_night = 0
        print(f"report.context['num_pilots']: {report.context['num_pilots']}, report.context['days_surveyed']: {report.context['days_surveyed']}")
    else:
        plots_per_pilot_per_night = report.context['num_plots'] / (denom)
    report.context['plots_per_pilot_per_night'] = math.ceil(plots_per_pilot_per_night)
    report.context['survey_effort'] = int(round(report.surveys['location_area'].sum() / 10000, 0))


def add_site_details_summary_table(report):
    report.context['num_plots_summary'] = len(report.locations_summary)
    report.context['num_pilots_summary'] = max(report.airdata_summary['pilot'].nunique(),
                                               report.surveys_summary['pilot'].nunique())

    # The number of days surveyed
    surveys_unique_dates = pd.to_datetime(report.surveys_summary['survey_start']).dt.date.nunique()
    detections_unique_dates = pd.to_datetime(report.detections_summary['date']).dt.date.nunique()
    # Choose the higher count
    report.context['days_surveyed_summary'] = max(surveys_unique_dates, detections_unique_dates)
    plots_per_pilot_per_night = report.context['num_plots_summary'] / (report.context['num_pilots_summary'] * report.context[
        'days_surveyed_summary'])
    report.context['plots_per_pilot_per_night_summary'] = math.ceil(plots_per_pilot_per_night)
    # Round the survey effort to the nearest hectare
    report.context['survey_effort_summary'] = int(round(report.surveys_summary['location_area'].sum() / 10000, 0))


def add_plots_table(report):
    report.locations['hectares'] = round(report.locations['total_area'] / 10000, 0).astype(int)
    table = report.locations[['location_id', 'hectares']]
    sites = ['kuluwan', 'lindesay', 'donaldson', 'crescent', 'corrabare']
    if report.location_filter in sites:
        table = table[table['hectares'] != 0]
    report.context['plot_table'] = table.to_dict('records')


def add_detections_list(report):
    detections_list = filter_species_names(report.detections)
    detections_list['waypoint'] = detections_list.apply(lambda row: f"{row['lat']}, {row['lon']}", axis=1)
    detections_list = detections_list[['date', 'time', 'species_name', 'detection_count', 'waypoint', 'comments']]
    detections_list['date'] = pd.to_datetime(detections_list['date'])
    detections_list['date'] = detections_list['date'].dt.strftime('%d/%m/%Y')
    detections_list['detection_count'] = detections_list['detection_count'].astype(int)
    detections_list = detections_list.rename(columns={'detection_count': 'count'})
    detections_list['comments'] = detections_list['comments'].fillna('')
    detections_list['waypoint'] = detections_list['waypoint'].replace('nan, nan', '')
    report.context['appendix_table'] = detections_list.to_dict('records')
    report.detections_list = detections_list


def add_species_list(report):
    detections_list = report.detections_list.sort_values('species_name')
    species_list = detections_list[['species_name', 'count']].groupby('species_name')['count'].sum()
    species_list = species_list.reset_index()  # Reset the index to include 'species_name' as a column
    report.species_list = species_list
    report.context['species_list'] = species_list.to_dict('records')


def add_detections_list_summary(report):
    detections_list = filter_species_names(report.detections_summary)
    detections_list['waypoint'] = detections_list.apply(lambda row: f"{row['lat']}, {row['lon']}", axis=1)
    detections_list = detections_list[['date', 'time', 'species_name', 'detection_count', 'waypoint', 'comments']]
    detections_list['date'] = pd.to_datetime(detections_list['date'])
    detections_list['date'] = detections_list['date'].dt.strftime('%d/%m/%Y')
    detections_list['detection_count'] = detections_list['detection_count'].astype(int)
    detections_list = detections_list.rename(columns={'detection_count': 'count'})
    detections_list['comments'] = detections_list['comments'].fillna('')
    detections_list['waypoint'] = detections_list['waypoint'].replace('nan, nan', '')
    # report.context['appendix_table'] = detections_list.to_dict('records')
    report.detections_list_summary = detections_list


def add_species_list_summary(report):
    detections_list = report.detections_list_summary.sort_values('species_name')
    species_list = detections_list[['species_name', 'count']].groupby('species_name')['count'].sum()
    species_list = species_list.reset_index()  # Reset the index to include 'species_name' as a column
    report.species_list_summary = species_list
    report.context['species_list_summary'] = species_list.to_dict('records')
