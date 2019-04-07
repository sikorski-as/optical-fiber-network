import matplotlib.pyplot as plt


class PlotGenerator:

    def __init__(self, data): #list of datas with designs
        self.data = data

    @staticmethod
    def show_plot(y, x, design):

        plt.plot(y, x, design)
        for x, y in zip(y[::20], x[::20]):
            plt.annotate("({}, {})".format(x, y), [x, y], xytext=[x + 0.05, y + 0.9])
        plt.ylabel("Cost")
        plt.xlabel("Time")
        plt.show()
