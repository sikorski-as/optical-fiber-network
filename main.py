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


if __name__ == '__main__':
	main()
