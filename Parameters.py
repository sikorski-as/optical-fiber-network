from enum import IntEnum

class OpticalFibersCapacity(IntEnum):
    L8 = 8
    L16 = 16
    L32 = 32
    L64 = 64
    L96 = 96

class Parameters:
    number_of_adm_paths_to_choose_from = 10
    probability_of_crossing_genes = 40  # 0 - 100
    amount_of_chromosomes_usa = 200  # mi
    amount_of_chromosomes_pol = 1000  # mi
    optical_fiber_capacity_usa = OpticalFibersCapacity.L96
    optical_fiber_capacity_pol = OpticalFibersCapacity.L32

