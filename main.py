from toolboxDataCollector import UserData as User
import json

class IdleonSamplingTool:
    def __init__(self) -> None:
        user = User()

        # ask for refinery mobs and vial mats here
        self.refineryMobs = self.checkRefineryMobs()
        self.vialMats = self.getVialMats()
        self.charSamples = user.sample(self.vialMats, self.refineryMobs)
        
        print(json.dumps(self.charSamples, indent=4))
    
    def checkRefineryMobs(self):
        refineryMobs = input("Would you like to sample mobs for refinery? (SporeCap, BullfrogHorn, PocketSand, FloofPloof, CrackedGlass, ContactLense)\n> ")
        if refineryMobs in ["True", "Yes", "Y"]: return True
        else: return False

    def getVialMats(self):
        vialMats = input("Which vials would you like to focus samples on? Type them separated by commas. If you do not have any vials you wish to focus on, press enter.\n> ")
        if vialMats == "": return []
        else:
            return vialMats.split(", ")

if __name__ == "__main__":
    IdleonSamplingTool()