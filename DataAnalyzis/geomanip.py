import math


def longitude_to_x(long, zoom):
	long = math.radians(long)
	ret = 256/math.pi * math.pow(2, zoom) * (long + math.pi)
	return ret


def latitude_to_y(lati, zoom):
	lati = math.radians(lati)
	ret = 256/math.pi * math.pow(2, zoom) * (math.pi - math.log(math.tan((math.pi / 4) + lati / 2)))
	return ret


def get_x(long, center_long, map_width, zoom, **rest):
	ret = longitude_to_x(long, zoom) - longitude_to_x(center_long, zoom) + map_width / 2
	return ret


def get_y(lati, center_lati, map_height, zoom, **rest):
	ret = latitude_to_y(lati, zoom) - latitude_to_y(center_lati, zoom) + map_height / 2
	return ret


def haversine(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance between two points
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	c = 2 * math.asin(math.sqrt(a))
	r = 6371  # Radius of earth in kilometers. Use 3956 for miles
	return c * r
