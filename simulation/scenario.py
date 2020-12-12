import uuid
import simpy
from datetime import datetime
import time
from threading import Thread
from simulation.support.database import client
#from simulation.environment.flight_manifest import FlightManifest as Manifest

class Scenario(object):

    def __init__(self, scenarioName: str, parameters:dict):
        self.scenarioDict:dict = dict(client["simulation_data"]["Scenarios"].find_one({"id":scenarioName}))        
        self.uuid:str = str(uuid.uuid1())
        self.name:str = scenarioName
        self.parameters:dict = parameters
        self.modelDefinition:dict = dict(client["simulation_data"]["Model_Definitions"].find_one({"name":self.scenarioDict["modelDefinition"]}))
        self.startTime:datetime = datetime.strptime(self.scenarioDict["startTime"], "%d/%m/%Y %H:%M:%S")
        self.endTime:datetime = datetime.strptime(self.scenarioDict["endTime"], "%d/%m/%Y %H:%M:%S")
        self.triggerTime:datetime = datetime.now()
        self.cabins:dict = self.scenarioDict["cabins"]
        self.newPassengers:int = self.scenarioDict["newPassengers"]
        self.capacity = sum(self.cabins[i]["capacity"] for i in self.cabins.keys())
        self.totalPassengers:int = sum(self.cabins[i]["passengers"] for i in self.cabins.keys()) + self.newPassengers
        self.compModel:str = self.modelDefinition["compModel"]
        self.passModel:str = self.modelDefinition["passModel"]
        self.dataModel:str = self.modelDefinition["dataModel"]
        self.target:float = self.scenarioDict["target"]
        self.compTarget = self.modelDefinition["comp_target"]
        self.passTarget = self.modelDefinition["pass_target"]
        self.ignorePass = self.modelDefinition["ignore_pass"]
        self.ignoreComp = self.modelDefinition["ignore_comp"]
        self.keys:list = self.modelDefinition["keys"]
        self.dest:str = self.scenarioDict["Arriv"]
        Thread(target=self.__startup, kwargs={}).start()
        self.env:simpy.Environment = simpy.Environment(initial_time=time.mktime(self.startTime.timetuple()))
        #self.manifest:Manifest = 1#
        self.env.process(self.__hourTimer())
        #self.manifest.finalOutput()

    def __hourTimer(self):
        while True:
            print("Time is now %s" % datetime.fromtimestamp(self.env.now))
            yield self.env.timeout(3600)

    def __startup(self):
        client["simulation_data"]["Simulations"].insert_one({
            "id" : self.uuid,
            "scenario_name": self.name,
            "status" : "RUNNING",
            "parameters" : self.parameters,
            "timestamp" : datetime.now().isoformat(),
            "info" : {
                "dept" : self.scenarioDict["Dept"],
                "arriv" : self.scenarioDict["Arriv"],
                "flight_number" : 1768,
                "start_time" : self.startTime.isoformat(),
                "departure_time" : self.endTime.isoformat(),
                "finalize_time" : self.endTime.isoformat(),
                "outcome" : "Success"
            },
            "cabins" : self.cabins,
            "volunteers" : {
                "total_bids" : 0,
                "total_volunteers" : 0,
                "total_volunteers_processed" : 0
            }
        })
        client["simulation_data"]["Simulation_Events"].insert_one({
            "sim_id" : self.uuid, 
            "event_list" : []
        })
        client["simulation_data"]["Simulation_Volunteers"].insert_one({
            "sim_id" : self.uuid, 
            "vol_list" : []
        }) 
        client["simulation_data"]["Simulation_Passengers"].insert_one({
            "sim_id" : self.uuid, 
            "vol_list" : []
        }) 

    def __updateStatus(self):
        client["simulation_data"]["Simulations"].update_one({"id" : self.uuid}, {"$set" : {"status":"SUCCESS"}})

    def updateStatus(self):
        Thread(target=self.__updateStatus, kwargs={}).start()