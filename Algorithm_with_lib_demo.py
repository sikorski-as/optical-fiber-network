from GeneticAlg import creator, crossover, mutation, toolkit
from Chromosome import Chromosome, ChromosomeCreator, ChromosomeUtils
import Network
import Parameters
from pprint import pprint

def test():

    network = Network.Network.load_from_file('Resources/net-pl.xml', structure=True, demands=True, admissible_paths=Parameters.Parameters.number_of_adm_paths_pol)

    pop_size = Parameters.Parameters.amount_of_chromosomes_pol
    crt = creator.Creator(ChromosomeUtils.generate_chromosome_pol_170)
    chromosomes = crt.create(pop_size, network)
    # chromosome = initial_pop[0]
    # pprint(chromosome.__dict__)
    tools = toolkit.Toolkit()
    tools.set_fitness_weights(weights=(-1.0,))
    individuals = tools.create_individuals(chromosomes)
    tools.calculate_fitness_values(individuals, [ChromosomeUtils.get_network_transponders_configuration_cost])
    # individual = individuals[0]
    best = tools.select_best(individuals, 1)
    iteration = 0
    pprint(f"{iteration}. {best}")

    while iteration < 100:
        couples = tools.create_couples(individuals, 2, int(pop_size / 2), select_function=toolkit.Toolkit.select_linear)
        cr = crossover.Crossover(Parameters.Parameters.probability_of_crossing_genes)
        offspring = cr.cross(couples, ChromosomeUtils.cross_chromosomes)
        mut = mutation.Mutation(Parameters.Parameters.probability_of_mutation)
        mut.mutate(offspring, ChromosomeUtils.mutate_chromosome_legit)
        tools.calculate_fitness_values(offspring, [ChromosomeUtils.get_network_transponders_configuration_cost])
        individuals = tools.select_best(individuals + offspring, pop_size)
        best = tools.select_best(individuals, 1)
        iteration += 1
        pprint(f"{iteration}. {best}")
