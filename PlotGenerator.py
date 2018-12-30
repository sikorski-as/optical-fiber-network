import matplotlib.pyplot as plt


class PlotGenerator:

    def __init__(self, data):
        self.data = data

    def show_plot(self):
        x_axis = [i for i in range(0, len(self.data))]
        plt.plot(x_axis, self.data, 'g--')
        plt.plot(x_axis, self.data, 'bo')
        plt.axis([-0.1, len(x_axis), -1, max(self.data) + 1])

        for x, y in zip(x_axis, self.data):
            plt.annotate("({}, {})".format(x, y), [x, y], xytext=[x + 0.05, y + 0.3])

        plt.ylabel("Koszt")
        plt.xlabel("Numer iteracji")
        plt.show()
