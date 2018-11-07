import xml.etree.ElementTree as ET


class Network:
	def load_from_file(filename):
		tree = ET.parse(filename)
		root = tree.getroot()
		# print(root.tag, root.attrib, root.text)
		net = Network()
		# get nodes info
		for node in root[0][0]:
			net.add_node(Node(node.attrib['id']))

		# get links info
		for link in root[0][1]:
			connection = link.attrib['id'].split('_')[1:]
			net.add_link([int(x) for x in connection])

		return net

	def __init__(self):
		self.nodes = []
		self.links = []
		self.nodes_dict = {}
		self.links_dict = {}

	def add_node(self, node):
		self.nodes.append(node)
		self.nodes_dict[node.name] = node

	def add_link(self, pair):
		pair = tuple(pair)
		self.links.append(pair)
		self.links_dict[pair] = True

	def are_connected(self, first, second):
		conn = (first, second) in self.links_dict or (second, first) in self.links_dict
		return conn


class Node:
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "( {} )".format(self.name)