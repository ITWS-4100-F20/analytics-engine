import simpy
import time
from datetime import datetime
from simulation.environment.scenario import Scenario
from simulation.processes.passenger import Passenger

def timeCheck(env: simpy.Environment):
    while True:
        print("Time is now %s" % datetime.fromtimestamp(env.now))
        wait_duration = 3600
        yield env.timeout(wait_duration)

def runSimulation(scenario: Scenario):
    print("Oversale Simulation initiated", datetime.fromtimestamp(scenario.oversaleStartTime), "for flight", 133, "from", scenario.departureAirport, "to", scenario.arrivalAirport, ".")
    env = simpy.Environment(initial_time=scenario.oversaleStartTime)
    passengers = [
        Passenger(env, 244, 'John',  time.mktime(time.strptime("12/01/2020 10:00:00", "%d/%m/%Y %H:%M:%S"))- scenario.oversaleStartTime),
        Passenger(env, 34, 'Joe',  time.mktime(time.strptime("12/01/2020 12:30:00", "%d/%m/%Y %H:%M:%S"))- scenario.oversaleStartTime)
    ]
    for p in passengers:
        env.process(p.checkIn())
    env.process(timeCheck(env))
    env.run(until=scenario.flightBoardingTime)      
