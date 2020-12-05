import simpy
from typing import Any, List
from simpy.events import AnyOf
from simulation.environment.flight_cabin import FlightCabin
from simulation.processes.passenger import Passenger
class FlightManifest(object):
    def __init__(self, env: simpy.Environment ,flightID: int, flightNum: int, passengerList: List[Passenger], cabinBookings: list):
        self.env = env
        self.flightID = flightID
        self.flightnum = flightNum
        self.passengerList = passengerList
        self.cabinBookings = cabinBookings
        self.seatingReady = env.event()
        self.checkedIn = []
        self.seating = []
        
    def setupPassengers(self) -> None:
        print("Setting up passengers")
        eventList = []
        for p in self.passengerList:
            self.env.process(p.checkIn())
            eventList.append(p.checked_in)
            self.env.process(p.reqCabin(self.env))
        self.env.process(self.passengerWait(eventList))

    def passengerWait(self, eventList: List[simpy.Event]):
        while len(eventList) > 0:
            checked_in = yield AnyOf(self.env, eventList) 
            for p in checked_in:
                self.checkedIn.append(checked_in[p])
                eventList.remove(p)

    def finalOutput(self):
        print("Checked in:", len(self.checkedIn))
        print("Seated:", len(self.seating))
