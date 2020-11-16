import simpy
import random
from datetime import datetime
from simulation.environment.scenario import Scenario
class Passenger(object):
    def __init__(self, env: simpy.Environment ,scenario: Scenario, id: int, name: str, checkInTime: int):
        # passenger data model info
        self.env = env
        self.scenario = scenario
        self.id = id
        self.name = name
        self.checkInTime = checkInTime
        self.checked_in = env.event()
        self.atGate = False

    def checkIn(self):
        yield self.env.timeout(self.checkInTime)
        print("Passenger %d has checked in" % self.id, datetime.fromtimestamp(self.env.now))
        self.checked_in.succeed(self.id)
        gateArrivalTime = random.randrange(600, self.scenario.flightBoardingTime - self.env.now - 600) 
        yield self.env.timeout(gateArrivalTime)
        print("Passenger %d has arrived at the gate" % self.id, datetime.fromtimestamp(self.env.now)) 
        self.atGate = True
