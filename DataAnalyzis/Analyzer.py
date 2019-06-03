import numpy as np


class DataInfo:
    """
        transponders -> key - int, value -> (x, y) x - bitrate, y - slices used
        vertices -> amount of cities
    """

    def __init__(self, file):
        self.demand = 450
        self.transponders = {1: (40, 2), 2: (100, 3), 3: (200, 4), 4: (400, 6)}
        self.number_of_slices = 768
        self.number_of_paths = 3
        self.vertices = 12
        self.file = file
        self.matrix = ([[[np.zeros((self.number_of_slices, self.vertices), dtype=int) for k in range(0, self.number_of_paths)] for j in range(0, self.vertices)] for
        i in range(0, len(self.transponders.keys()))])

    def skip_line(self):
            self.file.readline()

    def upload_data(self):
        for i in range(0, len(self.transponders.keys())):
            for j in range(0, self.vertices):
                for k in range(0, self.number_of_paths):
                    self.skip_line()
                    self.skip_line()
                    for l in range(0, self.number_of_slices):
                        row = self.file.readline().split()
                        self.matrix[i][j][k][l] = row[1:]
                    self.skip_line()

    def statistics(self):
        for i in range(0, len(self.transponders.keys())):
            for j in range(0, self.vertices):
                for k in range(0, self.number_of_paths):
                    print(f"{i}:{j}:{k} -> {self.matrix[i][j][k].sum()}")


if __name__ == '__main__':
    with open("wyn_450.out") as file:
        data_info = DataInfo(file)
        data_info.upload_data()
        data_info.statistics()
