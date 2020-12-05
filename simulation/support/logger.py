from simulation.support.database import client
from copy import copy
import concurrent.futures

class Logger(object):
    def __init__(self, name:str):
        self.name = name

    def _logger(self, data:dict, time:str):
        send = copy(data)
        send["time"] = time
        client["simulation_data"][self.name].insert_one(send)

    def log(self, data: dict, time:str):
        with concurrent.futures.ThreadPoolExecutor() as exc:
            exc.submit(self._logger, data = data, time = time)

loggy = Logger("testsimulationloging")
