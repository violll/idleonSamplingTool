import json
import pickle
import copy

class UserData():
    def __init__(self) -> None:
        self.userData = json.load(open('data.json'))
        self.toolboxKeys = json.load(open('toolboxKeys.json'))
        
        # character names
        charNames = self.userData['charNames']

        # character classes
        self.chars = {charNames[i]: copy.deepcopy(self.toolboxKeys["classesKey"][str(self.userData['data']['CharacterClass_' + str(i)])]) for i in range(len(charNames))}

        # 3d printer slots data
        printer = [d for d in eval(self.userData['data']['Print']) if type(d) != int and d != 'Blank']
        self.nPrinterSlots = len(printer)//len(charNames)

        # sampling resources available to the player based on what is in their inventory
        # assumes the inventory is autosorted 
        # could make the initial resource list based on wiki data, but it is not yet updated for w6
        storage = self.userData['data']['ChestOrder']

        self.ores = storage[:storage.index('CopperBar')]
        self.logs = [self.toolboxKeys["logsKey"][log] for log in storage if ("Tree" in log or "Foal" in log) and "Interior" not in log]
        self.bugs = [self.toolboxKeys["bugsKey"][bug] for bug in storage if "Bug" in bug]
        self.fish = [self.toolboxKeys["fishKey"][fish] for fish in storage if "Fish" in fish and "Food" not in fish]

        self.sample()

    def sample(self, vials=["HermitCan", "SporeCap", "MapleLogs", "SnakeSkin"]):
        # add mats/mobs to assigned once they are checked off
        assigned = set()

        # assign refinery
        ## refinery mobs
        ## assumes there is one character assigned to RefineryMobs and they have enough sample slots
        char = [self.chars[char] for char in self.chars if self.chars[char]["SampleRole"] == "RefineryMobs"][0]
        char["Samples"].extend(self.toolboxKeys["refineryMobs"])

        ## refinery mats
        for mat in self.toolboxKeys["refineryMats"]: 
            matType = self.getMatType(mat)
            char = [self.chars[char] for char in self.chars if self.chars[char]["SampleRole"] == matType and len(self.chars[char]["Samples"]) < self.nPrinterSlots][-1]
            char["Samples"].append(mat)

            if mat not in vials and mat not in self.toolboxKeys["atomMatSources"]:
                assigned.add(mat)

        # assign atom generating mats
        for mat in self.toolboxKeys["atomMatSources"]:
            matType = self.getMatType(mat)
            chars = [self.chars[char] for char in self.chars if self.chars[char]["SampleRole"] == matType and len(self.chars[char]["Samples"]) < self.nPrinterSlots and mat not in self.chars[char]["Samples"]]
            for char in chars: char["Samples"].append(mat)

            assigned.add(mat)
                
        # assign vials
        for mat in vials:
            matType = self.getMatType(mat)
            chars = [self.chars[char] for char in self.chars if matType in self.chars[char]["SampleRole"] and len(self.chars[char]["Samples"]) < self.nPrinterSlots and mat not in self.chars[char]["Samples"]]
            for char in chars: char["Samples"].append(mat)

            assigned.add(mat)
            
        # assign remaining resources
        for mat in [x for x in self.logs + self.ores + self.fish + self.bugs if x not in assigned]:
            # print(mat)
            matType = self.getMatType(mat)
            try: 
                char = [self.chars[char] for char in self.chars if self.chars[char]["SampleRole"] == matType and len(self.chars[char]["Samples"]) < self.nPrinterSlots][-1]
                # print(char)
                if char != {}: char["Samples"].append(mat)
                assigned.add(mat)
            except: 
                continue
            
        # assign alchemy mats -- for hourly clicking or future vials
        for mat in self.toolboxKeys["miscMats"]:
            matType = self.getMatType(mat)
            chars = [self.chars[char] for char in self.chars if matType in self.chars[char]["SampleRole"] and len(self.chars[char]["Samples"]) < self.nPrinterSlots and mat not in self.chars[char]["Samples"]]
            for char in chars: char["Samples"].append(mat)

            assigned.add(mat)
        
        # checking
        print(set(self.logs + self.ores + self.fish + self.bugs).difference(assigned))
        print(json.dumps(self.chars, indent=4))
        for char in self.chars: 
            if len(self.chars[char]["Samples"]) < self.nPrinterSlots:
                print(char)

    def getMatType(self, mat):
        if mat in self.ores: return "Mining"
        elif mat in self.logs: return "Choppin"
        elif mat in self.bugs: return "Catching"
        elif mat in self.fish: return "Fishing"
        else: return "Mobs"

    def saveJSON(self):
        dump = json.dumps(self.userData, indent=4)

        with open('data.json', 'w') as f:
            f.write(dump)
            f.close()
    
    def savePKL(self, obj, f):
        with open(f, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

UserData()