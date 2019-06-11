import matplotlib.pyplot as plt
import matplotlib.image as mpl_image
from matplotlib.patches import Polygon
import matplotlib.patheffects as PathEffects
import matplotlib.lines as mlines


def prepare(background_image_filename):
	image = mpl_image.imread(background_image_filename)
	plt.close(plt.gcf())
	plt.figure(figsize=(image.shape[1] / 100, image.shape[0] / 100))
	plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
	plt.imshow(image)
	plt.axis("off")
	plt.xlim([0, image.shape[1]])
	plt.ylim([image.shape[0], 0])


def point(*args, **kwargs):
	plt.scatter(*args, **kwargs)


def line(x1, y1, x2, y2, *args, **kwargs):
	plt.plot([x1, x2], [y1, y2], *args, **kwargs)


def polygons(polygons_data_list, *args, **kwargs):
	for polygon_data in polygons_data_list:
		pol = Polygon(polygon_data, *args, **kwargs)
		plt.gca().add_patch(pol)


def text(*args, **kwargs):
	effects = None
	if 'effects' in kwargs:
		effects = kwargs['effects']
		del kwargs['effects']

	txt = plt.text(*args, **kwargs)
	if effects is not None:
		txt.set_path_effects([PathEffects.withStroke(**effects)])


def save_as(*args, **kwargs):
	plt.savefig(*args, **kwargs)


def show():
	plt.show()
