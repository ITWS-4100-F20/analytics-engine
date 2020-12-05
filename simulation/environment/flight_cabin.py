
import simpy

class FlightCabin(simpy.Resource):
    def __init__(self, env, cabinType: str, capacity: int, passengers:list):
        super(FlightCabin, self).__init__(env, capacity)
        self.cabinType = cabinType
        self.passengers = passengers