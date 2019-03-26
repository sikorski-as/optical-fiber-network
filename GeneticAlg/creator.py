import inspect


class Creator:

    def __init__(self, object_reference):
        """
            Attributes:
                object_reference: reference to object which will be treated as chromosome
        """
        # if inspect.isclass(object_reference):
        self.chromosome = object_reference
        # else:
        #     raise TypeError('Value should be a reference to a class')

    def create(self, n: int, *args, **kwargs):
        """
            Attributes:
               n: amount of elements to be created
               args, kwargs: arguments to initialize object
            Returns:
               list of objects created using arguments
        """
        print(n, end=" ")
        print(*args, end=" ")
        for key, val in kwargs.items():
            print("{} {}".format(key, val), end=" ")
        print()
        return [self.chromosome(*args, **kwargs) for _ in range(0, n)]
