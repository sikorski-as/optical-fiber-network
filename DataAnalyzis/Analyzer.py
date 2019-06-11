from pprint import pprint
from collections import defaultdict
import numpy as np
import mapbox
import geomanip
import draw


class DataInfo:
    """
        transponders -> key - int, value -> (x, y) x - bitrate, y - slices used
        number_of_vertices -> amount of cities
    """

    def __init__(self, result_file, paths_file):
        # demanded value, unused
        self.demand = 450

        # transponder type -> (bitrate, used slices)
        self.transponders = {1: (40, 2), 2: (100, 3), 3: (200, 4), 4: (400, 6)}

        # summary number of slices
        self.number_of_slices = 768

        # number of paths per demand
        self.number_of_paths = 3

        # number of nodes in the network
        self.number_of_vertices = 12

        # number of edges in the network
        self.number_of_edges = 18

        # filename with data for X(t, n, n', p, s)
        self.file = result_file

        # filename with paths data
        self.paths_file = paths_file

        vertices_pairs = filter(lambda v: v[0] != v[1], np.ndindex(self.number_of_vertices, self.number_of_vertices))
        self.paths_dict = {verts: [list() for _ in range(self.number_of_paths)] for verts in vertices_pairs}

        shape = (len(self.transponders),    # 0: t  - transponder type
                 self.number_of_vertices,   # 1: n  - node 1
                 self.number_of_vertices,   # 2: n' - node 2
                 self.number_of_paths,      # 3: p  - path
                 self.number_of_slices)     # 4: s  - slice

        self.X = np.zeros(shape=shape, dtype=int)

    def upload_data(self):
        """
        Load X(t, n, n', p, s) data.

        :return: five dimensional X(...) array
        """
        shape = (self.X.shape[0], self.X.shape[1], self.X.shape[3])
        for t, n1, p in np.ndindex(shape):
            self.file.readline()
            self.file.readline()
            for s in range(self.number_of_slices):
                row = self.file.readline().split()
                for n2, x in enumerate(row[1:]):
                    self.X[t, n1, n2, p, s] = int(x)
            self.file.readline()
        return self.X

    def statistics(self):
        for i, j, k in np.ndindex(self.X.shape[0], self.X.shape[1], self.X.shape[3]):
            print(f'{i}:{j}:{k} -> {self.X[i, j, :, k, :].sum()}')

    def upload_path_row(self):
        vertex, path, edge, *row = self.paths_file.readline().split()
        vertex1, path, edge = int(vertex) - 1, int(path) - 1, int(edge)
        for vertex2, result in enumerate(row):
            if int(result):
                self.paths_dict[(vertex1, vertex2)][path].append(edge)

    def upload_paths(self):
        """
        Load paths data.
        
        :return: dictionary of loaded paths (key: tuple of nodes, value: list of paths)
        """
        self.paths_file.readline()
        for _ in range(self.number_of_edges):
            for _ in range(self.number_of_paths):
                for _ in range(self.number_of_vertices):
                    self.upload_path_row()
                self.paths_file.readline()
            self.paths_file.readline()
        return self.paths_dict

    def compute_used_slices(self):
        """
        Compute used slices.

        :return: dictionary of slice usage (key: edge ID, value: used slices)
        """
        slices_in_edges = defaultdict(int)
        for t, n1, n2, p in np.ndindex(self.X.shape[:4]):
            if n1 != n2:
                used_slices = self.X[t, n1, n2, p].sum() * self.transponders[t + 1][1]
                # print(f't={t}, n={n1}, n\'={n2}, p={p}, used_slices={used_slices}')
                for edge in self.paths_dict[(n1, n2)][p]:
                    slices_in_edges[edge] += used_slices
        return slices_in_edges


if __name__ == '__main__':
    # load slices usage data and compute percentage usage
    slice_usage = {}
    with open("wyn_450.out") as file, open("450.dat") as path_file:
        data_info = DataInfo(result_file=file, paths_file=path_file)
        data_info.upload_data()
        data_info.upload_paths()
        slices_in_edges = data_info.compute_used_slices()
        slice_usage = {k: (v / data_info.number_of_slices * 100) for (k, v) in slices_in_edges.items()}
        print('slices in edges:')
        pprint(slices_in_edges)

    # settings for appropriate mercator displaying
    map_data = {
        'style': 'countries_basic',
        'center_long': 19.6153711,
        'center_lati': 52.0892499,
        'zoom': 5,
        'map_width': 1024,
        'map_height': 512,
        'api_token': '<mapbox api token here>'
    }

    cities = {}
    with open('cities.txt') as f:
        for line in f:
            # load name of the city and its degree coordinates
            name, long, lati = line.replace('(', '').replace(')', '').split()

            # convert degree coordinates to pixel coordinates
            x, y = geomanip.get_x(long=float(long), **map_data), geomanip.get_y(lati=float(lati), **map_data)

            # save pixel coordinates of each city
            cities[name] = x, y

    edges = {}
    with open('edges.txt') as f:
        for i, line in enumerate(f, start=1):
            # load names of cities that are end of each edge
            n1, n2 = line.split()[2:4]

            # save pixel coordinates of each edge's end
            edges[i] = cities[n1], cities[n2]

    # print('cities with positions:')
    # pprint(cities)
    # print('edges with positions:')
    # pprint(edges)
    # mapbox.get_map_as_file('map.png', mapdata=map_data)  # download map from the API, needs api_token

    # draw map
    draw.prepare('map.png')

    # draw edges between nodes
    for i, ((x1, y1), (x2, y2)) in enumerate(edges.values(), start=1):
        draw.line(x1, y1, x2, y2, marker='o', color='k')
        sx, sy = (x1 + x2) / 2, (y1 + y2) / 2  # middle point between nodes for annotation
        usage = slice_usage[i]
        draw.text(sx, sy, '{:.2f}% ({})'.format(usage, slices_in_edges[i]),
                  weight='bold',
                  color='red',
                  fontsize=9,
                  horizontalalignment='center')

    # draw city names
    for city_name, (x, y) in cities.items():
        draw.text(x, y - 10, city_name[:2],
                  weight='bold',
                  color='white',
                  fontsize=12,
                  horizontalalignment='center',
                  effects={'linewidth': 1, 'foreground': 'black'})
    draw.show()
