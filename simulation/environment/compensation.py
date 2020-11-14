
class Compensation(object):
    def __init__(self, compensationCategory: str, compensationKeywords: list[str], compensationType: str ):
        self.compensationCategory = compensationCategory
        self.compensationKeyword = compensationKeywords
        #Compensation Type refers to if the data is Continuous (CONT) or Discrete(DISC)
        self.compensationType = compensationType

        @classmethod
        def setAmount(self, amount):
            self.amount = amount

defaultCompensationList = [
    Compensation("COMP", ["AGT_COMP", "COMP"], "CONT"),
    Compensation("MILES", ["MILES", "AGT_MILES"], "CONT"),
    Compensation("MEAL", ["MEAL_B", "MEAL_L", "MEAL_D"], "DISC"),
    Compensation("TRANS", ["TRANS"], "DISC"),
    Compensation("HOTEL", ["HOTEL"], "DISC"),
] 