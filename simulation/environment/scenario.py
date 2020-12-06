import uuid

class Scenario(object):
    def __init__(self, 
        oversaleStartTime: int, flightBoardingTime: int, 
        departureAirport: str, arrivalAirport: str,
        aircraftManifestID: int, cabins: dict, flightnum: int
    ):
        self.uuid = str(uuid.uuid1())
        self.oversaleStartTime = oversaleStartTime
        self.flightBoardingTime = flightBoardingTime
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.aircraftManifestID = aircraftManifestID
        self.cabins = cabins
        self.flightnum = flightnum

