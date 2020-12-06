import simpy
from typing import Any, List
from datetime import datetime
from simpy.events import AnyOf
from simulation.environment.flight_cabin import FlightCabin
from simulation.processes.passenger import Passenger
from simulation.support.logger import loggy

class FlightManifest(object):
    def __init__(self, env: simpy.Environment , flightNum: int, passengerList: List[Passenger], cabinBookings: list):
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
                loggy.log(events[p], datetime.fromtimestamp(self.env.now).isoformat())
                eventList.remove(p)
                eventList.append((self.passengerList[events[p]["pid"]].event))

    def finalOutput(self):
        print("Checked in:", len(self.checkedIn))
        print("Seated:", len(self.seating))
