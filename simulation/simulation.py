import simpy
import json
import time
import pymongo
from datetime import datetime
from simulation.environment.scenario import Scenario
from simulation.processes.passenger import Passenger
from simulation.environment.flight_cabin import FlightCabin
from simulation.environment.flight_manifest import FlightManifest
from simulation.support.database import client
from simulation.support.util import *
def timeCheck(env: simpy.Environment):
    while True:
        print("Time is now %s" % datetime.fromtimestamp(env.now))
        wait_duration = 3600
        yield env.timeout(wait_duration)

def runSimulation(scenario: Scenario):
    print("Oversale Simulation initiated", datetime.fromtimestamp(scenario.oversaleStartTime), "for flight", 133, "from", scenario.departureAirport, "to", scenario.arrivalAirport, ".")
    env = simpy.Environment(initial_time=scenario.oversaleStartTime)
    totalpassengers = sum(scenario.cabins[i]["passengers"] for i in scenario.cabins.keys())
    passengers = getPassengers(totalpassengers, scenario, env)
    cabins = getCabins(scenario.cabins, passengers)
    manifest = FlightManifest(env, scenario.flightid, scenario.flightnum, passengers, cabins)
    manifest.setupPassengers()
    env.process(timeCheck(env))
    env.run(until=scenario.flightBoardingTime)      
    manifest.finalOutput()