import Network
from PlotGenerator import PlotGenerator
from Chromosome import ChromosomeCreator
from Chromosome import ChromosomeUtils
from Parameters import Parameters, OpticalFibersCapacity
from Algorithm import Algorithm


def example():
    network = Network.generate_network_with_admissible_paths(Parameters.number_of_adm_paths_to_choose_from,
                                                             'Resources/net-pl.xml')

    chromosome_creator = ChromosomeCreator()
    chromosome_utils = ChromosomeUtils()

    # chromosomes = chromosome_creator.generate_chromosomes_random(network, Parameters.amount_of_chromosomes)
    #
    # for chromosome in chromosomes:
    # 	print(chromosome_utils.get_network_cost(chromosome, OpticalFibersCapacity.L8))
    #
    # chr = chromosomes[0]
    # chr2 = chromosomes[1]
    # pair = (chr, chr2)
    #
    # chromosome_utils.cross_chromosomes((chr, chr2))
    # loci = [(0, 3), (0, 20), (0, 8), (1, 20), (2, 15), (20, 22)]
    # chromosome_utils.cross_chromosomes2(pair, loci)

    #	print(chromosome_utils.get_network_cost(chr, OpticalFibersCapacity.L96))
    #	print(chromosome_utils.get_network_cost(chr2, OpticalFibersCapacity.L96))

    n = 10

    better_chromosome = chromosome_creator.generate_chromosomes_all_in_one(network, n)
    better_chromosome1 = chromosome_creator.generate_chromosomes_random(network, n)


# for key in sorted(better_chromosome[0].paths_dict):
# 	print(key)
# 	for path in better_chromosome[0].paths_dict[key]:
# 		print(path)
# 	print()

# for path in sorted(better_chromosome[0].paths_demand):
# 	cost = 0
# 	for demand in better_chromosome[0].paths_demand[path]:
# 		cost += demand
# 	print("{} - {}".format(path, cost))
#
# print(chromosome_utils.get_network_cost(better_chromosome[0], OpticalFibersCapacity.L96))
# print(chromosome_utils.get_network_cost(better_chromosome[0], OpticalFibersCapacity.L96))

# for chromosome in better_chromosome:
# 	print(chromosome_utils.get_network_cost(chromosome, OpticalFibersCapacity.L96), end=" ")
# print()
# for chromosome in better_chromosome1:
# 	print(chromosome_utils.get_network_cost(chromosome, OpticalFibersCapacity.L96), end=" ")

    plot_gen = PlotGenerator([10, 7, 3, 2, 1, 0])
    plot_gen.show_plot()


def marcin():
    network = Network.generate_network_with_admissible_paths(Parameters.number_of_adm_paths_to_choose_from,
                                                             'Resources/net-us.xml')
    chromosome_creator = ChromosomeCreator()
    chromosome_utils = ChromosomeUtils()
    chromosomes = chromosome_creator.generate_chromosomes_all_in_one(network, Parameters.amount_of_chromosomes)
    algorithm = Algorithm(chromosomes, network)
    chromosomes = algorithm.algorithm1()
    print(algorithm.results)
    plot_gen = PlotGenerator(algorithm.results)
    plot_gen.show_plot()

    for chromosome in chromosomes:
        cost = chromosome_utils.get_network_cost(chromosome, Parameters.optical_fiber_capacity)
        if cost == 0:
            print(cost)
            for key in chromosome.paths_demand:
                for demand in chromosome.paths_demand[key]:
                    print(demand, end=' ')
                print()

            print()


def main():
    marcin()


if __name__ == '__main__':
    main()
