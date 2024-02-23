import json
import pickle

class UserData():
    def __init__(self) -> None:
        self.userData = json.load(open('data.json'))
        self.toolboxKeys = json.load(open('toolboxKeys.json'))
        
        # character names
        self.charNames = self.userData['charNames']

        # character classes
        self.charClasses = [self.toolboxKeys["classesKey"][str(self.userData['data']['CharacterClass_' + str(i)])] for i in range(len(self.charNames))]

        # 3d printer slots data
        printer = [d for d in eval(self.userData['data']['Print']) if type(d) != int and d != 'Blank']
        self.nPrinterSlots = len(printer)//len(self.charNames)

        # sampling resources available to the player based on what is in their inventory
        # assumes the inventory is autosorted 
        # could make the initial resource list based on wiki data, but it is not yet updated for w6
        storage = self.userData['data']['ChestOrder']

        self.ores = storage[:storage.index('CopperBar')]
        self.logs = [self.toolboxKeys["logsKey"][log] for log in storage if ("Tree" in log or "Foal" in log) and "Interior" not in log]
        self.bugs = [self.toolboxKeys["bugsKey"][bug] for bug in storage if "Bug" in bug]
        self.fish = [self.toolboxKeys["fishKey"][fish] for fish in storage if "Fish" in fish and "Food" not in fish]

    def saveJSON(self):
        dump = json.dumps(self.userData, indent=4)

        with open('data.json', 'w') as f:
            f.write(dump)
            f.close()
    
    def savePKL(self, obj, f):
        with open(f, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)