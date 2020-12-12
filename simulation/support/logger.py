from simulation.passenger import Passenger
from simulation.support.database import client
from copy import copy
import concurrent.futures
import threading

class Logger(object):
    """
    Controls logging for the entire application.
    """
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
        thread = threading.Thread(target=self._logger, kwargs={'data' : data, "time":time}).start()
    
    def __logPassengers(self, passengers:list, volunteer):
        loc = "Simulation_Passengers"
        if volunteer:
            loc = "Simulation_Volunteers"
        for i in passengers:
            if i.details["vol_info"]["processed"] == False:
                i.details["compensation"] = []
        client["simulation_data"][loc].update_one({"sim_id": self.name}, {"$set" :{"vol_list" :  [i.details for i in passengers]}})
        if volunteer:
            total_volunteers = len(passengers)
            total_processed = sum([1 if i.processed else 0 for i in passengers])
            total_bids = sum([i.details["compensation"][-1]["comp_amount"] if i.processed else 0 for i in passengers])
            client["simulation_data"]["Simulations"].update_one({"id" : self.name}, {"$set" : {"volunteers":{"total_bids": total_bids,"total_volunteers":total_volunteers, "total_volunteers_processed":total_processed}}})


    def logPassengers(self, passengers:list, volunteer):
        thread = threading.Thread(target=self.__logPassengers, kwargs={'passengers' : passengers, "volunteer":volunteer}).start()

loggy = Logger()
