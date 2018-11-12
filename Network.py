import xml.etree.ElementTree as ET


class Network:
	def __init__(self):
		self.nodes = []
		self.links = []
		self.nodes_dict = {}
		self.links_dict = {}
		self.demands = {}
		self.paths_dict = {}

	def add_node(self, node):
		self.nodes.append(node)
		self.nodes_dict[node.name] = node

	def add_link(self, pair):
		pair = tuple(pair)
		self.links.append(pair)
		self.links_dict[pair] = True

	def add_demand(self, pair, value):
		pair = tuple(pair)
		self.demands[pair] = value

	def are_connected(self, first, second):
		conn = (first, second) in self.links_dict or (second, first) in self.links_dict
		return conn

	def demand_of(self, first, second):
		pair, pair_inv = (first, second), (second, first)
		if pair in self.demands:
			return self.demands[pair]
		elif pair_inv in self.demands:
			return self.demands[pair_inv]
		else:
			raise Exception("No demand between {} and {}".format(first, second))

	def paths_between(self, first, second):
		if (first, second) in self.paths_dict:
			return self.paths_dict[(first, second)]
		elif (second, first) in self.paths_dict:
			return list(list(reversed(path)) for path in self.paths_dict[(second, first)])
		raise Exception("No path between {} and {}".format(first, second))

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
			net.add_link(int(x) for x in connection)

		# get demands info
		for demand in root[1]:
			index = demand.attrib['id'].split('_')[1:]
			index = tuple(int(x) for x in index)
			value = float(demand[2].text)

			net.add_demand(index, value)

			# get admissible paths
			paths = []
			for path in demand[3]:
				links = []
				for link in path:
					pair = link.text.split('_')[1:]
					links.append(tuple(int(x) for x in pair))
				nodes = [index[0]]
				for link in links:
					if link[0] == nodes[-1]:
						nodes.append(link[1])
					else:
						nodes.append(link[0])
				paths.append(nodes)
			net.paths_dict[index] = paths

		return net


class Node:
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "( {} )".format(self.name)