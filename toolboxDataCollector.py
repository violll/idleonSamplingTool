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
            "Fishing": self.fish
            }
        
        # add mats to assigned once they are fully assigned
        self.assigned = set()

    def sample(self, vials, sampleRefineryMobs):
        # assign mobs
        if sampleRefineryMobs:
            refinaryChars = [self.chars[char] for char in self.chars if self.chars[char]["SampleRole"] == "RefineryMobs"]
            self.assignN(refinaryChars, self.toolboxKeys["refineryMobs"])
        
        mobChars = [self.chars[char] for char in self.chars if "Mobs" in self.chars[char]["SampleRole"]]
        mobVials = [mob for mob in vials if self.getMatType(mob) == "Mobs"]

        self.assignN(mobChars, mobVials, True)

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
            
            # no leftover slots: assign refinery, atom mats, and vials
            if leftoverSlots < 0: 
                refineryMats = [mat for mat in self.toolboxKeys["refineryMats"] if self.getMatType(mat) == matType and mat not in self.assigned]
                self.assignK(relevantChars, refineryMats)
                self.assignN(relevantChars, atomSources)
                self.assignN(relevantChars, currVials)
            
            # assign leftover slots to atoms mats and vials
            if leftoverSlots > 0:
                leftoverSlots = self.assignK(relevantChars, atomSources, leftoverSlots, len(relevantChars))
                leftoverSlots = self.assignK(relevantChars, currVials, leftoverSlots, len(relevantChars))

            # assign mats used for hourly clicks
            self.assignN(relevantChars, hourlyClickMats)
            
            # assign remaining mats
            self.assignN(relevantChars, mats)

            # if there are still leftover slots available, fill in the blanks with extra mats that could be hourly clickable
            if leftoverSlots > 0:
                self.assignN(relevantChars, hourlyClickMats, True)
                        
        return self.chars
    
    # assigns each mat in mats to k characters, stops assigning when extra slots are gone
    def assignK(self, chars, mats, leftoverSlots=100000, k = 1):
        for mat in mats:
            if leftoverSlots <= 0: break
            
            for char in random.sample(chars, k): 
                if leftoverSlots <= 0: break
                char["Samples"].append(mat)
                if mat in self.assigned: leftoverSlots -= 1
                else: self.assigned.add(mat)

        return leftoverSlots
    
    # assigns each mat in mats to one character until all slots are uniquely filled
    def assignN(self, chars, mats, ignoreAssigned = False):
        for char in chars:
            remainingSlots = self.nPrinterSlots - len(char["Samples"])

            i = 0
            while remainingSlots > 0:
                if i >= len(mats): break

                mat = mats[i]
                if mat not in self.assigned or (ignoreAssigned and mat not in char["Samples"]):
                    char["Samples"].append(mat)
                    self.assigned.add(mat)
                    remainingSlots -= 1
                i += 1

        return

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
