from simulation.scenario import Scenario
from simulation.comptroller import Comptroller
from simulation.passenger import Passenger
import simpy
from typing import Any, List
from simulation.support.logger import loggy
from simpy.events import AnyOf
from datetime import datetime
import random
import time

class Simulation(Scenario):
    """
    Controls the entire simulation.
    """
    def __init__(self, scenarioName: str, parameters:dict):
        super().__init__(scenarioName, parameters)
        self.comptroller:Comptroller = Comptroller(self.keys, self.compModel, self.passModel, self.target, self.passTarget, self.compTarget, self.dataModel)
        self.passengers = {}
        self.checkedIn = []
        self.volunteered = []
        self.canceled = []
        self.__setupPassengers()
        self.bids = 0
        loggy.name = self.uuid
        
    def __setupPassengers(self):
        """
        Initializes all the passengers, their cabins, and their processes.
        """
        startid = random.randint(101,253)
        for key in self.cabins.keys():
            for i in range(0, self.cabins[key]["passengers"]):
                self.passengers[str(startid)] = Passenger(self.env, self, str(startid), key, self.dest)
                startid += 1
        for i in range(0, self.newPassengers):
            self.passengers[str(startid)] = Passenger(self.env, self, str(startid), random.choice([i for i in self.cabins.keys()]), self.dest)
            startid += 1
        eventList = {}
        for p in self.passengers.values():
            self.env.process(p.start())
            eventList[p.id] = p.events
        self.env.process(self.__passengerWait(eventList))
    
    def __join(self, eventList):
        res = []
        for i in eventList.values():
            res.extend(i)
        return res

    def __passengerWait(self, eventList):
        """
        Listens for events returned by passenger objects. Controls the next moves by the simulation 
        regarding that passenger.
        """
        while sum(len(i) for i in eventList.values()) > 0:
            e = yield AnyOf(self.env, self.__join(eventList)) 
            for p in e:
                print(e[p])
                eventtype = e[p]["event_type"]
                add = []
                if eventtype == "CHECK_IN":
                    self.checkedIn.append(e[p]["pid"])
                    e1 = self.env.event()
                    e2 = self.env.event()
                    add.append(e1)
                    add.append(e2)
                    self.env.process(self.passengers[e[p]["pid"]].respondToBid(self.comptroller, True, e1))
                    self.env.process(self.passengers[e[p]["pid"]].gateArrival(e2))
                elif eventtype == "BID":
                    t = int(time.mktime(self.endTime.timetuple()) - self.env.now)
                    if t > 89:
                        res = e[p]["details"]["response"]
                        self.bids += 1
                        if res == 0:
                            e1 = self.env.event()
                            add.append(e1)
                            self.env.process(self.passengers[e[p]["pid"]].respondToBid(self.comptroller, False, e1))
                        else:
                            self.volunteered.append(e[p]["pid"])
                elif eventtype == "CANCELED":
                    if e[p]["pid"] in self.volunteered:
                        self.volunteered.remove(e[p]["pid"])
                    if e[p]["pid"] in self.checkedIn:
                        self.checkedIn.remove(e[p]["pid"])
                    self.canceled.append(e[p]["pid"])
                    loggy.logEvents(e[p], datetime.fromtimestamp(self.env.now).isoformat())
                    del eventList[e[p]["pid"]]
                loggy.logEvents(e[p], datetime.fromtimestamp(self.env.now).isoformat())
                self.passengers[e[p]["pid"]].events.remove(p)
                if eventtype != "CANCELED":
                    eventList[e[p]["pid"]] = self.passengers[e[p]["pid"]].events + add

    def run(self):
        """
        Runs the simulation and controls final logging.
        """
        self.env.run(until=time.mktime(self.endTime.timetuple())) 
        self.updateStatus()
        notvol = [self.passengers[i].name for i in self.passengers.keys() if i not in self.volunteered and i not in self.canceled]
        volpass = [self.passengers[i] for i in self.volunteered]
        volpass.sort(key=lambda x: x.bidAmount())
        for cabin in self.cabins.keys():
            diff = self.cabins[cabin]["passengers"] - self.cabins[cabin]["capacity"]
            diff = diff if diff > 0 else 0
            for i in volpass:
                if diff == 0:
                    break
                if i.details["vol_info"]["cabin"] == cabin:
                    i.processed = True
                    i.details["vol_info"]["processed"] = True
                    diff += -1
        loggy.logPassengers(volpass, True)
        loggy.logPassengers(self.passengers.values(), False)

        print("""COMPLETED SIMULATION\n
        bids: {}
        init_passengers: {}
        fin_passengers: {}
        volunteers: {}
        not volunteers: {}
        checkedin: {}
        canceled: {}
        capacity:{}""".format(self.bids, self.totalPassengers, self.totalPassengers - len(self.canceled), len(self.volunteered), len(notvol), len(self.checkedIn), len(self.canceled), self.capacity))