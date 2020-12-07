import simpy
from typing import Any, List
from datetime import datetime
from simpy.events import AnyOf
from simulation.environment.flight_cabin import FlightCabin
from simulation.processes.passenger import Passenger
from simulation.support.logger import loggy
from simulation.environment.scenario import Scenario

class FlightManifest(object):
    def __init__(self, scen: Scenario, env: simpy.Environment , flightNum: int, passengerList: List[Passenger], cabinBookings: list):
        self.scenario = scen
        self.env = env
        self.flightnum = flightNum
        self.passengerList = {p.id : p for p in passengerList}
        self.cabinBookings = cabinBookings
        self.seatingReady = env.event()
        self.checkedIn = []
        self.volunteered = []
        self.seating = []
        
    def setupPassengers(self) -> None:
        #print("Setting up passengers")
        eventList = []
        for p in self.passengerList.values():
            self.env.process(p.checkIn())
            self.env.process(p.cancel())
            eventList.append(p.event)
        self.env.process(self.passengerWait(eventList))
    
    """
        eligibliity:
            wanna volunteer
            no ineligable factors
                underage,etc.
            part of group

    """

    def passengerWait(self, eventList: List[simpy.Event]):
        while len(eventList) > 0:
            events = yield AnyOf(self.env, eventList) 
            for p in events:
                self.passengerList[events[p]["pid"]].event = self.env.event()
                print(events[p])
                eventtype = events[p]["event_type"]
                if eventtype == "CHECK_IN":
                    self.checkedIn.append(events[p]["pid"])
                    self.env.process(self.passengerList[events[p]["pid"]].respondToBid())
                elif eventtype == "BID":
                    res = events[p]["details"]["response"]
                    if res == 0:
                        self.env.process(self.passengerList[events[p]["pid"]].respondToBid())
                    elif res == 1:
                        self.volunteered.append(events[p]["pid"])
                elif eventtype == "CANCELED":
                    if events[p]["pid"] in self.volunteered:
                        self.volunteered.remove(events[p]["pid"])
                    if events[p]["pid"] in self.checkedIn:
                        self.checkedIn.remove(events[p]["pid"])
                loggy.logEvents(events[p], datetime.fromtimestamp(self.env.now).isoformat())
                eventList.remove(p)
                eventList.append((self.passengerList[events[p]["pid"]].event))

    def cmp_pass(self, a:Passenger, b:Passenger):
        if a.bidAmount() < b.bidAmount():
            return -1
        elif a.bidAmount() == b.bidAmount():
            return 0
        else:
            return 1

    def finalOutput(self):
        volpass = [self.passengerList[i] for i in self.volunteered]
        volpass.sort(key=lambda x: x.bidAmount())
        for cabin in self.scenario.cabins.keys():
            diff = self.scenario.cabins[cabin]["passengers"] - self.scenario.cabins[cabin]["capacity"]
            diff = diff if diff > 0 else 0
            print("\t\t\t",diff,cabin)
            for i in volpass:
                if diff == 0:
                    break
                if i.details["vol_info"]["cabin"] == cabin:
                    i.processed = True
                    i.details["vol_info"]["processed"] = True
                    i.leaveFlight()
                    diff += -1


        loggy.logPassengers(volpass, True)
        loggy.logPassengers(self.passengerList.values(), False)
        print("Checked in:", len(self.checkedIn))
        print("Seated:", len(self.seating))
