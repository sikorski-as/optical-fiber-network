from matplotlib import pyplot

import Network
import random
from PlotGenerator import PlotGenerator
from Chromosome import ChromosomeCreator, Chromosome
from Chromosome import ChromosomeUtils
from Parameters import Parameters, OpticalFibersCapacity
from Algorithm import Algorithm
import Algorithm_with_lib_demo
import ast
import json


def usa_90():
    print("Problem minimalizacji kosztu dla sieci amerykanskiej z 2 sieczkami predefiniowanymi i 90 demand na kazdym")
    print("Chromosomy: " + str(Parameters.amount_of_chromosomes_usa))
    print("Przepustowosc: " + str(OpticalFibersCapacity.L96.value))
    network = Network.Network.generate_network_with_admissible_paths('Resources/net-us.xml')
    chromosome_creator = ChromosomeCreator()
    chromosome_utils = ChromosomeUtils()
    chromosomes = chromosome_creator.generate_chromosomes_usa_90(network, Parameters.amount_of_chromosomes_usa)

    # algorithm = Algorithm(chromosomes, network)
    # chromosomes = algorithm.pick_bests(chromosomes, chromosome_utils.get_network_transponders_cost,
    #                                    Parameters.amount_of_chromosomes_usa, Parameters.optical_fiber_capacity_usa)
    algorithm = Algorithm(chromosomes, network)
    chromosomes = algorithm.algorithm_usa_90(Parameters.optical_fiber_capacity_usa)

    print(algorithm.results)
    plot_gen = PlotGenerator([[algorithm.results, 'g--']])
    plot_gen.show_plot()

    best_chromosome = algorithm.pick_bests_sorted(chromosomes, chromosome_utils.get_network_transponders_configuration_cost, 1,
                                                  Parameters.optical_fiber_capacity_usa)[0]
    for key in sorted(best_chromosome.paths_dict):
        print("{} -> ".format(key))
        for demand, path, transponders in zip(best_chromosome.paths_demand[key], best_chromosome.paths_dict[key],
                                              best_chromosome.transponders_used[key]):
            print("{} {}".format(demand, chromosome_utils.get_transponders_configuration_cost(transponders)), end="")
            print("{} {} ".format(path, transponders))
        print()

    t1, t2, t3 = 0, 0, 0
    for key in sorted(best_chromosome.paths_dict):
        for transponders in best_chromosome.transponders_used[key]:
            t1 += transponders[0]
            t2 += transponders[1]
            t3 += transponders[2]
    print("10:{} 40:{} 100:{}".format(t1*2, t2*2, t3*2))

    return algorithm.results, algorithm.time_elapsed, best_chromosome


def pol_170():
    print("Problem minimalizaji kosztu dla sieci polskiej")
    print("Chromosomy: " + str(Parameters.amount_of_chromosomes_pol))
    print("Przepustowosc: " + str(OpticalFibersCapacity.L32.value))

    network = Network.Network.load_from_file('Resources/net-pl.xml', structure=True, demands=True, admissible_paths=Parameters.number_of_admissible_paths)
    chromosome_creator = ChromosomeCreator()
    chromosome_utils = ChromosomeUtils()
    chromosomes = chromosome_creator.generate_chromosomes_pol_170(network, 20*Parameters.amount_of_chromosomes_pol)

    algorithm = Algorithm(chromosomes, network)
    chromosomes = algorithm.pick_bests(chromosomes, chromosome_utils.get_network_transponders_configuration_cost,
                                       Parameters.amount_of_chromosomes_pol, Parameters.optical_fiber_capacity_pol)

    algorithm = Algorithm(chromosomes, network)
    chromosomes = algorithm.algorithm_pol_170(Parameters.optical_fiber_capacity_pol)
    print(algorithm.results)
    plot_gen = PlotGenerator([[algorithm.results, 'g--']])
    plot_gen.show_plot()

    best_chromosome = algorithm.pick_bests_sorted(chromosomes, chromosome_utils.get_network_transponders_configuration_cost, 1,
                                                  Parameters.optical_fiber_capacity_pol)[0]
    for key in sorted(best_chromosome.paths_dict):
        print("{} -> ".format(key))
        for demand, path, transponders in zip(best_chromosome.paths_demand[key], best_chromosome.paths_dict[key],
                                              best_chromosome.transponders_used[key]):
            print("{} {}".format(demand, chromosome_utils.get_transponders_configuration_cost(transponders)), end="")
            print("{} {} ".format(path, transponders))
        print()

    t1, t2, t3 = 0, 0, 0

    t4 = sum(t_amount[0] for t_amount in best_chromosome.transponders_used)

    for key in sorted(best_chromosome.paths_dict):

        for transponders in best_chromosome.transponders_used[key]:
            t1 += transponders[0]
            t2 += transponders[1]
            t3 += transponders[2]
    print("10:{} 40:{} 100:{}".format(t1*2, t2*2, t3*2))
    print(t4)
    return algorithm.results, algorithm.time_elapsed, best_chromosome


def konwertuj_klucze_do_stringa(dictionary):
    new_dict = dict()
    for k, v in dictionary.items:
        new_dict[str(k)] = v

    return new_dict


def wczytaj_chromosom_do_pliku(chromosome, name):

    file = open("wyniki/{}_transponders.txt".format(name), "w")
    converted_transponders_dict = konwertuj_klucze_do_stringa(chromosome.transponders_used)
    file.write(json.dumps(converted_transponders_dict))
    file.close()
    file = open("wyniki/{}_demands.txt".format(name), "w")
    converted_demand_dict = konwertuj_klucze_do_stringa(chromosome.paths_demand)
    file.write(json.dumps(converted_demand_dict))
    file.close()
    file = open("wyniki/{}_paths.txt".format(name), "w")
    converted_paths = konwertuj_klucze_do_stringa(chromosome.paths_dict)
    file.write(json.dumps(converted_paths))
    file.close()


def wczytywanie_do_pliku(data, name):

    results, time, _ = data
    file = open("wyniki/{}_score.txt".format(name), "w")
    file.write(str(results))
    file = open("wyniki/{}_time.txt".format(name), "w")
    file.write(str(time))


def wczytaj_z_pliku(name):
    new_dict = dict()
    file = open(name, "r")
    data = json.loads(file.read())

    for k, v in zip(data.keys(), data.values()):
        a, b = k[1:len(k)-1].replace(" ", "").split(",")
        a, b = int(a), int(b)
        new_dict[(a, b)] = v

    return new_dict


def test_lib():
    Algorithm_with_lib_demo.test("1.nobel-germany-2-48-170")


def wczytaj_dane():
    with open("1.nobel-germany-2-48-170", 'rb') as file:
        import pickle
        score = pickle.load(file)
        timestamp = pickle.load(file)
        print(f"{score} \n{timestamp}")

    PlotGenerator.show_plot(timestamp, score, 'r--')


if __name__ == '__main__':
    test_lib()
    # wczytaj_dane()
