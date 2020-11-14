from simulation.environment.compensation import Compensation
class OversaleData(object):
    def __init__(self, availableCompensationTypes: list[Compensation]):
        self.availableCompensationTypes = availableCompensationTypes
        self.finalized = False
        self.finalizeTimestamp = None
        self.solicitRankList = []
        self.pendingSolicitations = []
        self.rejectedSolicitations = []
