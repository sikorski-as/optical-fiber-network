import random
from Chromosome import ChromosomeUtils
from Parameters import Parameters, OpticalFibersCapacity


class Algorithm:
    def __init__(self, chromosomes, network):
        self.chromosomes = chromosomes
        self.network = network
        self.chromosome_utils = ChromosomeUtils()
        self.results = list()

    def pick_bests_sorted(self, chromosomes, fun, k, capacity):
        valued_chromosomes = list()
        for chromosome in chromosomes:
            valued_chromosomes.append([chromosome, fun(chromosome, capacity)])
        valued_chromosomes.sort(key=lambda x: x[1])  # ???
        return [best for best, _ in valued_chromosomes[:k]]

    def pick_bests(self, chromosomes, fun, k, capacity):
        valued_chromosomes = list()
        for chromosome in chromosomes:
            valued_chromosomes.append([chromosome, fun(chromosome, capacity)])
        valued_chromosomes.sort(key=lambda x: x[1])  # ???
        best_sorted_chromosomes = [best for best, _ in valued_chromosomes[:k]]
        return [chromosome for chromosome in self.chromosomes if chromosome in best_sorted_chromosomes]

    def algorithm1_usa(self):
        size = len(self.chromosomes) - 1
        i = 0
        while True:
            for j in range(0, size, 2):
                crossed_chromosomes = self.chromosome_utils.cross_chromosomes(
                    [self.chromosomes[j], self.chromosomes[j + 1]])
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(1, 19)
                    b = random.randrange(a + 1, 20)
                    crossed_chromosomes[0] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[0], [(a, b)])
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(1, 19)
                    b = random.randrange(a + 1, 20)
                    crossed_chromosomes[1] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[1], [(a, b)])
                self.chromosomes.append(crossed_chromosomes[0])  # append all?
                self.chromosomes.append(crossed_chromosomes[1])
            self.chromosomes = self.pick_bests(self.chromosomes, self.chromosome_utils.get_network_cost_100, size + 1,
                                               Parameters.optical_fiber_capacity_usa)
            result = self.chromosome_utils.get_network_cost_100(self.pick_bests_sorted(self.chromosomes,
                                                                                       self.chromosome_utils.get_network_cost_100,
                                                                                       1,
                                                                                       Parameters.optical_fiber_capacity_usa)[
                                                                    0], Parameters.optical_fiber_capacity_usa)
            print(str(i) + " - " + str(result))
            self.results.append(result)
            i += 1
            if result == 0:
                break

        return self.chromosomes

    def algorithm1_pol(self):
        size = len(self.chromosomes) - 1
        i = 0
        while True:
            for j in range(0, size, 2):
                crossed_chromosomes = self.chromosome_utils.cross_chromosomes(
                    [self.chromosomes[j], self.chromosomes[j + 1]])
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(0, 11)
                    b = random.randrange(a + 1, 12)
                    crossed_chromosomes[0] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[0], [(a, b)])
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(0, 11)
                    b = random.randrange(a + 1, 12)
                    crossed_chromosomes[1] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[1], [(a, b)])
                self.chromosomes.append(crossed_chromosomes[0])  # append all?
                self.chromosomes.append(crossed_chromosomes[1])
            self.chromosomes = self.pick_bests(self.chromosomes, self.chromosome_utils.get_network_cost_100, size + 1,
                                               Parameters.optical_fiber_capacity_pol)
            result = self.chromosome_utils.get_network_cost_100(
                self.pick_bests_sorted(self.chromosomes, self.chromosome_utils.get_network_cost_100, 1,
                                       Parameters.optical_fiber_capacity_pol)[0], Parameters.optical_fiber_capacity_pol)
            print(str(i) + " - " + str(result))
            self.results.append(result)
            i += 1
            if result == 0:
                break

        return self.chromosomes

    def algorithm2_pol(self):
        size = len(self.chromosomes) - 1
        i = 0
        last_result = 0
        last_result_counter = 0
        while last_result_counter != 10:
            for j in range(0, size, 2):
                crossed_chromosomes = self.chromosome_utils.cross_chromosomes(
                    [self.chromosomes[j], self.chromosomes[j + 1]])
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(0, 11)
                    b = random.randrange(a + 1, 12)
                    crossed_chromosomes[0] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[0], [(a, b)])
                    # print("mutuje")
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(0, 11)
                    b = random.randrange(a + 1, 12)
                    crossed_chromosomes[1] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[1], [(a, b)])
                    # print("mutuje")
                self.chromosomes.append(crossed_chromosomes[0])
                self.chromosomes.append(crossed_chromosomes[1])
            self.chromosomes = self.pick_bests(self.chromosomes, self.chromosome_utils.get_network_transponders_cost,
                                               size + 1, OpticalFibersCapacity.L96)
            best_chromosome = \
            self.pick_bests_sorted(self.chromosomes, self.chromosome_utils.get_network_transponders_cost, 1,
                                   OpticalFibersCapacity.L96)[0]
            result = self.chromosome_utils.get_network_transponders_cost(best_chromosome, OpticalFibersCapacity.L96)
            result_cost = self.chromosome_utils.get_network_cost(best_chromosome, OpticalFibersCapacity.L96)
            print(str(i) + " - " + str(result) + " - " + str(result_cost))
            self.results.append(result)
            i += 1
            if last_result == result:
                last_result_counter += 1
            else:
                last_result_counter = 0
            last_result = result
        return self.chromosomes

    def algorithm2_usa(self):
        size = len(self.chromosomes) - 1
        i = 0
        last_result = 0
        last_result_counter = 0
        while last_result_counter != 10:
            for j in range(0, size, 2):
                crossed_chromosomes = self.chromosome_utils.cross_chromosomes(
                    [self.chromosomes[j], self.chromosomes[j + 1]])
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(0, 25)
                    b = random.randrange(a + 1, 26)
                    crossed_chromosomes[0] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[0], [(a, b)])
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(0, 25)
                    b = random.randrange(a + 1, 26)
                    crossed_chromosomes[1] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[1], [(a, b)])
                self.chromosomes.append(crossed_chromosomes[0])  # append all?
                self.chromosomes.append(crossed_chromosomes[1])
            self.chromosomes = self.pick_bests(self.chromosomes, self.chromosome_utils.get_network_transponders_cost,
                                               size + 1, OpticalFibersCapacity.L96)
            best_chromosome = \
            self.pick_bests_sorted(self.chromosomes, self.chromosome_utils.get_network_transponders_cost, 1,
                                   OpticalFibersCapacity.L96)[0]
            result = self.chromosome_utils.get_network_transponders_cost(best_chromosome, OpticalFibersCapacity.L96)
            result_cost = self.chromosome_utils.get_network_cost(best_chromosome, OpticalFibersCapacity.L96)
            print(str(i) + " - " + str(result) + " - " + str(result_cost))
            self.results.append(result)
            i += 1
            if last_result == result:
                last_result_counter += 1
            else:
                last_result_counter = 0
            last_result = result
        return self.chromosomes

    def algorithm_pol_170(self, optical_fiber_capacity):
        size = len(self.chromosomes) - 1
        i = 0
        last_result = 0
        last_result_counter = 0
        while last_result_counter != 100:
            for j in range(0, size, 2):
                crossed_chromosomes = self.chromosome_utils.cross_chromosomes(
                    [self.chromosomes[j], self.chromosomes[j + 1]])
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(0, 11)
                    b = random.randrange(a + 1, 12)
                    crossed_chromosomes[0] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[0], [(a, b)])
                    # print("mutuje")
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(0, 11)
                    b = random.randrange(a + 1, 12)
                    crossed_chromosomes[1] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[1], [(a, b)])
                    # print("mutuje")
                self.chromosomes.append(crossed_chromosomes[0])
                self.chromosomes.append(crossed_chromosomes[1])
            self.chromosomes = self.pick_bests(self.chromosomes, self.chromosome_utils.get_network_transponders_configuration_cost,
                                               size + 1, optical_fiber_capacity)
            best_chromosome = \
            self.pick_bests_sorted(self.chromosomes, self.chromosome_utils.get_network_transponders_configuration_cost, 1,
                                   optical_fiber_capacity)[0]
            result = self.chromosome_utils.get_network_transponders_configuration_cost(best_chromosome, optical_fiber_capacity)
            result_cost = self.chromosome_utils.get_network_cost_transponders(best_chromosome, optical_fiber_capacity)
            print(str(i) + " - " + str(result) + " - " + str(result_cost))
            self.results.append(result)
            i += 1
            if last_result == result:
                last_result_counter += 1
            else:
                last_result_counter = 0
            last_result = result
        return self.chromosomes

    def algorithm_usa_90(self, optical_fiber_capacity):
        size = len(self.chromosomes) - 1
        i = 0
        last_result = 0
        last_result_counter = 0
        while last_result_counter != 1:
            for j in range(0, size, 2):
                crossed_chromosomes = self.chromosome_utils.cross_chromosomes(
                    [self.chromosomes[j], self.chromosomes[j + 1]])
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(0, 25)
                    b = random.randrange(a + 1, 26)
                    crossed_chromosomes[0] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[0], [(a, b)])
                    # print("mutuje")
                if random.randrange(1, 101) < Parameters.probability_of_mutation:
                    a = random.randrange(0, 25)
                    b = random.randrange(a + 1, 26)
                    crossed_chromosomes[1] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[1], [(a, b)])
                    # print("mutuje")
                self.chromosomes.append(crossed_chromosomes[0])
                self.chromosomes.append(crossed_chromosomes[1])
            self.chromosomes = self.pick_bests(self.chromosomes, self.chromosome_utils.get_network_transponders_configuration_cost,
                                               size + 1, optical_fiber_capacity)
            best_chromosome = \
            self.pick_bests_sorted(self.chromosomes, self.chromosome_utils.get_network_transponders_configuration_cost, 1,
                                   optical_fiber_capacity)[0]
            result = self.chromosome_utils.get_network_transponders_configuration_cost(best_chromosome, optical_fiber_capacity)
            result_cost = self.chromosome_utils.get_network_cost_transponders(best_chromosome, optical_fiber_capacity)
            print(str(i) + " - " + str(result) + " - " + str(result_cost))
            self.results.append(result)
            i += 1
            if last_result == result:
                last_result_counter += 1
            else:
                last_result_counter = 0
            last_result = result
        return self.chromosomes
