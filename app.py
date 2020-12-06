#this will be used to host the FLASK api server
import time
from simulation.support.database import client
from simulation.environment.scenario import Scenario
from simulation.support.util import *
from simulation.simulation import *
import uuid
from flask import Flask, request

app = Flask(__name__)


def startSim(scen, data):
    startTime = time.strptime("12/01/2020 01:00:00", "%d/%m/%Y %H:%M:%S")
    endTime = time.strptime("12/01/2020 22:00:00", "%d/%m/%Y %H:%M:%S")
    scenario = getScenario(scen)
    testScenario = Scenario(time.mktime(startTime), time.mktime(endTime), scenario["Dept"], scenario["Arriv"]
        , scenario["PassengerList"], scenario["cabins"], scenario["FlightNum"])
    runSimulation(testScenario)
    return testScenario.uuid

@app.route('/simulation/<name>/', methods=["GET", "POST"])
def simulation(name):
    data = None
    if request.method == 'POST':
        data = dict(request.json)
        print(data)
    return startSim(name, data)

if __name__ == '__main__':
    app.run(port=3031)