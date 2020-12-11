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
    def __init__(self, scenarioName: str, parameters:dict):
        super().__init__(scenarioName, parameters)
        self.comptroller:Comptroller = Comptroller(self.keys, self.compModel, self.passModel, self.target, self.passTarget, self.compTarget, self.dataModel)
        self.passengers = {}
        self.checkedIn = []
        self.volunteered = []
        self.canceled = []
        self.__setupPassengers()
        self.bids = 0
        
    def __setupPassengers(self):
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
        while sum(len(i) for i in eventList.values()) > 0:
            e = yield AnyOf(self.env, self.__join(eventList)) 
            for p in e:
                print(e[p])
                eventtype = e[p]["event_type"]
                if eventtype == "CHECK_IN":
                    self.checkedIn.append(e[p]["pid"])
                    self.env.process(self.passengers[e[p]["pid"]].respondToBid(self.comptroller, True))
                    self.env.process(self.passengers[e[p]["pid"]].gateArrival())
                elif eventtype == "BID":
                    res = e[p]["details"]["response"]
                    self.bids += 1
                    if res == 0:
                        self.env.process(self.passengers[e[p]["pid"]].respondToBid(self.comptroller, False))
                    else:
                        self.volunteered.append(e[p]["pid"])
                elif eventtype == "CANCELED":
                    if e[p]["pid"] in self.volunteered:
                        self.volunteered.remove(e[p]["pid"])
                    if e[p]["pid"] in self.checkedIn:
                        self.checkedIn.remove(e[p]["pid"])
                    self.canceled.append(e[p]["pid"])
                    eventList[e[p]["pid"]] = []
                #loggy.logEvents(events[p], datetime.fromtimestamp(self.env.now).isoformat())
                self.passengers[e[p]["pid"]].events.remove(p)
                if eventtype != "CANCELED":
                    eventList[e[p]["pid"]] = self.passengers[e[p]["pid"]].events

    def run(self):
        self.env.run(until=time.mktime(self.endTime.timetuple())) 
        self.updateStatus()
        print("COMPLETED SIMULATION\nbids: {}\npassengers: {}\nvolunteers: {}\ncheckedin: {}\ncanceled: {}\ncapacity:{}".format(self.bids, self.totalPassengers, len(self.volunteered), len(self.checkedIn), len(self.canceled), self.capacity))