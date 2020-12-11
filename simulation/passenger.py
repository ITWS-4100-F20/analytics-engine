import simpy
import random
import names
import time
from datetime import datetime
import numpy.random
from simulation.scenario import Scenario

class Passenger(object):
    def __init__(self, env:simpy.Environment, scenario:Scenario, id:str, cabin:str, dest:str):
        self.dest = dest
        self.scenario:Scenario = scenario
        self.env:simpy.Environment = env
        self.events:env.event = [self.env.event()]
        self.cabin:str = cabin
        self.id:str = id #From schema
        self.gender:str = random.choice(["male", "female"])
        self.name:str = names.get_full_name(gender=self.gender) #From schema
        self.processed:bool = False
        self.checkin = False
        self.gate = False
        memberchoice:dict = random.choice([("None", random.randint(0, 25000)), ("Silver", random.randint(25000, 75000)), ("Gold", random.randint(75000, 150000)), ("Platinum", random.randint(150000, 250000))])
        self.details:dict = {
            "bid_history" : [

            ],
            "compensation" : [

            ],
            "vol_info" : {
                "cabin" : self.cabin,
                "fin_dest" : self.dest,
                "id" : self.id,
                "name" : self.name,
                "processed" : False, #needs to be overwritten when processed
                "vol_method" : random.choice(["APP","WEB","KIOSK","GATE"]),
                "volstatus" : False,
                "baggage": random.choice([0,1,2,3]),
                "age" : random.randint(18, 65),
                "gender": self.gender,
                "memberlevel": memberchoice[0],
                "miles" :  memberchoice[1]
            }
        }

    
    def start(self):
        res = self.events[0]
        yield self.env.timeout(0)
        self.env.process(self.checkIn())
        self.env.process(self.cancel())
        res.succeed(
            {
                "pid" : self.id,
                "event_type" : "START",
                "details" : {
                    "name" : self.name
                }
            })

    def checkIn(self):
        res = self.env.event()
        self.events.append(res)
        t = numpy.random.normal(0, 10000)
        yield self.env.timeout(t if t > 0 else -t)
        res.succeed(
            {
                "pid" : self.id,
                "event_type" : "CHECK_IN",
                "details" : {
                    "name" : self.name
                }
            })
        self.checkin = True

    def gateArrival(self):
        res = self.env.event()
        self.events.append(res)
        t = int(time.mktime(self.scenario.endTime.timetuple()) - self.env.now)
        print("Time Left: ", t)
        t = random.randint(0, t) if t < 14400 else (t - 14400) + random.randint(0, 14400)
        yield self.env.timeout(t)
        res.succeed(
            {
                "pid" : self.id,
                "event_type" : "GATE_ARRIVAL",
                "details" : {
                    "name" : self.name
                }
            })
        self.gate = True

    def cancel(self):
        if random.randint(0, 100) > 2:
            return
        t = int(time.mktime(self.scenario.endTime.timetuple()) - self.env.now)
        if t < 300:
            return
        t = random.randint(299, t)
        res = self.env.event()
        self.events.append(res)
        yield self.env.timeout(t)
        res.succeed({"pid" : self.id, "event_type" : "CANCELED", "details" : {
            "name" : self.name
        }})

    def respondToBid(self, comp, first):
        res = self.env.event()
        self.events.append(res)
        if first:
            t = 0
        else:
            t = int(time.mktime(self.scenario.endTime.timetuple()) - self.env.now)
            t = random.randint(90, t)
        yield self.env.timeout(t)
        #success, compensation, bid = comp(self)
        #self.details["bid_history"].append(bid)
        #if success:
        #    self.details["compensation"].append(compensation)
        res.succeed({"pid" : self.id, "event_type" : "BID", "details" : {
            "name" : self.name,
            "amount" : 69,
            "ETC" : 69,
            "response" : 1
            #"amount" : compensation["comp_amount"],
            #"ETC" : bid["etc_comp"],
            #"response" : 1 if success else 0
            }
        })

    def bidAmount(self):
        return self.details["compensation"][-1]["comp_amount"]
    
