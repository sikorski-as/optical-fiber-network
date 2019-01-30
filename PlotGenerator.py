import matplotlib.pyplot as plt


class PlotGenerator:

    def __init__(self, data): #list of datas with designs
        self.data = data

    @staticmethod
    def add_data_to_plot(data, design):
        chosen_data = data[0:len(data):20] + list([data[len(data) - 1]])
        x_axis = [i for i in range(0, len(data))]
        chosen_x_axis = x_axis[0:len(x_axis):20] + list([len(x_axis) - 1])
        plt.plot(x_axis, data, design)
        plt.plot(chosen_x_axis, chosen_data, 'bo')
        plt.axis([-0.1, len(x_axis), min(data) - 100, max(data) + 100])

        for x, y in zip(chosen_x_axis, chosen_data):
            plt.annotate("({}, {})".format(x, y), [x, y], xytext=[x + 0.05, y + 0.3])

    def show_plot(self):
        for data, design in self.data:
            self.add_data_to_plot(data, design)

        plt.ylabel("Koszt")
        plt.xlabel("Numer iteracji")
        plt.show()
