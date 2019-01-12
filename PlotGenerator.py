import matplotlib.pyplot as plt


class PlotGenerator:

    def __init__(self, data):
        self.data = data

    def show_plot(self):
        chosen_data = self.data[0:len(self.data):5]
        x_axis = [i for i in range(0, len(self.data))]
        chosen_x_axis = x_axis[0:len(x_axis):5]
        plt.plot(x_axis, self.data, 'g--')
        plt.plot(chosen_x_axis, chosen_data, 'bo')
        plt.axis([-0.1, len(x_axis), 1000, max(self.data) + 100])

        for x, y in zip(chosen_x_axis, chosen_data):
            plt.annotate("({}, {})".format(x, y), [x, y], xytext=[x + 0.05, y + 0.3])

        plt.ylabel("Koszt")
        plt.xlabel("Numer iteracji")
        plt.show()
