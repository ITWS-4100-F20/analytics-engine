from simulation.support.database import client
from sklearn.neural_network import MLPClassifier
from simulation.passenger import Passenger
import pymongo
import numpy
import pickle

class Comptroller(object):

    def __init__(self, keys:list, compModel:str, passengerModel:str, target:float):
        self.compMod:MLPClassifier = self.__getModel(compModel)
        self.passMod:MLPClassifier = self.__getModel(passengerModel)
        self.bidNumber:int = 0
        self.target:float = target
        self.keys:list = keys
    
    def __getModel(self, name:str):
        return pickle.loads([i for i in client["simulation_data"]["model"].find({"name" : name}).sort("_id",-1).limit(1)][0]["model"])
    
    def Bid(self, passenger:Passenger, timeleft:int):
        comp_types = {"ETC": {"value" : 0, "pass" : 0}, "MILES": {"value" : 0, "pass" : 0}}
        choice = float("inf")
        key = ""
        for i in comp_types.keys():
            row = [passenger.ml[key] for key in self.keys if "pass_" in key]
            row.extend([i, timeleft, self.target])
            comp_types[i]["value"] = self.compMod.predict(row)
            row = [passenger.ml[key] for key in self.keys if "pass_" in key]
            row.extend([i,timeleft, comp_types[i]["value"]])
            comp_types[i]["pass"] = self.passMod.predict_proba(row)
            value = 1 - comp_types[i]["pass"] * comp_types[i]["value"] * (5 if i == "ETC" else 1)
            if value < choice:
                key = i
                choice = value
        print("Winning Key %s" % {key})
        
    """
    model_db = db["model"]
    #my_model = model_db.find({"name": model_name})
    version = 0
    for f in model_db.find({},{"name": model_name,"prediction":1,"version":1}):
        if f["version"] > version:
            version = f["version"]
            prediction_title = f["prediction"]
    my_model = model_db.find({"version": version})
    #print(prediction)
    for x in my_model:
        model = pickle.loads(x['model'])    
    
    def getCompensation(self, p):
        # comp type
        # comp amount predicted
        # target result
        # timeleft until boarding
        # initiated by

        # neural network retrieval
        # BID



        bidStart = flatten([dict(i) for i in client["simulation_data"]["Compensation"].find({}).skip(random.randint(0,self.len-1)).limit(1)])[0]
        bidStart["etc_comp"] = random.randint(2, 20) * 50
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
        compChosen= (random.choice([[bidStart["etc_comp"], "ETC"],[bidStart["etc_comp"] * 5, "MILES"]]))
        comp = {
          "comp_amount": compChosen[0],
          "comp_id": self.comp,
          "comp_type": compChosen[1],
          "vol_id": 1
        }
        self.comp += 1
        return bid, comp
    """