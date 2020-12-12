import threading
from simulation.simulation import Simulation
from simulation.support.modelHelper import createModels
from flask import Flask, request
from simulation.support.modelHelper import test

app = Flask(__name__)

def __startSim(scen:Simulation):
    scen.run()
    pass

@app.route('/simulation', methods=["POST"])
def simulation():
    #test()
    data = dict(request.json)
    scen = Simulation(data["scenarioId"], data["parameters"])
    thread = threading.Thread(target=__startSim, kwargs={'scen' : scen}).start()
    return {"sim_id" :scen.uuid }
    #return "hi"

@app.route('/modelDefinition', methods=["POST"])
def modelAdd():
    data = dict(request.json)
    createModels(data["def_name"],data["data_schema_name"],data["passenger_target"],data["comp_target"],data["ignore_pass"],data["ignore_comp"])
    return "ok", 200

if __name__ == '__main__':
    app.run(port=3031, host='0.0.0.0')