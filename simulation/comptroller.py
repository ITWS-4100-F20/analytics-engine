from simulation.support.database import client
from sklearn.neural_network import MLPClassifier
from simulation.passenger import Passenger
from simulation.support.modelHelper import numeric, keyed_numeric, test
from simulation.support.flatten import flatten
from copy import copy
import pymongo
import random
import numpy
import pickle

class Comptroller(object):

    def __init__(self, keys:list, compModel:str, passengerModel:str, target:float, passTarget:str, compTarget:str, data:str):
        test()
        self.compMod:MLPClassifier = self.__getModel(compModel)
        self.passMod:MLPClassifier = self.__getModel(passengerModel)
        self.bidNumber:int = 0
        self.target:float = target
        self.keys:list = keys
        self.passTarget:str = passTarget
        self.compTarget:str = compTarget
        modelData, self.keystore = numeric(flatten([dict(i) for i in client["simulation_data"][data].find({})]))
    
    def __getModel(self, name:str):
        return pickle.loads([i for i in client["simulation_data"]["model"].find({"name" : name}).sort("_id",-1).limit(1)][0]["model"])
    
    def Bid(self, passenger:dict, timeleft:int):
        comp_types = {0: {"type": "ETC", "value" : 0, "pass" : 0}, 1: {"type": "MILES", "value" : 0, "pass" : 0}}
        choice = float("inf")
        key = ""
        for i in comp_types.keys():
            row, self.keystore = keyed_numeric({k : passenger[k] for k in self.keys if k != self.passTarget and k in passenger.keys()}, self.keystore)
            row["comp-target"] = self.target
            row["comp_type"] = i
            row["pass-result"] = True
            row["comp_amount"] = 0
            row["comp_timeleft"] = timeleft
            pdata = numpy.array([[row[i] for i in self.keys if i != "comp_amount" and i != "pass-result"]]).reshape(1,-1)
            d = self.compMod.predict(pdata)
            row["comp_amount"] = d[0]
            pdata = numpy.array([[row[i] for i in self.keys if i != "pass-result" and i != "comp-target"]]).reshape(1,-1)
            d = self.passMod.predict_proba(pdata)
            print(d)
            row["comp-result"] = d[0][0]
            comp_types[i]["value"] = row["comp_amount"]
            comp_types[i]["pass"] = row["comp-result"]
            value = (1 - comp_types[i]["pass"]) * (comp_types[i]["value"] * (1 if i == 0 else 1))
            if value < choice:
                key = i
                choice = value
            print("Choice Upload ",i, value, comp_types[i]["value"], comp_types[i]["type"])
        result = True if random.randint(0, 100) < comp_types[key]["pass"] * 100 else False
        bid = {
            "accepted" : result,
            "bid_id" : self.bidNumber,
            "etc_comp" : comp_types[key]["value"] if comp_types[key]["type"] == "ETC" else int(comp_types[key]["value"]/5),
            "initiated_by" : "USER",
            "miles_comp": comp_types[key]["value"] * 5 if comp_types[key]["type"] == "ETC" else comp_types[key]["value"],
            "timestamp" : "", #datetime.fromtimestamp(p.env.now).isoformat(),
            "vol_id" : passenger["id"],
            "vol_name": passenger["pass_name"]
        }
        comp = {
          "comp_amount": comp_types[key]["value"],
          "comp_id": self.bidNumber,
          "comp_type": comp_types[key]["type"],
          "vol_id": passenger["id"]
        }
        self.bidNumber += 1
        return (result, comp, bid)