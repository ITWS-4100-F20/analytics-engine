import threading
from simulation.simulation import Simulation
from flask import Flask, request

app = Flask(__name__)

def __startSim(scen:Simulation):
    scen.run()

@app.route('/simulation', methods=["POST"])
def simulation():
    data = dict(request.json)
    scen = Simulation(data["scenarioId"], data["parameters"])
    thread = threading.Thread(target=__startSim, kwargs={'scen' : scen}).start()
    return {"sim_id" :scen.uuid }

if __name__ == '__main__':
    app.run(port=3031, host='0.0.0.0')