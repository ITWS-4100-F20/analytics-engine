import simpy
class SolicitationOffer(object):
    def __init__(self, passengerID: int, compensationKeyword: str, compensationAmount: any, offerTimestamp: simpy.SimTime):
        self.passengerID = passengerID
        self.compensationKeyword = compensationKeyword
        self.compensationAmount = compensationAmount
        self.offerTimestamp = offerTimestamp
        self.offerResponded = False
        self.responseTimestamp = None
        self.responseResult = 'pending'