import copy
import itertools
import math
import random
from math import ceil

from Parameters import Parameters
from GeneticAlg import toolkit


class Chromosome:
    """
        Atributes:
            paths_dict: key (x, y), value: list of paths between x and y
    """
    paths_dict = {}

    def __init__(self):
        self.paths_demand = {}  # pair(node1_id, node2_id) -> list of 3 demands, first demand - first path,
        self.transponders_used = {}  # pair(node1_id, node2_id) -> list of 3 lists of transponders_used [0, 2, 0], first configuration - first path,
        # sum of paths demand should be equal demand between two nodes

    def set_paths_demand(self, pair, list_of_demands):
        self.paths_demand[pair] = list_of_demands

    def set_transponders_used(self, pair, transponders_configuration):
        self.transponders_used[pair] = transponders_configuration

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
    transponders_170 = [[i, j, k] for i in range(0, 2) for j in range(0, 6) for k in range(0, 3) if
                        200 >= 10 * i + 40 * j + 100 * k >= 170]
    transponders_90 = [[i, j, k] for i in range(0, 2) for j in range(0, 4) for k in range(0, 2) if
                       120 >= 10 * i + 40 * j + 100 * k >= 90]

    @staticmethod
    def get_network_cost_transponders(chromosome):
        """liczy ile lambd za dużo"""
        edges_waves_used = {}  # (node1_id, node2_id) -> amount of waves used
        cost = 0  # edge 9L, capacity 8L -> cost += 1

        for key in sorted(chromosome.paths_dict):
            for transponders, path in zip(chromosome.transponders_used[key], chromosome.paths_dict[key]):
                waves_used = sum(transponders)
                for edge in ChromosomeUtils.pairwise(path):
                    sorted_edge = tuple(sorted(edge))
                    if edges_waves_used.get(sorted_edge) is None:
                        edges_waves_used[sorted_edge] = waves_used
                    else:
                        edges_waves_used[sorted_edge] += waves_used

        for edge in sorted(edges_waves_used):
            #print("{} - {} -> {}".format(edge, edges_waves_used[edge], edges_waves_used[edge] - optical_fiber_capacity))
            sorted_edge = tuple(sorted(edge))
            if edges_waves_used[sorted_edge] > Parameters.optical_fiber_capacity:
                cost += edges_waves_used[sorted_edge] - Parameters.optical_fiber_capacity
        return cost

    # <editor-fold desc="Description">
    # def get_network_cost_transponders_debug(self, chromosome, optical_fiber_capacity):
    #     edges_waves_used = {}  # (node1_id, node2_id) -> amount of waves used
    #     cost = 0  # edge 9L, capacity 8L -> cost += 1
    #
    #     for key in sorted(chromosome.paths_dict):
    #         for transponders, path in zip(chromosome.transponders_used[key], chromosome.paths_dict[key]):
    #             waves_used = sum(transponders)
    #             for edge in self.pairwise(path):
    #                 sorted_edge = tuple(sorted(edge))
    #                 if edges_waves_used.get(sorted_edge) is None:
    #                     edges_waves_used[sorted_edge] = waves_used
    #                 else:
    #                     edges_waves_used[sorted_edge] += waves_used
    #
    #     for edge in sorted(edges_waves_used):
    #         print("{} - {} -> {}".format(edge, edges_waves_used[edge], edges_waves_used[edge] - optical_fiber_capacity))
    #         sorted_edge = tuple(sorted(edge))
    #         if edges_waves_used[sorted_edge] > optical_fiber_capacity:
    #             cost += edges_waves_used[sorted_edge] - optical_fiber_capacity
    #     return cost

    # def get_network_cost_100(self, chromosome, optical_fiber_capacity):  # taking only 100 transponders to calculate
    #     edges_waves_used = {}  # (node1_id, node2_id) -> amount of waves used
    #     cost = 0  # edge 9L, capacity 8L -> cost += 1
    #
    #     for key in sorted(chromosome.paths_dict):
    #         for demand, path in zip(chromosome.paths_demand[key], chromosome.paths_dict[key]):
    #             waves_used = ceil(demand / 100)
    #             for edge in self.pairwise(path):
    #                 sorted_edge = tuple(sorted(edge))
    #                 if edges_waves_used.get(sorted_edge) is None:
    #                     edges_waves_used[sorted_edge] = waves_used
    #                 else:
    #                     edges_waves_used[sorted_edge] += waves_used
    #
    #     for edge in sorted(edges_waves_used):
    #         # print("{} - {} -> {}".format(edge, edges_waves_used[edge], edges_waves_used[edge] - optical_fiber_capacity))
    #         sorted_edge = tuple(sorted(edge))
    #         if edges_waves_used[sorted_edge] > optical_fiber_capacity:
    #             cost += edges_waves_used[sorted_edge] - optical_fiber_capacity
    #     return cost
    #
    # def get_waves_cost(self, demand):
    #     if demand % 10 != 0:
    #         demand = demand - (demand % 10) + 10
    #     transponder100tmp = math.floor(demand / 100)
    #     demand -= transponder100tmp * 100
    #     transponder10, transponder40, transponder100 = self.ct[demand]
    #     transponder100 += transponder100tmp
    #     cost = transponder10 + transponder40 + transponder100
    #     return cost
    #
    # def get_waves_cost2(self, demand):
    #     if demand % 10 != 0:
    #         demand = demand - (demand % 10) + 10
    #     if demand % 40 == 0 and math.floor(demand / 100) % 2 != 0:
    #         return demand / 40
    #     transponder100tmp = math.floor(demand / 100)
    #     demand -= transponder100tmp * 100
    #     transponder10, transponder40, transponder100 = self.ct2[demand]
    #     transponder100 += transponder100tmp
    #     cost = transponder10 + transponder40 + transponder100
    #     return cost
    #
    # def get_transponders_cost(self, demand):
    #     if demand % 10 != 0:
    #         demand = demand - (demand % 10) + 10
    #     transponder100tmp = math.floor(demand / 100)
    #     demand -= transponder100tmp * 100
    #     transponder10, transponder40, transponder100 = self.ct[demand]
    #     transponder100 += transponder100tmp
    #     cost = transponder10 + 3 * transponder40 + 7 * transponder100
    #     return cost
    #
    # def get_transponders_cost2(self, demand):
    #     if demand % 10 != 0:
    #         demand = demand - (demand % 10) + 10
    #     if demand % 40 == 0 and math.floor(demand / 100) % 2 != 0:
    #         return (demand / 40) * 2
    #     transponder100tmp = math.floor(demand / 100)
    #     demand -= transponder100tmp * 100
    #     transponder10, transponder40, transponder100 = self.ct2[demand]
    #     transponder100 += transponder100tmp
    #     cost = transponder10 + 2 * transponder40 + 5 * transponder100
    #     return cost
    # </editor-fold>

    @staticmethod
    def get_transponders_configuration_cost(transponders_configuration):
        total_cost = 0
        for amount_of_transponders, cost_of_transponder in zip(transponders_configuration, Parameters.transponders_cost):
            total_cost += amount_of_transponders * cost_of_transponder
        return total_cost * 2

    @staticmethod
    def get_network_transponders_configuration_cost(chromosome):
        cost = 0
        for key in sorted(chromosome.paths_dict):
            for transponders in chromosome.transponders_used[key]:
                cost += ChromosomeUtils.get_transponders_configuration_cost(transponders)
        overflow = ChromosomeUtils.get_network_cost_transponders(chromosome)
        if overflow > 0:
            cost += math.pow(overflow, 3) + 1000
        return cost

    @staticmethod
    def pairwise(iterable):  # used in gen_network_cost
        """ s -> (s0,s1), (s1,s2), (s2, s3), ... """
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    @staticmethod
    def cross_chromosomes(pair_of_individuals):
        """ switching genes(chromosome1, chromosome2) -> (new_chromosome_1, new_chromosome_1)
         method -> take gene from ch1 and ch2 then draw if they should be switched or not """
        pair_of_chromosomes = (pair_of_individuals[0].chromosome, pair_of_individuals[1].chromosome)
        if len(pair_of_chromosomes) != 2:
            return

        chromosome_1 = copy.deepcopy(pair_of_chromosomes[0])
        chromosome_2 = copy.deepcopy(pair_of_chromosomes[1])

        for key in chromosome_1.paths_demand:
            if random.randrange(1, 101) < Parameters.probability_of_crossing_genes:
                chromosome_1.paths_demand[key], chromosome_2.paths_demand[key] = \
                    chromosome_2.paths_demand[key], chromosome_1.paths_demand[key]
                chromosome_1.transponders_used[key], chromosome_2.transponders_used[key] = \
                    chromosome_2.transponders_used[key], chromosome_1.transponders_used[key]

        return [toolkit.Individual(chromosome_1), toolkit.Individual(chromosome_2)]

    @staticmethod
    def cross_chromosomes_loci(pair_of_chromosomes, loci):
        """ from 0 to loci[0] not switch then loci[0] - loci[1] switch.. """

        loci = sorted(loci)
        chromosome_1 = copy.deepcopy(pair_of_chromosomes[0])
        chromosome_2 = copy.deepcopy(pair_of_chromosomes[1])

        should_switch_genes = False
        counter = 0

        for key in chromosome_1.paths_demand:
            if should_switch_genes:
                chromosome_1.paths_demand[key], chromosome_2.paths_demand[key] = \
                    chromosome_2.paths_demand[key], chromosome_1.paths_demand[key]
                chromosome_1.transponders_used[key], chromosome_2.transponders_used[key] = \
                    chromosome_2.transponders_used[key], chromosome_1.transponders_used[key]
            if counter < len(loci) and key == loci[counter]:
                should_switch_genes = not should_switch_genes
                counter += 1

        return [chromosome_1, chromosome_2]

    @staticmethod
    def mutate_chromosome(chromosome, pairs):  # chromosome, list of tuples(node1_id, node2_id) -> mutated_chromosome
        mutated_chromosome = chromosome
        for pair in pairs:
            ChromosomeUtils.mutate_gene(mutated_chromosome.paths_demand[pair])
            ChromosomeUtils.mutate_gene(mutated_chromosome.transponders_used[pair])
        return mutated_chromosome

    @staticmethod
    def mutate_chromosome_legit(individual):
        chromosome = individual.chromosome
        for key in chromosome.paths_dict:
            if random.randint(0, 101) < Parameters.probability_of_mutation:
                ChromosomeUtils.mutate_gene(chromosome.paths_demand[key])
                ChromosomeUtils.mutate_gene(chromosome.transponders_used[key])

    @staticmethod
    def mutate_gene(gene):  # take all paths and move right
        n = len(gene)
        new_gene = [0] * n

        for i in range(0, n):
            new_gene[i] = gene[(i - 1) % n]

    @staticmethod
    def generate_chromosome_usa_90(network):
        chromosome = Chromosome()
        chromosome.set_paths_dict(network.paths_dict)
        demand_utils = DemandUtils()

        for pair in sorted(network.paths_dict):
            # demand = network.demands_dict[pair]
            demands, transponders = demand_utils.generate_demands_and_transponders_config_all_in_one(90,
                                                                                                     ChromosomeUtils.transponders_90,
                                                                                                     Parameters.number_of_admissible_paths)
            chromosome.set_paths_demand(pair, demands)
            chromosome.set_transponders_used(pair, transponders)
        return chromosome
    # uogólnić

    @staticmethod
    def generate_chromosome_pol_170(network):
        chromosome = Chromosome()
        chromosome.set_paths_dict(network.paths_dict)
        demand_utils = DemandUtils()
        for pair in sorted(network.demands_dict):
            # demand = network.demands_dict[pair]
            demands, transponders = demand_utils.generate_demands_and_transponders_config_all_in_one(170,
                                                                                                     ChromosomeUtils.transponders_170,
                                                                                                     Parameters.number_of_admissible_paths)
            chromosome.set_paths_demand(pair, demands)
            chromosome.set_transponders_used(pair, transponders)
        return chromosome


