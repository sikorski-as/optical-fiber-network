import unittest
import Network


class NetworkClassTest(unittest.TestCase):
	def test_add_node(self):
		net = Network.Network()

		net.add_node(Network.Node('London'))
		self.assertEqual(net.number_of_nodes(), 1)

		net.add_node(Network.Node('London'))
		self.assertEqual(net.number_of_nodes(), 2)

	def test_add_link(self):
		net = Network.Network()

		london_node_id = net.add_node(Network.Node('London'))
		paris_node_id = net.add_node(Network.Node('Paris'))
		self.assertEqual(net.number_of_nodes(), 2)

		net.add_link((london_node_id, paris_node_id))
		self.assertEqual(net.number_of_links(), 1)

	def test_add_demand(self):
		net = Network.Network()

		london_node_id = net.add_node(Network.Node('London'))
		paris_node_id = net.add_node(Network.Node('Paris'))
		pair = london_node_id, paris_node_id

		self.assertEqual(net.number_of_nodes(), 2)

		net.add_demand(pair, 19.0)
		self.assertEqual(net.demand_of(pair), 19.0)

	def test_are_connected(self):
		net = Network.Network()

		london_node_id = net.add_node(Network.Node('London'))
		paris_node_id = net.add_node(Network.Node('Paris'))
		pair = london_node_id, paris_node_id
		self.assertEqual(net.number_of_nodes(), 2)

		net.add_link((london_node_id, paris_node_id))
		self.assertEqual(net.number_of_links(), 1)
		self.assertTrue(net.are_connected(pair))

	'''
	def test_demand_of(self, first, second):
		pass

	def test_has_admissible_paths(self):
		pass

	def test_paths_between(self, first, second):
		pass

	def test_node_list(self, sequence):
		pass

	def test_index_of(self, node):
		pass

	def test_load_structure(self, filename):
		pass

	def test_load_demands(self, filename, admissible_paths=False):
		pass
	'''


if __name__ == '__main__':
	unittest.main()