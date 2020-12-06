from datetime import datetime
from simulation.support.flatten import flatten
from simulation.support.database import client
import random

class Compensation(object):
    def __init__(self, compensationCategory: str, compensationKeywords: list, compensationType: str ):
        self.compensationCategory = compensationCategory
        self.compensationKeyword = compensationKeywords
        #Compensation Type refers to if the data is Continuous (CONT) or Discrete(DISC)
        self.compensationType = compensationType

        @classmethod
        def setAmount(self, amount):
            self.amount = amount

defaultCompensationList = [
    Compensation("COMP", ["AGT_COMP", "COMP"], "CONT"),
    Compensation("MILES", ["MILES", "AGT_MILES"], "CONT"),
    Compensation("MEAL", ["MEAL_B", "MEAL_L", "MEAL_D"], "DISC"),
    Compensation("TRANS", ["TRANS"], "DISC"),
    Compensation("HOTEL", ["HOTEL"], "DISC"),
] 

class Comptroller(object):
    def __init__(self):
        self.bids = 0
        self.len = client["simulation_data"]["Compensation"].count()
    
    def getCompensation(self, p):
        bidStart = flatten([dict(i) for i in client["simulation_data"]["Compensation"].find({}).skip(random.randint(0,self.len-1)).limit(1)])[0]
        bid = {
            "accepted" : False,
            "bid_id" : self.bids,
            "etc_comp" : bidStart["etc_comp"],
            "initiated_by" : "USER",
            "miles_comp": bidStart["miles_comp"],
            "timestamp" : datetime.fromtimestamp(p.env.now).isoformat(),
            "vol_id" : p.id,
            "vol_name": p.name
        }
        self.bids += 1
        comp = {
          "comp_amount": bidStart["comp_amount"],
          "comp_id": 1,
          "comp_type": bidStart["comp_type"],
          "vol_id": 1
        }
        return bid, comp

compy = Comptroller()