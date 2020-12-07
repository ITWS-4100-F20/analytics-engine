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
        self.comp = 0
        self.len = client["simulation_data"]["Compensation"].count()
    
    def getCompensation(self, p):
        bidStart = flatten([dict(i) for i in client["simulation_data"]["Compensation"].find({}).skip(random.randint(0,self.len-1)).limit(1)])[0]
        bid = {
            "accepted" : False,
            "bid_id" : self.bids,
            "etc_comp" : bidStart["etc_comp"],
            "initiated_by" : "USER",
            "miles_comp": 5 * bidStart["etc_comp"],
            "timestamp" : datetime.fromtimestamp(p.env.now).isoformat(),
            "vol_id" : p.id,
            "vol_name": p.name
        }
        self.bids += 1
        compChosen= (random.choice([(bidStart["etc_comp"], "ETC"),(bidStart["etc_comp"] * 5, "MILES")]))
        comp = {
          "comp_amount": compChosen[0],
          "comp_id": self.comp,
          "comp_type": compChosen[1],
          "vol_id": 1
        }
        self.comp += 1
        return bid, comp

compy = Comptroller()