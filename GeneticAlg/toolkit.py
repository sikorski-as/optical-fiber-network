import random
import numpy.random


class Toolkit:

    def __init__(self):
        self.weights = tuple()

    def set_fitness_weights(self, weights: 'tuple of floats'):
        """
            Setting fitness weights:
                <0 -> minimize

                >=0 -> maximize

            Attributes:
                weights: tuple of floats
        """

        if type(weights) is tuple:
            for element in weights:
                if type(element) is not float:
                    raise TypeError('All weights must be floats!')

            self.weights = weights
        else:
            raise TypeError('Weights must be passed in tuple!')

    @staticmethod
    def create_individuals(chromosomes):
        """
            List of objects is converted to list of 'individuals'
            Attributes:
                chromosomes: list of objects
            Returns:
                list of individuals
                [(object, fitval_1, fitval_2, ...), ...]
            Raises:
                TypeError if chromosomes are not stored in list
        """

        if type(chromosomes) is list:
            return [Individual(chromosome) for chromosome in chromosomes]
        else:
            raise TypeError('Chromosomes should be passed in list!')

    def calculate_fitness_values(self, individuals: list, list_of_funcs, list_of_attributes=None):
        """
            Modifying existing population, not creating new one.
            If there is no list_of_attributes then chromosome is passed to function.
            If k is greater than len of individuals then list of individuals is returned.
            Attributes:
                individuals: list of individuals
                list_of_attributes: list of attributes used to calculate fitness value
                list_of_funcs: list if functions used to calculate fitness value
            Raises:
                TypeError: when attributes are not stored in a list
                ValueError: when the amount of elements in list_of_funcs is not equal list of weights
        """

        if type(individuals) is not list:
            raise TypeError('Individuals should be stored in a list!')
        if type(list_of_funcs) is not list:
            raise TypeError('Fitness functions should be stored in a list!')
        if list_of_attributes is not None and type(list_of_attributes) is not list:
            raise TypeError('Attributes should be stored in list!')
        if len(list_of_funcs) != len(self.weights):
            raise ValueError('Amount of functions should be equal amount of weights!')

        if list_of_attributes is not None and len(list_of_attributes) < len(self.weights):
            list_of_attributes += [list_of_attributes[-1] for _ in
                                   range(0, len(self.weights) - len(list_of_attributes))]
        if list_of_attributes is None:
            for individual in individuals:
                individual.values = tuple(func(individual.chromosome) for func in list_of_funcs)
        else:
            for individual in individuals:
                individual.values = tuple(func(getattr(individual.chromosome, attribute)) for func, attribute in
                                          zip(list_of_funcs, list_of_attributes))

    @staticmethod
    def select_random(individuals: list, k: int):
        """
            Attributes:
                individuals: list of individuals
                k: amount of individuals to be picked
            Returns:
                list of individuals
        """

        return random.sample(individuals, k)

    def select_best(self, individuals: list, k: int, key=0):
        """
            Picks best k individuals
            Attributes:
                individuals: list of individuals
                k: amount of individuals to be picked
                key: determines which fitness value should be used
            Locals:
                should_reverse: determines if function is minimizing or maximizing fitness value
            Returns:
                list of picked individuals
        """
        should_reverse = False
        if self.weights[key] >= 0:
            should_reverse = True

        if k == 1:
            if should_reverse:
                return max(individuals, key=lambda x: x.values[key])
            else:
                return min(individuals, key=lambda x: x.values[key])

        return sorted(individuals, key=lambda x: x.values[key], reverse=should_reverse)[:k]

    def select_worst(self, individuals: list, k: int, key=0):
        """
            Picks worst k individuals
            Attributes:
                individuals: list of individuals
                k: amount of individuals to be picked
                key: determines which fitness value should be used
            Locals:
                should_reverse: determines if function is minimizing or maximizing fitness value
            Returns:
                list of picked individuals
        """
        should_reverse = False
        if self.weights[key] >= 0:
            should_reverse = True

        return sorted(individuals, key=lambda x: x.values[key], reverse=should_reverse)[:k]

    def select_roulette(self, individuals: list, k: int, key=0, replacement: bool=False):
        """
            Picks k individuals using roulette method
            https://en.wikipedia.org/wiki/Fitness_proportionate_selection
            It is possible that in a return list there will be duplications of individuals!
            Works only with maximising problem!
            Attributes:
                individuals: list of individuals
                k: amount of individuals to be picked
                key: determines which fitness value should be used
                replacement: determines if individual can be chosen more than once
            Locals:
                sum_fitness: sum of all fitness values considering key
                probabilities: list of probabilities of individuals
            Returns:
                list of picked individuals
        """
        if self.weights[key] < 0:
            raise ValueError('Roulette selection works only with maximising problem!')
        else:
            sum_fitness = sum(ind.values[key] for ind in individuals)
            probabilities = [ind.values[key] / sum_fitness for ind in individuals]

        return numpy.random.choice(individuals, k, replace=replacement, p=probabilities).tolist()

    def select_linear(self, individuals: list, k: int, key=0, replacement: bool=False):
        """
            Picks k individuals using linear rank selection
            It is possible that in a return list there will be duplications of individuals!
            Attributes:
                individuals: list of individuals
                k: amount of individuals to be picked
                key: determines which fitness value should be used
                replacement: determines if individual can be chosen more than once
            Locals:
                probabilities: list of probabilities of individuals
                _sum: sum from 1 to n, used to calculate probability
            Returns:
                list of picked individuals
        """
        if self.weights[key] >= 0:
            sorted_individuals = sorted(individuals, reverse=True, key=lambda x: x.values[key])
        else:
            sorted_individuals = sorted(individuals, key=lambda x: x.values[key])
        n = len(sorted_individuals)
        _sum = (1 + n) * n / 2
        probabilities = [i / _sum for i in range(n, 0, -1)]

        return numpy.random.choice(sorted_individuals, k, replace=replacement, p=probabilities).tolist()

    def select_tournament(self, individuals: list, k: int, n: int=2, key=0, replacement: bool=False):
        """
            Picks k individuals using tournament selection
            In each tournament the best individual is picked.
            It is possible that in a return list there will be duplications of individuals!
            Attributes:
                individuals: list of individuals
                k: amount of individuals to be picked
                n: amount of individuals which will take part in each tournament
                key: determines which fitness value should be used
                replacement: determines if individual can be chosen more than once
            Locals:
                chosen: list of picked individuals
            Returns:
                list of picked individuals
        """
        if not replacement and len(individuals) < k:
            raise ValueError('Not enough individuals to pick without replacement!')

        chosen = []
        if replacement:
            for i in range(0, k):
                players = numpy.random.choice(individuals, n).tolist()
                if self.weights[key] >= 0:
                    winner = players[players.index(max(players, key=lambda x: x.values[key]))]
                else:
                    winner = players[players.index(min(players, key=lambda x: x.values[key]))]
                chosen.append(winner)
        else:
            not_picked_individuals = list.copy(individuals)
            for i in range(0, k):
                players = numpy.random.choice(not_picked_individuals, n).tolist()
                if self.weights[key] >= 0:
                    winner_index = players.index(max(players, key=lambda x: x.values[key]))
                    winner = not_picked_individuals[winner_index]
                else:
                    winner_index = players.index(min(players, key=lambda x: x.values[key]))
                    winner = not_picked_individuals[winner_index]
                not_picked_individuals.remove(winner)
                chosen.append(winner)

        return chosen

    @staticmethod
    def create_couples(individuals: list, size: int, length: int, key: int=None, select_function=None, replacement: bool=False):
        """
            Creates list of tuples where one tuple is a 'couple'. If key is None then algorithm packs
            individuals in tuples in order they are stored in a list. If key is chosen then individuals are
            picked using method passed in 'select_function' algorithm.
            Attributes:
                individuals: list of individuals
                size: size of a 'couple'
                length: amount of 'couples'
                replacement: determines if individual can be chosen more than once
                key: determines which fitness value should be used
                select_function: function used in selection of individuals
            Locals:

            Returns:
                list of couples [(1,2,3..),()..]
        """
        if key is not None and select_function is None:
            raise ValueError('You need to pass function which will be used in selection!')

        if not replacement or key is None:
            if size * length > len(individuals):
                raise ValueError('There is not enough individuals to choose without replacement!')

        if key is None:
            couples = [tuple(individuals[begin:begin + size]) for begin in range(0, length * size, size)]
        elif replacement:
            list_with_replacements = select_function(individuals, size * length, key=key, replacement=True)
            couples = [tuple(list_with_replacements[begin:begin + size]) for begin in range(0, length * size, size)]
        else:
            list_without_replacements = select_function(individuals, size * length, key=key)
            couples = [tuple(list_without_replacements[begin:begin + size]) for begin in range(0, length * size, size)]

        return couples


class Individual:

    def __init__(self, chromosome=None):
        self.chromosome = chromosome
        self.values = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<{} {} {}>".format(self.chromosome, self.values[0], self.__hash__())
        #return "<{}>".format(self.values[0])

