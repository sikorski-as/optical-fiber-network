import unittest
from GeneticAlg import toolkit


class Test:
    @staticmethod
    def func(value):
        return value * 2


class TestToolkitMethods(unittest.TestCase):

    def setUp(self):
        self.toolkit = toolkit.Toolkit()
        self.toolkit.set_fitness_weights((1.0,))
        self.individuals = [toolkit.Individual(1), toolkit.Individual(2), toolkit.Individual(3), toolkit.Individual(4)]
        self.toolkit.calculate_fitness_values(self.individuals, [Test.func])

    def test_set_fitness_weights_when_wrong_values(self):
        weights = ("1", 2, 3)
        with self.assertRaises(TypeError):
            self.toolkit.set_fitness_weights(weights)

    def test_set_fitness_weights_when_correct_values(self):
        weights = (1.0, 2.0, 3.0)
        self.toolkit.set_fitness_weights(weights)
        self.assertEqual(weights, self.toolkit.weights)

    def test_creating_individuals(self):
        chromosomes = [1, 2, 3, 4]
        indvs = self.toolkit.create_individuals(chromosomes)
        self.assertEqual(len(indvs), len(chromosomes))

    def test_creating_individuals_with_wrong_chromosomes(self):
        chromosomes = (1, 2, 3, 4)
        with self.assertRaises(TypeError):
            self.toolkit.create_individuals(chromosomes)

    def test_calculating_fitness_values_with_bad_stored_individuals(self):
        indvs = (toolkit.Individual(1), toolkit.Individual(2))
        with self.assertRaises(TypeError):
            self.toolkit.calculate_fitness_values(indvs, [Test.func], ["attributes"])

    def test_calculating_fitness_values_with_bad_stored_attributes(self):
        with self.assertRaises(TypeError):
            self.toolkit.calculate_fitness_values(self.individuals, [Test.func], ("atttribute1", "attribute2"))

    def test_calculating_fitness_values_with_bad_stored_functions(self):
        with self.assertRaises(TypeError):
            self.toolkit.calculate_fitness_values(self.individuals, (Test.func, ), ["atttribute1", "attribute2"])

    def test_selecting_best_max(self):
        self.toolkit.set_fitness_weights((1.0,))
        self.toolkit.calculate_fitness_values(self.individuals, [Test.func])
        best_ind = self.toolkit.select_best(self.individuals, k=1)
        self.assertEqual(4, best_ind.chromosome)

    def test_selecting_best_min(self):
        k = 1
        self.toolkit.set_fitness_weights((-1.0,))
        self.toolkit.calculate_fitness_values(self.individuals, [Test.func])
        best_ind = self.toolkit.select_best(self.individuals, k=k)
        self.assertEqual(k, best_ind.chromosome)

    def test_amount_of_selected_best(self):
        k = 2
        best_inds = self.toolkit.select_best(self.individuals, k=k)
        self.assertEqual(k, len(best_inds))

    def test_selecting_best_when_to_many_chosen(self):
        best_inds = self.toolkit.select_best(self.individuals, k=10)
        self.assertEqual(len(self.individuals), len(best_inds))

    def test_creating_couples_when_there_is_key_and_no_select_function_passed(self):
        with self.assertRaises(ValueError):
            self.toolkit.create_couples(self.individuals, size=2, length=2, key=0)

    def test_creating_couples_when_no_key_and_too_many_couples_to_create(self):
        with self.assertRaises(ValueError):
            self.toolkit.create_couples(self.individuals, size=3, length=100, key=None)

    def test_creating_couples_when_no_replacement_and_too_many_couples(self):
        with self.assertRaises(ValueError):
            self.toolkit.create_couples(self.individuals, size=5, length=100, key=0, replacement=False)

    def test_creating_couples_when_no_key(self):
        length, size = 2, 2
        couples = self.toolkit.create_couples(self.individuals, size=size, length=length, key=None, replacement=False)
        self.assertEqual(length, len(couples))
        self.assertEqual(size, len(couples[0]))

    def test_creating_couples_when_there_is_key(self):
        length, size = 2, 2
        couples = self.toolkit.create_couples(self.individuals, size=size, length=length, key=0,
                                              select_function=self.toolkit.select_worst, replacement=False)
        self.assertEqual(length, len(couples))
        self.assertEqual(size, len(couples[0]))

    def test_select_tournament_when_no_replacement_and_to_many_to_choose(self):
        k, n = 100, 2
        with self.assertRaises(ValueError):
            self.toolkit.select_tournament(self.individuals, k=k, n=n, key=0, replacement=False)

    def test_select_tournament_with_replacement(self):
        k, n = 2, 2
        selected_inds = self.toolkit.select_tournament(self.individuals, k=k, n=n, key=0, replacement=True)
        self.assertEqual(k, len(selected_inds))
