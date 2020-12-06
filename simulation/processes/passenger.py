import simpy
import random
from datetime import datetime
from simulation.environment.scenario import Scenario
from simulation.environment.flight_cabin import FlightCabin

class Passenger(object):
    def __init__(self, env: simpy.Environment ,scenario: Scenario, id: int, name: str, checkInTime: int):
        # passenger data model info
        self.env = env
        self.scenario = scenario
        self.id = id
        self.name = name
        self.volunteer_method = "DEFAULT"
        self.checkInTime = checkInTime
        self.event = env.event()
        self.finalDest = scenario.arrivalAirport
        self.atGate = False
        self.processed = False
        self.req = None
        self.cabin = None
        self.details = {
            "bid_history" : [

            ],
            "compensation" : [

            ],
            "vol_info" : {
                "cabin" : "Default",
                "fin_dest" : self.finalDest,
                "id" : self.id,
                "name" : self.name,
                "processed" : True,
                "vol_method" : "DEFAULT"
            }
        }
        self.ml = { #these are a bumch of parameters to be grabbed from the database about the customer.
            "age": 42,
            "miles": 200123,
            "checked": 1,
            "carryon": 1,
            "gender": 0.0,
            "memberlevel": 1,
            "lastflighttime": 124
        }

    def setCabin(self, cabin:FlightCabin):
        if self.req is not None:
            self.cabin.release(self.req)
        self.details["vol_info"]["cabin"] = cabin.cabinType
        self.cabin = cabin

    def leaveFlight(self):
        self.cabin.release(self.req)

    def cancel(self):
        while True:
            if random.randint(0,1000) == 0:
                self.event.succeed({"pid" : self.id, "event_type" : "CANCELED", "details" : {}})
                return False
            yield self.env.timeout(1000)

    def checkIn(self):
        yield self.env.timeout(self.checkInTime)
        #print("Passenger %d has checked in" % self.id, datetime.fromtimestamp(self.env.now))
        self.event.succeed({"pid" : self.id, "event_type" : "CHECK_IN", "details" : {}})
        self.env.process(self.reqCabin())
        try:
            gateArrivalTime = random.randrange(600, self.scenario.flightBoardingTime - self.env.now - 600)
        except:
            gateArrivalTime = 0
        yield self.env.timeout(gateArrivalTime if gateArrivalTime > 0 else 1)
        #print("Passenger %d has arrived at the gate" % self.id, datetime.fromtimestamp(self.env.now)) 
        self.atGate = True

    def respondToBid(self):
        time = random.randrange(100, 600)
        self.event.succeed({"pid" : self.id, "event_type" : "BID", "details" : {
            "amount" : 69,
            "ETC" : 100,
            "response" : 1
            }
        })
        self.details["bid_history"].append(
            {
                "accepted" : True,
                "bid_id" : 123,
                "etc_comp" : 1,
                "initiated_by" : "USER",
                "miles_comp": 30,
                "timestamp" : datetime.fromtimestamp(self.env.now).isoformat(),
                "vol_id" : self.id,
                "vol_name": self.name
            }
        )
        self.details["compensation"].append(
            {
                "comp_amount": 1,
                "comp_id": 1,
                "comp_type": "FOOOOOD",
                "vol_id": 1
            }
        )
        yield self.env.timeout(time)
        #retrive bid so passenger gets it
        #print("Passenger %d has responded to bid number %d with %r." % (self.id, 21, True), datetime.fromtimestamp(self.env.now)) 
        #takes info about flight offer and self and responds based on probabiltiy from neural network to offer.

    def reqCabin(self):
        self.req = self.cabin.request()
        yield self.req
        #print("Passenger %d has recieved a seat" % self.id, datetime.fromtimestamp(self.env.now)) 
    
