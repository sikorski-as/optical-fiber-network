

class Crossover:

    def __init__(self, crossover_probability: int):
        self.CPB = crossover_probability

    def cross(self, list_of_couples: list, crossover_function):
        """
            Note: crossover function should return list of offspring
            Attributes:
                list_of_couples: list of tuples in which couples are stored
                crossover_function: function used to cross couple, should return list of children
            Returns:
                list of individuals
        """
        offspring = []
        for couple in list_of_couples:
            children = crossover_function(couple)
            offspring += children
        return offspring
