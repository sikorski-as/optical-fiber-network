import unittest
from GeneticAlg import creator


class Test:
    val = 5

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class TestCreatorMethods(unittest.TestCase):

    def setUp(self):
        self.crt = creator.Creator(Test)

    def test_init_when_passing_wrong_val(self):
        with self.assertRaises(TypeError):
            creator.Creator("a")

    def test_init_when_correct_class(self):
        self.assertEqual(self.crt.chromosome.val, Test.val)

    def test_amount_of_created_elements(self):
        values = self.crt.create(4, "1", "2", "3")
        self.assertEqual(4, len(values))

    def test_passing_kwargs_when_creating_elements(self):
        values = self.crt.create(1, a=1, b=2, c=3)
        self.assertEqual(values[0].a, 1)
        self.assertEqual(values[0].b, 2)
        self.assertEqual(values[0].c, 3)

    def test_passing_args_when_creating_elements(self):
        values = self.crt.create(1, 1, 2, 3)
        self.assertEqual(values[0].a, 1)
        self.assertEqual(values[0].b, 2)
        self.assertEqual(values[0].c, 3)


if __name__ == '__main__':
    unittest.main()
