class Scenario(object):
    def __init__(self, 
        oversaleStartTime: int, flightBoardingTime: int, 
        departureAirport: str, arrivalAirport: str,
        aircraftManifestID: int
    ):
        self.oversaleStartTime = oversaleStartTime
        self.flightBoardingTime = flightBoardingTime
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.aircraftManifestID = aircraftManifestID

