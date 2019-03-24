from enum import IntEnum


class OpticalFibersCapacity(IntEnum):
    L8 = 8
    L16 = 16
    L32 = 32
    L64 = 64
    L96 = 96


class Parameters:
    number_of_adm_paths_to_choose_from = 3 #czy wybierac z puli czy brac n najkrótszych???

    probability_of_crossing_genes = 50  # 0 - 100
    probability_of_mutation = 10

    amount_of_chromosomes_usa = 300  # mi
    amount_of_chromosomes_pol = 400  # mi

    optical_fiber_capacity_usa = OpticalFibersCapacity.L96
    optical_fiber_capacity_pol = OpticalFibersCapacity.L32
    optical_fiber_capacity = OpticalFibersCapacity.L32

    transponders_cost = [1, 2, 7]

    number_of_adm_paths_usa = 3
    number_of_adm_paths_pol = 3

    amount_of_repetitions = 1000
    amount_of_time = 100
