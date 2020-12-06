#this will be used to host the FLASK api server
import time
import threading
from simulation.support.database import client
from simulation.environment.scenario import Scenario
from simulation.support.util import *
from simulation.simulation import *
import uuid
from flask import Flask, request

app = Flask(__name__)


def startSim(scen, data):
    runSimulation(scen)

@app.route('/simulation', methods=["POST"])
def simulation(name):
    data = dict(request.json)
    scen = getScenario(data["Id"])
    thread = threading.Thread(target = startSim, kwargs={'scen' : scen, 'data' : data["parameters"]})
    thread.start()
    return scen.uuid

if __name__ == '__main__':
    app.run(port=3031)