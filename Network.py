import xml.etree.ElementTree as ET
import random

import Parameters

"""
	Opis
	Atributes:
	Locals:
	Returns:
	Raises:
"""


class Network:
	"""
		Atributes:
			name: name of network
			nodes: list of Node objects
			nodes_dict:
	"""
	def __init__(self, name='Unnamed Network'):
		"""
			Atributes:
				name: name of network
				nodes: list of nodes
				nodes_dict: dictionary, key - node.name, value - index of node in nodes
				links_dict: key - tuple(x, y): begin of edge, end of edge
				demands_dict: key - tuple(x, y): begin of path, end of path
				paths_dict: key - tuple(x, y): begin of path, end of path
		"""
		self.name = name
		self.nodes = []
		self.nodes_dict = {}    # node name -> id in nodes list
		self.links_dict = {}    # pair (node1_id, node2_id) -> True
		self.demands_dict = {}  # pair (node1_id, node2_id) -> demanded value
		self.paths_dict = {}    # pair (node1_id, node2_id) -> list of paths, each path = a list

	#
	# NODES
	#

	def number_of_nodes(self):
		""" Return  number of nodes. """
		return len(self.nodes)

	def add_node(self, node):
		""" Add node and return its id.  """
		self.nodes.append(node)
		node_id = len(self.nodes_dict)
		self.nodes_dict[node.name] = node_id
		return node_id

	def nodes_range(self):
		""" Return a range with IDs of all nodes. """
		return range(len(self.nodes))

	#
	# LINKS
	#

	def number_of_links(self):
		""" Return number of links. """
		return len(self.links_dict)

	def add_link(self, pair):
		""" Add link between nodes specified as a tuple of IDs. """
		pair = tuple(pair)
		self.links_dict[pair] = True

	def are_connected(self, pair):
		""" Return if there is a link between nodes specified as a tuple of IDs. """
		pair = tuple(pair)
		pair_inv = pair[::-1]
		conn = (pair in self.links_dict) or (pair_inv in self.links_dict)
		return conn

	def neighbours_of(self, node_id):
		""" Return a list of neighbours of a provided node. """
		n_list = []
		for id in self.nodes_range():
			pair = (node_id, id)
			if self.are_connected(pair):
				n_list.append(id)
		return n_list

	#
	# DEMANDS
	#

	def add_demand(self, pair, value=0.0):
		""" Add demand between nodes specified as a tuple of IDs and set its value. """
		pair = tuple(pair)
		self.demands_dict[pair] = value

	def demand_of(self, pair):
		"""
		Return demanded value between nodes specified as a pair.
		Raise an exception if there is not such demand.
		"""
		pair = tuple(pair)
		pair_inv = pair[::-1]
		if pair in self.demands_dict:
			return self.demands_dict[pair]
		elif pair_inv in self.demands_dict:
			return self.demands_dict[pair_inv]
		else:
			raise Exception("No demand between {} and {}.".format(*pair))

	#
	# ADMISSIBLE PATHS
	#

	def number_of_admissible_paths(self):
		""" Return number of admissible paths. """
		return len(self.paths_dict)

	def add_admissible_path(self, path):
		"""
		Add an admissible path provided as a list of node IDs.
		Raise an exception if such path is invalid
		"""
		pair = (path[0], path[-1])
		pair_inv = pair[::-1]
		# verify demand
		if (pair not in self.demands_dict) and (pair_inv not in self.demands_dict):
			raise Exception('There is no such demand for this admissible path.')

		# verify nodes
		for node_id in path:
			if node_id < 0 or node_id >= self.number_of_nodes():
				raise Exception('Node with ID={} does not exists in the network.'.format(node_id))

		# verify path
		for i in range(len(path) - 1):
			if not self.are_connected(path[i:i+2]):
				raise Exception('Such path in the network is not possible.')

		if pair not in self.paths_dict:
			self.paths_dict[pair] = []
			self.paths_dict[pair].append(path)
		else:
			self.paths_dict[pair].append(path)

	def add_admissible_paths(self, paths):
		for path in paths:
			self.add_admissible_path(path)

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

		raise Exception("No path between {} and {}".format(*pair))

	#
	# ANOTHER USEFUL FUNCS
	#

	def generate_all_paths_between(self, pair, max_amount_of_paths):
		"""

		"""
		paths_created = 0
		start, end = pair
		queue = [(start, [start])]
		while queue:
			(vertex, path) = queue.pop(0)
			for next in set(self.neighbours_of(vertex)) - set(path):
				if next == end:
					yield path + [next]
					paths_created += 1
				else:
					queue.append((next, path + [next]))
			if paths_created == max_amount_of_paths:
				break
	#
	# LOADING FROM FILE
	#

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
		Loads a specified number of admissible paths for each demand.
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
			demand_paths = demand.find('admissiblePaths') # this is none if trying to load demands for net-us.xml
			if admissible_paths > 0 and demand_paths is not None:
				for i, path in enumerate(demand_paths):
					if i < admissible_paths:
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

	@staticmethod
	def generate_network_with_admissible_paths(max_path_amount, file_path):
		net = Network.load_from_file(file_path, structure=True, demands=True, admissible_paths=0)
		visited = set()
		for element in net.nodes_dict:
			el_id = net.nodes_dict[element]
			visited.add(element)
			for vertex in set(net.nodes_dict) - visited:
				v_id = net.nodes_dict[vertex]
				pair = (el_id, v_id)
				all_paths_between = list(net.generate_all_paths_between(pair, max_path_amount))
				admissible_paths = list()
				admissible_paths.append(list(all_paths_between[0]))  # always add the shortest path
				random_paths = random.sample(all_paths_between[1:], Parameters.Parameters.number_of_adm_paths_usa - 1)
				for path in random_paths:
					admissible_paths.append(list(path))
				net.add_admissible_paths(admissible_paths)
		return net

	@staticmethod
	def generate_network_with_admissible_paths2(max_path_amount, file_path):
		net = Network.load_from_file(file_path, structure=True, demands=True, admissible_paths=0)
		visited = set()
		for element in net.nodes_dict:
			el_id = net.nodes_dict[element]
			visited.add(element)
			for vertex in set(net.nodes_dict) - visited:
				v_id = net.nodes_dict[vertex]
				pair = (el_id, v_id)
				all_paths_between = list(net.generate_all_paths_between(pair, max_path_amount))
				admissible_paths = list()
				admissible_paths.append(list(all_paths_between[0]))  # always add the shortest path
				random_paths = random.sample(all_paths_between[1:], 1)
				for path in random_paths:
					admissible_paths.append(list(path))
				net.add_admissible_paths(admissible_paths)
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
	for link in net.links_dict:
		source, target = link
		print(net.nodes[source].name, '<->', net.nodes[target].name)

	print('\nDemands in the loaded network:')

	for pair, demand in net.demands_dict.items():
		source, target = pair
		print(net.nodes[source].name, '<->', net.nodes[target].name, '=', demand)

		if net.number_of_admissible_paths() > 0:
			print('Admissible paths between {} and {}:'.format(net.nodes[source].name, net.nodes[target].name))
			for path in net.paths_between(source, target):
				print([net.nodes[x].name for x in path])
	if net.number_of_admissible_paths() > 0:
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

	for element in net.nodes_dict:
		start = net.nodes_dict[element]
		print("Neighbours of {}".format(net.nodes[start]))
		for neighbour in net.neighbours_of(start):
			print(net.nodes[neighbour])

