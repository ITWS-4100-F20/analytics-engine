#this will be used to host the FLASK api server
import time
from simulation import simulation
from simulation.support.database import client
from simulation.environment.scenario import Scenario
from simulation.support.util import *

from flask import Flask, request

app = Flask(__name__)


def startSim():
    startTime = time.strptime("12/01/2020 01:00:00", "%d/%m/%Y %H:%M:%S")
    endTime = time.strptime("12/01/2020 22:00:00", "%d/%m/%Y %H:%M:%S")
    scenario = getScenario('nick_test')
    testScenario = Scenario(time.mktime(startTime), time.mktime(endTime), scenario["start"], scenario["dest"]
        , scenario["manifestId"], scenario["cabins"], scenario["flightid"], scenario["flightnum"])
    simulation.runSimulation(testScenario)

@app.route('/simulation')
def simulation():
    if request.method == 'POST':
        print('POST')

if __name__ == '__main__':
    app.run(port=3031)