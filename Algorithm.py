import random
from Chromosome import ChromosomeUtils
from Parameters import Parameters


class Algorithm:
    def __init__(self, chromosomes, network):
        self.chromosomes = chromosomes
        self.network = network
        self.chromosome_utils = ChromosomeUtils()

    def pick_bests_sorted(self, chromosomes, fun, k):
        valued_chromosomes = list()
        for chromosome in chromosomes:
            valued_chromosomes.append([chromosome, fun(chromosome, Parameters.optical_fiber_capacity)])
        valued_chromosomes.sort(key=lambda x: x[1])  # ???
        return [best for best, _ in valued_chromosomes[:k]]

    def pick_bests(self, chromosomes, fun, k):
        valued_chromosomes = list()
        for chromosome in chromosomes:
            valued_chromosomes.append([chromosome, fun(chromosome, Parameters.optical_fiber_capacity)])
        valued_chromosomes.sort(key=lambda x: x[1])  # ???
        best_sorted_chromosomes = [best for best, _ in valued_chromosomes[:k]]
        return [chromosome for chromosome in self.chromosomes if chromosome in best_sorted_chromosomes]

    def algorithm1(self):
        size = len(self.chromosomes) - 1
        i = 0
        while True:
            for j in range(0, size, 2):
                crossed_chromosomes = self.chromosome_utils.cross_chromosomes([self.chromosomes[j], self.chromosomes[j + 1]])
                if random.randrange(1, 101) < 10:
                    a = random.randrange(1, 19)
                    b = random.randrange(a + 1, 20)
                    crossed_chromosomes[0] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[0], [(a, b)])
                if random.randrange(1, 101) < 10:
                    a = random.randrange(1, 19)
                    b = random.randrange(a + 1, 20)
                    crossed_chromosomes[1] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[1], [(a, b)])
                self.chromosomes.append(crossed_chromosomes[0])  # append all?
                self.chromosomes.append(crossed_chromosomes[1])
            self.chromosomes = self.pick_bests(self.chromosomes, self.chromosome_utils.get_network_cost, size + 1, )
            result = self.chromosome_utils.get_network_cost(self.pick_bests_sorted(self.chromosomes, self.chromosome_utils.get_network_cost, 1)[0], Parameters.optical_fiber_capacity)
            print(str(i) + " - " + str(result))
            i += 1
            if result == 0:
                break

        return self.chromosomes

    def algorithm2(self):
        size = len(self.chromosomes) - 1
        i = 0
        last_result = 0
        last_result_counter = 0
        while last_result_counter != 10:
            for j in range(0, size, 2):
                crossed_chromosomes = self.chromosome_utils.cross_chromosomes([self.chromosomes[j], self.chromosomes[j + 1]])
                if random.randrange(1, 101) < 10:
                    a = random.randrange(1, 19)
                    b = random.randrange(a + 1, 20)
                    crossed_chromosomes[0] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[0], [(a, b)])
                if random.randrange(1, 101) < 10:
                    a = random.randrange(1, 19)
                    b = random.randrange(a + 1, 20)
                    crossed_chromosomes[1] = self.chromosome_utils.mutate_chromosome(crossed_chromosomes[1], [(a, b)])
                self.chromosomes.append(crossed_chromosomes[0])  # append all?
                self.chromosomes.append(crossed_chromosomes[1])
            self.chromosomes = self.pick_bests(self.chromosomes, self.chromosome_utils.get_network_transponders_cost, size + 1, )
            result = self.chromosome_utils.get_network_transponders_cost(
                self.pick_bests_sorted(self.chromosomes, self.chromosome_utils.get_network_transponders_cost, 1)[0],
                Parameters.optical_fiber_capacity)
            print(str(i) + " - " + str(result))
            i += 1
            if last_result == result:
                last_result_counter += 1
            else:
                last_result_counter = 0
            last_result = result
        return self.chromosomes
