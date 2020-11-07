import simpy
from datetime import datetime

class Passenger(object):
    def __init__(self, env: simpy.Environment ,id: int, name: str, checkInTime: int):
        # passenger data model info
        self.env = env
        self.id = id
        self.name = name
        self.checkInTime = checkInTime
        self.checked_in = env.event()

    def checkIn(self):
        yield self.env.timeout(self.checkInTime)
        print("Passenger %d has checked in" % self.id, datetime.fromtimestamp(self.env.now))
        self.checked_in.succeed()
