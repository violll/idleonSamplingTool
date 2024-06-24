import json
import pickle
import copy
import random

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

        self.mats = {
            "Mining": self.ores,
            "Choppin": self.logs, 
            "Catching": self.bugs,
            "Fishing": self.bugs
            }
        
        # add mats to assigned once they are checked off
        self.assigned = set()

    def sample(self, vials, sampleRefineryMobs):
        # assign refinery
        ## refinery mobs
        ## assumes there is one character assigned to RefineryMobs and they have enough sample slots
        if sampleRefineryMobs:
            char = [self.chars[char] for char in self.chars if self.chars[char]["SampleRole"] == "RefineryMobs"][0]
            char["Samples"].extend(self.toolboxKeys["refineryMobs"])

        ## refinery mats
        # for mat in self.toolboxKeys["refineryMats"]: 
        #     matType = self.getMatType(mat)
        #     char = random.choice([self.chars[char] for char in self.chars if self.chars[char]["SampleRole"] == matType and len(self.chars[char]["Samples"]) < self.nPrinterSlots and mat not in self.chars[char]["Samples"]])
        #     char["Samples"].append(mat)

        #     if mat not in vials and mat not in self.toolboxKeys["atomMatSources"]:
        #         assigned.add(mat)

        # assign all sample mats
        for matType in ["Mining", "Choppin", "Fishing", "Catching"]:
            relevantChars = [self.chars[char] for char in self.chars if self.chars[char]["SampleRole"] == matType]
            mats = self.mats[matType]

            # determine how many extra slots are available for doubling up on samples
            if len(relevantChars) * self.nPrinterSlots < len(mats): leftoverSlots = -1
            else: leftoverSlots = (len(relevantChars) * self.nPrinterSlots) % len(mats)

            atomSources = [mat for mat in self.toolboxKeys["atomMatSources"] if self.getMatType(mat) == matType]
            currVials = [mat for mat in vials if self.getMatType(mat) == matType]
            hourlyClickMats = self.toolboxKeys["hourlyClicks"]["all"][matType]
            
            # do something here -- figure out which samples to avoid
            # assign atom mats first, then any vials, then hourlyclickmats
            if leftoverSlots < 0: 
                pass
            
            # assign leftover slots
            if leftoverSlots > 0:
                # atom source
                leftoverSlots = self.assignN(relevantChars, atomSources, leftoverSlots, len(relevantChars))

                # vials
                leftoverSlots = self.assignN(relevantChars, currVials, leftoverSlots, len(relevantChars))

                # TODO more slots available...
                if leftoverSlots > 0: print("still {} more slots!".format(leftoverSlots))

            # assign mats used for hourly clicks
            for mat in hourlyClickMats:
                if mat not in self.assigned: self.assignN([char for char in relevantChars if len(char["Samples"]) < self.nPrinterSlots], [mat])
            
            # assign remaining mats
            for mat in mats:
                if mat not in self.assigned: 
                    self.assignN([char for char in relevantChars if len(char["Samples"]) < self.nPrinterSlots], [mat])
        
        return self.chars
    
    def assignN(self, chars, mats, leftoverSlots=100000, k = 1):
        for mat in mats:
            if leftoverSlots <= 0: break
            
            for char in random.sample(chars, k): 
                if leftoverSlots <= 0: break
                char["Samples"].append(mat)
                if mat in self.assigned: leftoverSlots -= 1
                else: self.assigned.add(mat)

        return leftoverSlots

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
