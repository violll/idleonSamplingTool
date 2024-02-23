from toolboxDataCollector import UserData as User

class IdleonSamplingTool:
    def __init__(self) -> None:
        user = User()

        # ask for refinery and vial mobs here
        self.refinery = self.checkRefineryMobs()
    
    def checkRefineryMobs(self):
        refineryMobs = input("Would you like to sample mobs for refinery? (GMush, Bullfrog, Sand, Sheep, Thermometer, Neptuneeyes)\n> ")
        if refineryMobs in ["True", "Yes", "Y"]: return True
        else: return False

if __name__ == "__main__":
    IdleonSamplingTool()