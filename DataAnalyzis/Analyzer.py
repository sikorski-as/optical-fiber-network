from pprint import pprint

import numpy as np


class DataInfo:
    """
        transponders -> key - int, value -> (x, y) x - bitrate, y - slices used
        number_of_vertices -> amount of cities
    """

    def __init__(self, result_file, paths_file):
        self.demand = 450
        self.transponders = {1: (40, 2), 2: (100, 3), 3: (200, 4), 4: (400, 6)}
        self.number_of_slices = 768
        self.number_of_paths = 3
        self.number_of_vertices = 12
        self.number_of_edges = 18
        self.file = result_file
        self.paths_file = paths_file
        self.paths_dict = {(i, j): [list() for _ in range(0, self.number_of_paths)] for i in range(0, self.number_of_vertices) for j in range(0, self.number_of_vertices) if i != j}
        self.matrix = ([[[np.zeros((self.number_of_slices, self.number_of_vertices), dtype=int) for k in range(0, self.number_of_paths)] for j in range(0, self.number_of_vertices)] for
        i in range(0, len(self.transponders.keys()))])

    def skip_line(self):
            self.file.readline()

    def upload_data(self):
        for i in range(0, len(self.transponders.keys())):
            for j in range(0, self.number_of_vertices):
                for k in range(0, self.number_of_paths):
                    self.skip_line()
                    self.skip_line()
                    for l in range(0, self.number_of_slices):
                        row = self.file.readline().split()
                        self.matrix[i][j][k][l] = row[1:]
                    self.skip_line()

    def statistics(self):
        for i in range(0, len(self.transponders.keys())):
            for j in range(0, self.number_of_vertices):
                for k in range(0, self.number_of_paths):
                    print(f"{i}:{j}:{k} -> {self.matrix[i][j][k].sum()}")

    def upload_paths(self):
        self.paths_file.readline()
        for _ in range(0, self.number_of_edges):
            for _ in range(0, self.number_of_paths):
                for _ in range(0, self.number_of_vertices):
                    vertice, path, edge, *row = self.paths_file.readline().split()
                    vertice_number, path_number, edge_number = int(vertice), int(path), int(edge)
                    for i, result in enumerate(row, start=0):
                        if result == '1':
                            key = (vertice_number - 1, i)
                            self.paths_dict[key][path_number - 1].append(edge_number)
                self.paths_file.readline()
            self.paths_file.readline()
        pprint(self.paths_dict)


if __name__ == '__main__':

    with open("wyn_450.out") as file:
        with open("450.dat") as path_file:
            data_info = DataInfo(result_file=file, paths_file=path_file)
            data_info.upload_data()
            data_info.statistics()
            data_info.upload_paths()
