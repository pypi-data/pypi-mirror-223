import calendar
from datetime import date

import pandas as pd


def add_dates(report):
    # Concatenate the DataFrames vertically
    combined_df = pd.concat([report.surveys['survey_start'], report.detections['date']], axis=0)
    # Find the earliest date in either column
    start_date = pd.to_datetime(combined_df).min()
    report.context['start_day'] = start_date.day
    start_month = calendar.month_name[int(start_date.month)]
    report.context['start_month'] = calendar.month_name[int(start_date.month)]
    report.context['start_year'] = start_date.year
    report.context['start_date'] = f'{start_date.day} {start_month} {start_date.year}'

    # Add end dates
    end_date = pd.to_datetime(combined_df).max()
    report.context['end_day'] = end_date.day
    end_month = calendar.month_name[end_date.month]
    report.context['end_month'] = end_month
    report.context['end_year'] = end_date.year
    report.context['end_date'] = f'{end_date.day} {end_month} {end_date.year}'

    # Add today's date in various formats
    report.context['today_month_year'] = date.today().strftime("%B %Y")
    report.context['today_year'] = date.today().strftime("%Y")

    return report.context


def add_summary_dates(report):
    # Add start dates
    survey_df = report.surveys_summary
    detections_df = report.detections_summary
    # Concatenate the DataFrames vertically
    combined_df = pd.concat([survey_df['survey_start'], detections_df['date']], axis=0)
    # Find the earliest date in either column
    start_date = pd.to_datetime(combined_df).min()
    report.context['start_day_summary'] = start_date.day
    start_month = calendar.month_name[int(start_date.month)]
    report.context['start_month_summary'] = calendar.month_name[int(start_date.month)]
    report.context['start_year_summary'] = start_date.year
    report.context['start_date_summary'] = f'{start_date.day} {start_month} {start_date.year}'

    # Add end dates
    end_date = pd.to_datetime(combined_df).max()
    report.context['end_day_summary'] = end_date.day
    end_month = calendar.month_name[end_date.month]
    report.context['end_month_summary'] = end_month
    report.context['end_year_summary'] = end_date.year
    report.context['end_date_summary'] = f'{end_date.day} {end_month} {end_date.year}'

    # The number of days between the two dates
    report.context['num_days_summary'] = (end_date - start_date).days
    # The number of days surveyed
    surveys_unique_dates = pd.to_datetime(survey_df['survey_start']).dt.date.nunique()
    detections_unique_dates = pd.to_datetime(detections_df['date']).dt.date.nunique()
    # Choose the higher count
    report.context['days_surveyed_summary'] = max(surveys_unique_dates, detections_unique_dates)

    # Add today's date in various formats
    report.context['today_month_year_summary'] = date.today().strftime("%B %Y")
    report.context['today_year_summary'] = date.today().strftime("%Y")

    return report.context
