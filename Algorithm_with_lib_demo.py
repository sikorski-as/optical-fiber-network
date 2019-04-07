from GeneticAlg import creator, crossover, mutation, toolkit
from Chromosome import ChromosomeUtils
import Network
import Parameters
from pprint import pprint
import timer
import statistics


def test(file_to_save):
    data_collector = statistics.DataCollector()
    network = Network.Network.generate_network_with_admissible_paths('Resources/nobel-germany.xml')

    stopwatch = timer.Timer()

    pop_size = Parameters.Parameters.amount_of_chromosomes_ger
    crt = creator.Creator(ChromosomeUtils.generate_chromosome_pol_170)
    chromosomes = crt.create(pop_size, network)
    # pprint(chromosomes[0].paths_demand)
    # pprint(chromosomes[0].transponders_used)
    # pprint(network.paths_dict)

    tools = toolkit.Toolkit()
    tools.set_fitness_weights(weights=(-1.0,))
    individuals = tools.create_individuals(chromosomes)
    tools.calculate_fitness_values(individuals, [ChromosomeUtils.get_network_transponders_configuration_cost])
    best = tools.select_best(individuals, 1)
    iteration = 0
    pprint(f"{iteration}. {best}")

    stopwatch.start()
    while stopwatch.get_interval_of_time_from_start() < Parameters.Parameters.amount_of_time:
        couples = tools.create_couples(individuals, 2, int(pop_size / 2), key=0, select_function=toolkit.Toolkit.select_linear)
        cr = crossover.Crossover(Parameters.Parameters.probability_of_crossing_genes)
        offspring = cr.cross(couples, ChromosomeUtils.cross_chromosomes)
        mut = mutation.Mutation(Parameters.Parameters.probability_of_mutation)
        mut.mutate(offspring, ChromosomeUtils.mutate_chromosome_legit)
        tools.calculate_fitness_values(offspring, [ChromosomeUtils.get_network_transponders_configuration_cost])
        individuals = tools.select_best(individuals + offspring, pop_size)
        best = tools.select_best(individuals, 1)
        iteration += 1
        pprint(f"{iteration}. time: {stopwatch.get_interval_of_time_from_start()} {best} ovf: {ChromosomeUtils.get_network_cost_transponders(best.chromosome)}")
        data_collector.score.append(best.values[0])
        data_collector.timestamp.append(stopwatch.get_interval_of_time_from_start())

    pprint(best.chromosome)
    data_collector.save_data(file_to_save)

