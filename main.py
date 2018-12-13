import Network
from Chromosome import ChromosomeCreator
from Chromosome import ChromosomeUtils
from Algorithm import OpticalFibersCapacity
from Algorithm import Parameters


def example():
	network = Network.generate_network_with_admissible_paths(Parameters.number_of_adm_paths_to_choose_from,
															 'Resources/net-us.xml')

	chromosome_creator = ChromosomeCreator()
	chromosome_utils = ChromosomeUtils()

	chromosomes = chromosome_creator.generate_chromosomes(network, Parameters.amount_of_chromosomes)

	for chromosome in chromosomes:
		print(chromosome_utils.get_network_cost(chromosome, OpticalFibersCapacity.L8))

	chr = chromosomes[0]
	chr2 = chromosomes[1]
	pair = (chr, chr2)

	chromosome_utils.cross_chromosomes((chr, chr2))
	loci = [(0, 3), (0, 20), (0, 8), (1, 20), (2, 15), (20, 22)]
	chromosome_utils.cross_chromosomes2(pair, loci)

	print(chromosome_utils.get_network_cost(chr, OpticalFibersCapacity.L8))
	print(chromosome_utils.get_network_cost(chr2, OpticalFibersCapacity.L8))


def main():
	example()


if __name__ == '__main__':
	main()

