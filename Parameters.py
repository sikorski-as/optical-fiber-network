from enum import IntEnum


class OpticalFibersCapacity(IntEnum):
    L8 = 8
    L16 = 16
    L32 = 32
    L48 = 48
    L64 = 64
    L96 = 96


class Parameters:

    probability_of_crossing_genes = 70  # 0 - 100
    probability_of_mutation = 5

    demand = 170
    # amount_of_chromosomes_usa = 300  # mi
    # amount_of_chromosomes_pol = 400  # mi
    amount_of_chromosomes_ger = 400
    # optical_fiber_capacity_usa = OpticalFibersCapacity.L96
    # optical_fiber_capacity_pol = OpticalFibersCapacity.L32
    optical_fiber_capacity = OpticalFibersCapacity.L48

    transponders_cost = [1, 2, 7]

    number_of_admissible_paths = 2

    amount_of_repetitions = 10
    amount_of_time = 10000
