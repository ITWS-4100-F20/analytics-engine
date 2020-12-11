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
from simulation.support.flatten import flatten

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

"""
def getScenario(scenarioname:str, parameters={}):
    startTime = time.strptime("12/01/2020 22:00:00", "%d/%m/%Y %H:%M:%S")
    endTime = time.strptime("12/02/2020 22:00:00", "%d/%m/%Y %H:%M:%S")
    scenario = dict(client["simulation_data"]["scenarios"].find_one({"id":scenarioname}))
    scenario = Scenario(time.mktime(startTime), time.mktime(endTime), scenario["Dept"], scenario["Arriv"]
                    , scenario["PassengerList"], scenario["cabins"], scenario["FlightNum"])
    client["simulation_data"]["Simulations"].insert_one({
        "id" : scenario.uuid,
        "scenario_name": scenarioname,
        "status" : "RUNNING",
        "parameters" : parameters,
        "timestamp" : datetime.now().isoformat(),
        "info" : {
            "dept" : scenario.departureAirport,
            "arriv" : scenario.arrivalAirport,
            "flight_number" : 1768,
            "start_time" : "2020-12-01T22:00:00+0000",
            "departure_time" : "2020-12-02T22:00:00+0000",
            "finalize_time" : "2020-12-02T22:00:00+0000",
            "outcome" : "success"
        },
        "cabins" : scenario.cabins,
        "volunteers" : {
            "total_bids" : 0,
            "total_volunteers" : 0,
            "total_volunteers_processed" : 0
        }
    })
    client["simulation_data"]["Simulation_Events"].insert_one({
        "sim_id" : scenario.uuid, 
        "event_list" : []
    })
    client["simulation_data"]["Simulation_Volunteers"].insert_one({
        "sim_id" : scenario.uuid, 
        "vol_list" : []
    }) 
    client["simulation_data"]["Simulation_Passengers"].insert_one({
        "sim_id" : scenario.uuid, 
        "vol_list" : []
    }) 
    return scenario

def updateSenario(uuid:str):
    client["simulation_data"]["Simulations"].update_one({"id" : uuid}, {"$set" : {"status":"SUCCESS"}})

def logger(eventtype:str, msg:str, time:str):
    pass
"""