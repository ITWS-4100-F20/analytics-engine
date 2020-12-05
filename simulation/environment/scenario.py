class Scenario(object):
    def __init__(self, 
        oversaleStartTime: int, flightBoardingTime: int, 
        departureAirport: str, arrivalAirport: str,
        aircraftManifestID: int, cabins: dict, flightid: int, flightnum: int
    ):
        self.oversaleStartTime = oversaleStartTime
        self.flightBoardingTime = flightBoardingTime
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.aircraftManifestID = aircraftManifestID
        self.cabins = cabins
        self.flightid = flightid
        self.flightnum = flightnum

