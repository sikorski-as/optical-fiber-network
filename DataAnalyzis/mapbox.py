import requests

defaults = {
	'style': 'dark',
	'center_long': 0,
	'center_lati': 0,
	'zoom': 1,
	'map_width': 1024,
	'map_height': 512,
	'api_token': 'pk.eyJ1IjoibWNzcXVlZXppZSIsImEiOiJjamo3Mjg2bHUyNGwyM3FtbmhkYWNxaG12In0.iJNSfWOnLKzxq_shjNez9g'
}

style_urls = {
	# needs placeholders for api parameters: center_long, center_lati, zoom, map_width, map_height, api_token
	'dark': 'https://api.mapbox.com/styles/v1/mapbox/dark-v9/static/{},{},{}/{}x{}?access_token={}',
	'countries_basic': 'https://api.mapbox.com/styles/v1/mcsqueezie/cjuzqthv51t001fs6e6mmelrl/static/{},{},{}/{}x{}?access_token={}',
}


def request_link(style, center_long, center_lati, zoom, map_width, map_height, api_token):
	link = style_urls[style].format(
		center_long,
		center_lati,
		zoom,
		map_width,
		map_height,
		api_token
	)
	return link


def get_map_as_file(filename, mapdata=None):
	if mapdata is None:
		mapdata = defaults
		if mapdata['api_token'] is None:
			return False

	try:
		url = request_link(**mapdata)
		r = requests.get(url, allow_redirects=True)
		if r.status_code != requests.codes.ok:
			return False
		file = open(filename, 'wb')
		file.write(r.content)
		file.close()
		return True
	except Exception as e:
		print(e)
		return False
