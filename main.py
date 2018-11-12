from Network import *


def main():
	net = Network.load_from_file('Resources/net.xml')

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

		print('Admissible paths between {} and {}:'.format(net.nodes[source].name, net.nodes[target].name))
		for path in net.paths_between(source, target):
			print([net.nodes[x].name for x in path])

	print(net.paths_between(0, 1))
	print(net.paths_between(1, 0))


if __name__ == '__main__':
	main()
