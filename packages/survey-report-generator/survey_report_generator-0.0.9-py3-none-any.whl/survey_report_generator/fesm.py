from PIL import Image
from io import BytesIO
import requests
from .figures_utils import get_bounding_box, generate_figure
import pandas as pd


def generate_fesm_map(kmls, detections, filename):
	bbox = get_bounding_box(kmls, detections)
	image = get_fesm_map(bbox)
	generate_figure(kmls, detections, filename, bbox, image, path_colour='lightgray', alpha=1.0)


def get_fesm_map(bbox, size=(512, 512)):
	"""
	This method takes the bounding box coordinates of a survey area and returns a PIL Image of the FESM 2016-2021
	at those coordinates.

	Args:
		bbox (tuple): a tuple with 4 elements in the order (x_min, y_min, x_max, y_max) containing the
			coordinates for the area you want to extract from the map
		size (tuple): a tuple with 2 elements in the order (width, height) specifying the size of the output image in pixels
	"""
	bounding_box = f'{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}'

	url = 'https://mapprod3.environment.nsw.gov.au/arcgis/rest/services/Fire/FESM_2016_2021/MapServer/export'
	params = {
		'bbox': bounding_box,
		'bboxSR': '4326',
		'imageSR': '4326',
		'size': f'{size[0]},{size[1]}',
		# Do we need all layers?
		'layers': 'show:0,1,2,3,4',
		'f': 'image'
	}

	response = requests.post(url, params=params)

	# Open the image using PIL
	image_bytes = response.content
	image = Image.open(BytesIO(image_bytes)).convert("RGBA")

	return image


def get_fesm_info(lat, lon):
	"""
	This method takes the latitude and longitude coordinates and returns the information about the fire extent and
	severity at those coordinates.

	Args:
		lat (float): The latitude of the point of interest.
		lon (float): The longitude of the point of interest.
	"""

	url = 'https://mapprod3.environment.nsw.gov.au/arcgis/rest/services/Fire/FESM_2016_2021/MapServer/identify'
	params = {
		'geometry': f'{lon},{lat}',
		'geometryType': 'esriGeometryPoint',
		'sr': '4326',
		'layers': 'all:1,2,3,4,5',
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

	# Create a new DataFrame with renamed and selected columns
	FESM_df = pd.DataFrame({
		'FESM_layerId': df['layerId'],
		'FESM_layerName': df['layerName'],
		'FESM_ColorIndex': df['attributes.Color Index'],
		'FESM_OBJECTID': df['attributes.OBJECTID']
	})

	return FESM_df


if __name__ == '__main__':
	kmls = pd.read_csv('databases/kmls.csv')
	detections = pd.read_csv('databases/detections.csv')
	generate_fesm_map(kmls, detections)
