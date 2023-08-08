# Survey Report Generator

[![PyPI version](https://badge.fury.io/py/survey-report-generator.svg)](https://badge.fury.io/py/survey-report-generator)

Report Generator is a Python package used to generate reports for drone surveys. 
You input the location name and a few other variables and the package will return a Word document pre-filled with tables and figures summarising the data collected for that survey.

## Installation

Install Report Generator with pip:

```bash
pip install survey-report-generator
```

## Usage

Initially, you need to create a Report object, outlined in the `report.py` file, which takes the following parameters:
- **Required Parameters**
  - `location_name (str)`: The title of the report, this could be the official name of the location like
    'Kalateenee State Forest' or 'Bongil Bongil National Park'.
  - `location_filter (str)`: A keyword or code to filter the location by, for example, 'bongil', 'kalateenee' or
    'FR:KK64'.
- **Optional Parameters**
  - `regex (bool)`: If set to `True`, the location filter inputs can be regular expressions. By default, this is set to `False`.
  - `case (bool)`: If set to `True`, the search will only return entries in the same case as the location filter. By default, this is set to `False`.
  - `avoid_kmls (bool)`: If set to `True`, the location filter will ignore searching kml columns. By default, this is set to `False`.
  - `target_species (str)`: Some of the tables and figures generated focus on a particular species of interest. By default this is set to `'koala'`.
  - `database_location (str)`: In order to generate the contents in the report, databases need to be downloaded to local storage. This parameter specifies the path to the location where you want these databases to be stored. It can be a directory which doesn't exist yet.
  - `start_date (str)`: a string in the format dd-mm-yyyy representing the earliest date you want to include.
  - `end_date (str)`: a string in the format dd-mm-yyyy representing the latest date you want to include.

Here are a few examples of how to initialise a Report object.

```python
from survey_report_generator import Report

meryla = Report(location_name='Meryla State Forest', location_filter='meryla')
bar = Report(location_name='Bar Flora Reserve', location_filter='Bar', avoid_kmls=True, case=True)
koreelah = Report(location_name='Koreelah State Forest', location_filter=r"[K|k]oo?ree?lah", avoid_kmls=True, regex=True)
```

Once you have a Report object, you can input this into the `generate_report()` method. 

```python
from survey_report_generator import generate_report

generate_report(report=meryla)
```

This will generate folders with databases and figures along with the report itself as a Word document.

## License

Report Generator is released under the [MIT License](LICENSE).
