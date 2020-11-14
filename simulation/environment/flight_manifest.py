import simpy
from simpy.events import AnyOf
from simulation.environment.flight_cabin import FlightCabin
from simulation.processes.passenger import Passenger
class FlightManifest(object):
    def __init__(self, env: simpy.Environment ,flightID: int, flightNum: int, passengerList: list, cabinBookings: list):
        self.env = env
        self.flightID = flightID
        self.flightnum = flightNum
        self.passengerList = passengerList
        self.cabinBookings = cabinBookings
        self.seatingReady = env.event()
        self.checkedIn = []
        self.seating = []
        self.initPassengers()

    def initPassengers(self):
        print(self.flightID)
        pList = [p.checked_in for p in self.passengerList]
        while True:
            yield AnyOf(self.env, pList)
            print("someone checked in")
            return