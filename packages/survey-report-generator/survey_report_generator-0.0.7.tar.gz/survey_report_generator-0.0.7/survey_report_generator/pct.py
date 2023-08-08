from PIL import Image
from io import BytesIO
import requests
from .figures_utils import get_bounding_box, generate_figure
import pandas as pd


def generate_pct_map(kmls, detections, filename):
	bbox = get_bounding_box(kmls, detections)
	image = get_pct_map(bbox)
	generate_figure(kmls, detections, filename, bbox, image, path_colour='grey', alpha=1.0)


def get_pct_map(bbox, size=(512, 512)):
	"""
	This method takes the bounding box coordinates of a survey area and returns a PIL Image of the SVTM NSW Extant PCT
	at those coordinates.

	Args:
		bbox (tuple): a tuple with 4 elements in the order (x_min, y_min, x_max, y_max) containing the
			coordinates for the area you want to extract from the map
		size (tuple): a tuple with 2 elements in the order (width, height) specifying the size of the output image in pixels
	"""
	bounding_box = f'{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}'

	url = 'https://mapprod3.environment.nsw.gov.au/arcgis/rest/services/VIS/SVTM_NSW_Extant_PCT/MapServer/export'
	params = {
		'bbox': bounding_box,
		'bboxSR': '4326',
		'imageSR': '4326',
		'size': f'{size[0]},{size[1]}',
		'layers': 'show:0,1,2,3,4,5',
		'f': 'image'
	}

	response = requests.post(url, params=params)

	# Open the image using PIL
	image_bytes = response.content
	image = Image.open(BytesIO(image_bytes)).convert("RGBA")

	return image


def get_pct_info(lat, lon):
	"""
	This method takes the latitude and longitude coordinates and returns the information about the vegetation type
	at those coordinates.

	Args:
		lat (float): The latitude of the point of interest.
		lon (float): The longitude of the point of interest.
	"""

	url = 'https://mapprod3.environment.nsw.gov.au/arcgis/rest/services/VIS/SVTM_NSW_Extant_PCT/MapServer/identify'
	params = {
		'geometry': f'{lon},{lat}',
		'geometryType': 'esriGeometryPoint',
		'sr': '4326',
		'layers': 'all:2',
		'tolerance': '0',
		'mapExtent': '0,0,0,0',
		'imageDisplay': '800,600,96',  # example values, replace with actual values if available
		'returnGeometry': 'false',
		'f': 'json'
	}

	response = requests.post(url, params=params)
	json_response = response.json()

	# Normalize the JSON response into a dataframe
	df = pd.json_normalize(json_response['results'])

	# Create a new DataFrame with renamed and selected columns
	PCT_df = pd.DataFrame({
		'PCT_layerId': df['layerId'],
		'PCT_layerName': df['layerName'],
		'PCT_ID': df['attributes.PCTID'],
		'PCT_Name': df['attributes.PCTName'],
		'PCT_vegClass': df['attributes.vegClass'],
		'PCT_vegForm': df['attributes.vegForm'],
		'PCT_form': df['attributes.form_PCT']
	})

	return PCT_df


if __name__ == '__main__':
	kmls = pd.read_csv('databases/kmls.csv')
	detections = pd.read_csv('databases/detections.csv')
	generate_pct_map(kmls, detections)
