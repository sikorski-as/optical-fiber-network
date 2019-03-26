import time


class Timer:

    def __init__(self):
        self.start_time = None

    def get_interval_of_time_from_start(self) ->float:
        """
            Takes current time and returns interval between start_time and current time.
            Returns:
                Time interval
        """
        if self.start_time is None:
            raise ValueError("To get time interval you need to start timer first!")
        return time.time() - self.start_time

    def start(self):
        self.start_time = time.time()




