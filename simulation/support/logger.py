from simulation.processes.passenger import Passenger
from simulation.support.database import client
from copy import copy
import concurrent.futures

class Logger(object):
    def __init__(self):
        self.name = "trash" #uuid
        self.data = []

    def _logger(self, data:dict, time:str):
        send = copy(data)
        send["time"] = time
        client["simulation_data"]["Simulation_Events"].update_one(
            {"sim_id": self.name},
            {"$push": {
                "event_list" : send
                }
            }
        )

    def logEvents(self, data: dict, time:str):
        with concurrent.futures.ThreadPoolExecutor() as exc:
            exc.submit(self._logger, data = data, time = time)
    
    def logPassengers(self, passengers:list):
        client["simulation_data"]["Simulation_Volunteers"].update_one(
            {"sim_id": self.name},
            {"$push": {
                "vol_list" : {
                    "$each":[i.details for i in passengers]
                    }
                }
            }
        )
loggy = Logger()
