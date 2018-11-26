import xml.etree.ElementTree as ET


class Network:
	def __init__(self, name='Unnamed Network'):
		self.name = name
		self.nodes = []
		self.links = []  # to be removed
		self.nodes_dict = {}  # node name -> id in nodes list
		self.links_dict = {}  # pair (node1_id, node2_id) -> True
		self.demands = {}  # pair (node1_id, node2_id) ->
		self.paths_dict = {}  # pair

	def number_of_nodes(self):
		""" Return  number of nodes. """
		return len(self.nodes)

	def number_of_links(self):
		""" Return number of links. """
		return len(self.links_dict)

	def add_node(self, node):
		""" Add node and return its id.  """
		self.nodes.append(node)
		node_id = len(self.nodes_dict)
		self.nodes_dict[node.name] = node_id
		return node_id

	def add_link(self, pair):
		""" Add link between nodes specified as a tuple of IDs. """
		pair = tuple(pair)
		self.links.append(pair)
		self.links_dict[pair] = True

	def add_demand(self, pair, value=0.0):
		""" Add demand between nodes specified as a tuple of IDs and set its value. """
		pair = tuple(pair)
		self.demands[pair] = value

	def are_connected(self, pair):
		""" Return if there is a link between nodes specified as a tuple of IDs. """
		pair = tuple(pair)
		pair_inv = pair[::-1]
		conn = (pair in self.links_dict) or (pair_inv in self.links_dict)
		return conn

	def demand_of(self, pair):
		"""
		Return demanded value between nodes specified as a pair.
		Raise an exception if there is not such demand.
		"""
		pair = tuple(pair)
		pair_inv = pair[::-1]
		if pair in self.demands:
			return self.demands[pair]
		elif pair_inv in self.demands:
			return self.demands[pair_inv]
		else:
			raise Exception("No demand between {} and {}.".format(*pair))

	def add_admissible_path(self, path):
		"""
		Add an admissible path provided as a list of node IDs.
		Raise an exception if such path is invalid
		"""
		pair = (path[0], path[-1])
		pair_inv = pair[::-1]
		# verify demand
		if (pair in self.demands) and (pair_inv not in self.demands):
			raise Exception('There is no such demand for this admissible path.'.format(node_id))

		# verify nodes
		for node_id in path:
			if node_id < 0 or node_id >= self.number_of_nodes():
				raise Exception('Node with ID={} does not exists in the network.'.format(node_id))

		# verify path
		for i in range(len(path) - 1):
			if not self.are_connected(path[i:i+2]):
				raise Exception('Such path in the network is not possible.')

		self.paths_dict[pair] = path

	def has_admissible_paths(self):
		""" Return if any admissible path is specified. """
		return len(self.paths_dict) > 0

	def paths_between(self, pair):
		"""
		Return list of paths between nodes specified as a pair of nodes.
		Each path starts with a node specified as first element of the pair.
		"""
		pair = tuple(pair)
		pair_inv = pair[::-1]

		if pair in self.paths_dict:
			return self.paths_dict[pair]
		elif pair_inv in self.paths_dict:
			return list(list(reversed(path)) for path in self.paths_dict[pair_inv])

		if return_empty:
			return []
		else:
			raise Exception("No path between {} and {}".format(*pair))

	def node_list(self, sequence):
		""" Exchange a sequence of node IDs into a generator of corresponding node objects. """
		for node_id in sequence:
			yield self.nodes[node_id]

	def index_of(self, node):
		""" Return ID of a provided node. Raise an exception if there's no such node. """
		for i, network_node in enumerate(self.nodes):
			if network_node == node:
				return i
		raise Exception("Node {} does not belong to the network.".format(node))

	def load_structure(self, filename):
		""" Load nodes and links from a specified *.xml file. """
		tree = ET.parse(filename)
		root = tree.getroot()
		structure = root.find('networkStructure')
		# print(root.tag, root.attrib, root.text)

		# get nodes
		for node in structure.find('nodes'):
			node_name = node.attrib['id']
			self.add_node(Node(node_name))

		# get links
		for link in structure.find('links'):
			source = link.find('source').text
			target = link.find('target').text
			connection = (self.nodes_dict[source], self.nodes_dict[target])
			self.add_link(connection)

	def load_demands(self, filename, admissible_paths=0):
		"""
		Load demands from a specified *.xml file.
		Loads a specified number of admissible paths for this demand.
		"""
		tree = ET.parse(filename)
		root = tree.getroot()

		# get demands info
		for demand_id, demand in enumerate(root.find('demands')):
			source = self.nodes_dict[demand.find('source').text]
			target = self.nodes_dict[demand.find('target').text]
			index = (source, target)
			value = float(demand.find('demandValue').text)

			self.add_demand(index, value)

			# get admissible paths
			if demand_id < admissible_paths:
				for path in demand.find('admissiblePaths'):
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
					self.add_admissible_path(nodes)

	@staticmethod
	def load_from_file(filename, structure=True, demands=True, admissible_paths=0):
		"""  Load structure structure, demands and admissible paths from a specified *.xml file. """
		net = Network()
		if structure:
			net.load_structure(filename)
		if demands:
			net.load_demands(filename, admissible_paths=admissible_paths)
		return net


class Node:
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "({})".format(self.name)


def example():
	""" Example operations using Network class. """
	net = Network.load_from_file('Resources/net-us.xml', structure=True, demands=True, admissible_paths=0)

	print('Nodes in the loaded network:')
	nodes = [node.name for node in net.nodes]
	print(nodes, '\n')

	print('Links in the loaded network:')
	for link in net.links:
		source, target = link
		print(net.nodes[source].name, '<->', net.nodes[target].name)

	print('\nDemands in the loaded network:')

	for pair, demand in net.demands.items():
		source, target = pair
		print(net.nodes[source].name, '<->', net.nodes[target].name, '=', demand)

		if net.has_admissible_paths():
			print('Admissible paths between {} and {}:'.format(net.nodes[source].name, net.nodes[target].name))
			for path in net.paths_between(source, target):
				print([net.nodes[x].name for x in path])
	if net.has_admissible_paths():
		paths, path_reversed = net.paths_between(0, 1), net.paths_between(1, 0)
		print(paths)
		print(path_reversed)

		for path in paths:
			print('path:')
			for node in net.node_list(path):
				print('\t', node)

	random_node = Node('Berlin')
	try:
		net.index_of(random_node)
	except Exception as e:
		print(str(e))

	x = net.add_node(random_node)
	#net.add_admissible_path([0, 1, 500])