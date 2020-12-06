from datetime import datetime

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
    
    def getCompensation(self, p):
        bid = {
            "accepted" : False,
            "bid_id" : self.bids,
            "etc_comp" : 1,
            "initiated_by" : "USER",
            "miles_comp": 30,
            "timestamp" : datetime.fromtimestamp(p.env.now).isoformat(),
            "vol_id" : p.id,
            "vol_name": p.name
        }
        self.bids += 1
        comp = {
          "comp_amount": 1,
          "comp_id": 1,
          "comp_type": "FOOOOOD",
          "vol_id": 1
        }
        return bid, comp

compy = Comptroller()