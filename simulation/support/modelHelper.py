from simulation.support.database import client
from simulation.support.flatten import flatten
from sklearn.neural_network import MLPClassifier
import uuid
import pymongo
import numpy
import pickle


def keyed_numeric(data, keystore:dict):
    keys = data.keys()
    for i in keys:
        if type(data[i]) == type(""):
            if data[i] not in keystore[i]:
                keystore[i].append(data[i])
            data[i] = keystore[i].index(data[i])
    return (data, keystore) 

def numeric(data):
    keystore = {}
    keys = data[0].keys()
    for i in keys:
        if type(data[0][i]) == type(""):
            values = []
            for k in data:
                if k[i] not in values:
                    values.append(k[i])
                k[i] = values.index(k[i])
            keystore[i] = values
    return (data, keystore)

def createModels(name, data, passengerTarget, compTarget, ignorePass:list, ignoreComp:list):
    modelData, keystore = numeric(flatten([dict(i) for i in client["simulation_data"][data].find({})]))
    comp_train = []
    comp_target = []
    pass_train = []
    pass_target = []
    comp_keys = [i for i in modelData[0].keys() if i != compTarget and i not in ignoreComp]
    pass_keys = [i for i in modelData[0].keys() if i != passengerTarget and i not in ignorePass]
    for row in modelData:
        print(row)
        comp_train.append([row[i] for i in comp_keys])
        comp_target.append(row[compTarget])
        pass_train.append([row[i] for i in pass_keys])
        pass_target.append(row[passengerTarget])
    print("started training")
    pass_model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(13, 100, 5, 1), random_state=1, max_iter=1000)
    pass_model.fit(pass_train, pass_target)
    comp_model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(13, 100, 5, 1), random_state=1, max_iter=1000)
    comp_model.fit(comp_train, comp_target)
    pass_pickle = pickle.dumps(pass_model)
    comp_pickle = pickle.dumps(comp_model)
    models = [{"id": uuid.uuid1(), "name": name+"_pass", "prediction": passengerTarget, "schema_id": data, "version": 1, "model": pass_pickle},
    {"id": uuid.uuid1(), "name": name+"_comp", "prediction": compTarget, "schema_id": data, "version": 1, "model": comp_pickle}]
    client["simulation_data"]["model"].insert_many(models)
    print("MODELS INSERTED")

#createModels("final", "passenger_final", "comp-target", "comp_amount", ["pass-result", "comp-target"],["pass-result"])