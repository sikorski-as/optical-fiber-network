import itertools
import random
from math import ceil

from Algorithm import Parameters


class Chromosome:
    def __init__(self):
        self.paths_dict = {}    # pair(node1_id, node2_id) -> list of 3 paths
        self.paths_demand = {}  # pair(node1_id, node2_id) -> list of 3 demands, first demand - first path,
                                # sum of paths demand should be equal demand between two nodes

    def set_paths_demand(self, pair, list_of_demands):
        self.paths_demand[pair] = list_of_demands

    def set_path_demand(self, pair, number_of_path, demand):
        if pair not in self.paths_demand:
            self.paths_demand[pair] = [0] * 3
        self.paths_demand[pair][number_of_path] = demand

    def set_paths_dict(self, another_paths_dict):
        self.paths_dict = another_paths_dict

    def get_path_demand(self, pair, number_of_path):
        return self.paths_demand[pair][number_of_path]

    def get_path(self, pair, number_of_path):
        return self.paths_dict[pair][number_of_path]


class ChromosomeUtils:

    def get_network_cost(self, chromosome, optical_fiber_capacity):     # taking only 100 transponders to calculate
        edges_waves_used = {}     # (node1_id, node2_id) -> amount of waves used
        cost = 0    # edge 9L, capacity 8L -> cost += 1

        for key in sorted(chromosome.paths_dict):
            for demand, path in zip(chromosome.paths_demand[key], chromosome.paths_dict[key]):
                waves_used = ceil(demand / 100)
                for edge in self.pairwise(path):
                    sorted_edge = tuple(sorted(edge))
                    if edges_waves_used.get(sorted_edge) is None:
                        edges_waves_used[sorted_edge] = waves_used
                    else:
                        edges_waves_used[sorted_edge] += waves_used

        for edge in sorted(edges_waves_used):
            # print("{} - {}".format(edge, edges_waves_used[edge]))
            sorted_edge = tuple(sorted(edge))
            if edges_waves_used[sorted_edge] > optical_fiber_capacity:
                cost += edges_waves_used[sorted_edge] - optical_fiber_capacity
        return cost

    @staticmethod
    def pairwise(iterable):     # used in gen_network_cost
        """ s -> (s0,s1), (s1,s2), (s2, s3), ... """
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    @staticmethod
    def cross_chromosomes(pair_of_chromosomes):
        """ switching genes(chromosome1, chromosome2) -> (new_chromosome_1, new_chromosome_1)
         method -> take gene from ch1 and ch2 then draw if they should be switched or not """

        if len(pair_of_chromosomes) != 2:
            return

        chromosome_1 = pair_of_chromosomes[0]
        chromosome_2 = pair_of_chromosomes[1]

        for key in chromosome_1.paths_demand:
            if random.randrange(1, 101) < Parameters.probability_of_crossing_genes:
                tmp = chromosome_1.paths_demand[key]
                chromosome_1.paths_demand[key] = chromosome_2.paths_demand[key]
                chromosome_2.paths_demand[key] = tmp

    @staticmethod
    def cross_chromosomes2(pair_of_chromosomes, loci):
        """ from 0 to loci[0] not switch then loci[0] - loci[1] switch.. """

        loci = sorted(loci)
        chromosome_1 = pair_of_chromosomes[0]
        chromosome_2 = pair_of_chromosomes[1]

        should_switch_genes = False
        counter = 0

        for key in chromosome_1.paths_demand:
            if should_switch_genes:
                tmp = chromosome_1.paths_demand[key]
                chromosome_1.paths_demand[key] = chromosome_2.paths_demand[key]
                chromosome_2.paths_demand[key] = tmp
            if counter < len(loci) and key == loci[counter]:
                should_switch_genes = not should_switch_genes
                counter += 1

    def mutate_chromosome(self, chromosome, pairs):     # chromosome, list of (node1_id, node2_id) -> mutated_chromosome
        mutated_chromosome = chromosome
        for pair in pairs:
            mutated_chromosome.paths_demand[pair] = self.mutate_gene(mutated_chromosome.paths_demand[pair])
        return mutated_chromosome

    @staticmethod
    def mutate_gene(gene):    # take all paths and move right
        n = len(gene)
        new_gene = [0] * n

        for i in range(0, n):
            new_gene[i] = gene[(i - 1) % n]

        return new_gene

    def generate_chromosome(self, network):
        chromosome = Chromosome()
        chromosome.set_paths_dict(network.paths_dict)

        for pair in sorted(network.demands_dict):
            demand = network.demands_dict[pair]
            chromosome.set_paths_demand(pair, self.generate_random_demands(demand))

        return chromosome

    @staticmethod
    def generate_random_demands(demand):  # creates 3-el list of demands
        demands = list()
        rand_number = random.randrange(0, demand)
        demands.append(rand_number)
        rand_number = random.randrange(0, demand - rand_number)
        demands.append(rand_number)
        demands.append(int(demand - demands[0] - demands[1]))

        return demands


class ChromosomeCreator:
    def __init__(self):
        self.chromosomes = list()

    def generate_chromosomes(self, network, number_of_chromosomes):
        chromosome_utils = ChromosomeUtils()

        for i in range(0, number_of_chromosomes):
            self.chromosomes.append(chromosome_utils.generate_chromosome(network))

        return self.chromosomes


