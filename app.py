#this will be used to host the FLASK api server
import time
from simulation import simulation
from simulation.environment.scenario import Scenario

def startSim():
    startTime = time.strptime("12/01/2020 01:00:00", "%d/%m/%Y %H:%M:%S")
    endTime = time.strptime("12/01/2020 22:00:00", "%d/%m/%Y %H:%M:%S")
    testScenario = Scenario(time.mktime(startTime), time.mktime(endTime), "EWR", "ALB", 1)
    simulation.runSimulation(testScenario)

if __name__ == '__main__':
    startSim()