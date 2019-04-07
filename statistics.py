import Parameters
import pickle


def get_amount_of_transponder_used(transponders_used):

    amount_of_transponder_types = len(Parameters.Parameters.transponders_cost)
    return [sum(t_list[i] for t in transponders_used.values() for t_list in t) for i in range(amount_of_transponder_types)]


class DataCollector:

    def __init__(self):
        self.score = []
        self.timestamp = []

    def save_data(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.score, file)
            pickle.dump(self.timestamp, file)