class DemandUtils:

    # Zrobić n-elementowe
    @staticmethod
    def generate_random_demands(demand):  # creates 3-el list of demands
        demands = list()
        rand_number = random.randrange(0, demand)
        demands.append(rand_number)
        rand_number = random.randrange(0, demand - rand_number)
        demands.append(rand_number)
        demands.append(int(demand - demands[0] - demands[1]))

        return demands

    @staticmethod
    def generate_random_demands_all_in_one(demand, size):
        demands = [0] * size
        demands[random.randrange(0, size)] = demand

        return demands

    def generate_demands_and_transponders_config_all_in_one(self, demand, transponders_configuration, size):
        chosen_path = random.randrange(0, size)
        demands = [0] * size
        demands[chosen_path] = demand
        transponders_config = [[0, 0, 0]] * size
        transponders_config[chosen_path] = self.choose_transponders_configuration(transponders_configuration)

        return demands, transponders_config

    @staticmethod
    def choose_transponders_configuration(transponders_configurations):
        return random.choice(transponders_configurations)


class ChromosomeCreator:

    def generate_chromosomes_usa_90(self, network, number_of_chromosomes):
        chromosomes = list()
        chromosome_utils = ChromosomeUtils()
        for i in range(0, number_of_chromosomes):
            chromosomes.append(chromosome_utils.generate_chromosome_usa_90(network))

        return chromosomes

    def generate_chromosomes_pol_170(self, network, number_of_chromosomes):
        chromosomes = list()
        chromosome_utils = ChromosomeUtils()
        for i in range(0, number_of_chromosomes):
            chromosomes.append(chromosome_utils.generate_chromosome_pol_170(network))

        return chromosomes
