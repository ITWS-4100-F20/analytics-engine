import simpy
import json
import time
import pymongo
from datetime import datetime
from simulation.environment.scenario import Scenario
from simulation.processes.passenger import Passenger
from simulation.environment.flight_cabin import FlightCabin
from simulation.environment.flight_manifest import FlightManifest
from simulation.support.database import client

def flatten(data:list):
    res = []
    for row in data:
        rowdata = {}
        for point in row["fields"]:
            rowdata[point["field"]] = point["value"]
            if point["datatype"] == "int":
                rowdata[point["field"]] = int(point["value"])
        res.append(rowdata)
    return res

def getPassengers(n:int, scenario, env):
    passengerdata = flatten([dict(i) for i in client["simulation_data"]["nick_passengers"].find({}).limit(n)])
    passengers = []
    for passenger in passengerdata:
        delay = (time.mktime(time.strptime("12/01/2020 " + passenger["checkintime"], "%d/%m/%Y %H:%M:%S"))- scenario.oversaleStartTime)
        passengers.append(Passenger(env, scenario, passenger["number"], passenger["name"],  delay if delay >= 0 else 1 ))
    return passengers

def getCabins(env, cabinSpec:dict, passengers:list):
    cabins = []
    currentPass = 0
    for i in cabinSpec.keys():
        cabinpass = passengers[currentPass:currentPass+int(cabinSpec[i]["passengers"])]
        newcabin = FlightCabin(env, i, int(cabinSpec[i]["capacity"]), cabinpass)
        for passenger in cabinpass:
            passenger.setCabin(newcabin)

        cabins.append(newcabin)
        currentPass += int(cabinSpec[i]["passengers"])
    return cabins

def getScenario(scenarioname:str):
    startTime = time.strptime("12/01/2020 01:00:00", "%d/%m/%Y %H:%M:%S")
    endTime = time.strptime("12/01/2020 22:00:00", "%d/%m/%Y %H:%M:%S")
    scenario = dict(client["simulation_data"]["scenarios"].find_one({"id":scenarioname}))
    scenario = Scenario(time.mktime(startTime), time.mktime(endTime), scenario["Dept"], scenario["Arriv"]
                    , scenario["PassengerList"], scenario["cabins"], scenario["FlightNum"])
    client["simulation_data"]["Simulations"].insert_one({
        "id" : scenario.uuid,
        "scenario_name": scenarioname,
        "status" : "RUNNING",
        "parameters" : {}
    })
    client["simulation_data"]["Simulation_Events"].insert_one({
        "sim_id" : scenario.uuid, 
        "event_list" : []
    })
    client["simulation_data"]["Simulation_Volunteers"].insert_one({
        "sim_id" : scenario.uuid, 
        "vol_list" : []
    }) 
    return scenario

def logger(eventtype:str, msg:str, time:str):
    pass