from enum import IntEnum


class Algorithm:
    def __init__(self, chromosomes, network):
        self.chromosomes = chromosomes
        self.network = network


class Parameters:
    number_of_adm_paths_to_choose_from = 10
    probability_of_crossing_genes = 50  # 0 - 100
    amount_of_chromosomes = 2  # mi


class OpticalFibersCapacity(IntEnum):
    L8 = 8
    L16 = 16
    L32 = 32
    L64 = 64
    L96 = 96
