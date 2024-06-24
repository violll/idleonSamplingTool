# idleonSamplingTool
This is a tool for the game [Legends of Idleon](https://www.legendsofidleon.com/) and generates a list of 3d printer samples for each of your characters.
## Quick Start
Copy and paste your IdleonToolbox raw data into the data.json file.

Run the main.py file. 

A command line will prompt you if you'd like to take samples for the mobs that fuel the refinery (listed in the toolboxKeys.json file as `refineryMobs`). Type "True", "Yes", or "Y" to indicate yes, anything else to indicate no. 

The command line will then prompt you again to ask if there are any vials for which you would like to focus on samples. Typing in the names of mats here will prioritize them in the sampling algorithm. Skilling samples must be typed using the syntax found in the toolboxKeys.json file, under `logsKey`, `bugsKey`, and `fishKey`. For ores, the name of the ore is correct syntax, aside from the shortening of "Platinum" to "Plat".

## The Algorithm
The IdleonToolbox JSON data is needed for two reasons:
1. To determine the class spread of your characters, as samples are assigned based on said class. This is notated in the `classesKey` key of the `toolboxKeys.json` file. If you use a different setup for your samples, feel free to change the `SampleRole` for each class. 
2. To determine which skilling resources you can sample. **Your inventory MUST be autosorted for this feature to work.**

After user input is taken and all desired samples are defined, as described in the Quick Start section above, the sampling algorithm does its work. 

First, if the user wanted to sample mobs used in refinery, those are added to the characters with classes assigned to sample them. **If you want all mobs to be sampled, ensure the characters you have assigned this sampling role have, at minimum, six sample slots between them, which is required to sample all mobs.** Each mat is assigned one slot for only one character, the reasoning being that refinery demands are relatively low and heavily timegated by rank-ups.

If the user included any mobs in the list of vials they would like to be sampled, they will be added to any character with sample role of `VialMobs` or `RefineryMobs` (if sample slots still remain). Character with these sample roles will only have all sample slots filled if enough mobs are provided by the user input as mentioned above. 

Next, skilling mats are assigned in the general order as follows:
1. Refinery (only if there are not enough characters to sample all unique nodes of a skill)
2. Atom sources (these are listed in the `atomMatSources` key in `toolboxKeys.json`... feel free to change these)
3. Vials (if these are provided in the user input)
4. Mats that are potentially hourly clickable in alchemy
5. All other mats

### The Details: Mat Assignment
If you do not have enough character sample slots to sample each unique variety of a skill, the algorithm is slightly different. It will follow the priority of the list above, starting with refinery mats, but each resource will be assigned to only one slot. Once the slots are filled, no more mats from that skill can be assigned for sampling. 

If there are extra character sample slots, then the list begins at atom sources. It will assign atom source and vial mats until there are no extra sample slots left (or all possible atom and vial mats have been assigned). This means that multiple characters will be assigned these slots, to speed up resource generation when trying to max out vials or generate more atoms. The rest of the mats on the list are assigned to one character's slot.

In the case that there are still extra sample slots remaining after all mats are assigned, the hourly clickable mats will fill in the remaining gaps (see the list of hourly clickable mats in the `hourlyClicks` key in `toolboxKeys.json`. Note there are two nested dictionaries, one for all hourly clickable mats (`all`), and one for the bubbles that are linear in alchemy (`linear`). This program uses `all` by default. 

## Limitations 
I have bolded the major assumptions I have made in the current tool's algorithm. Below are smaller assumptions/limitations that the tool has, that may be fixed in a future update.
- Currently, only the highest-level classes are listed in `toolboxKeys.json`. Therefore, the tool will not currently work for players who have not yet unlocked them.
- While the tool asks if you'd like to sample mob mats for refinery, it does not ask if you would like to sample skilling mats for refinery... if you have enough sample slots, this is not an issue.
- This tool assumes you are at the point where you are able to generate atoms (and therefore should be prioritizing them)
- It is possible that not all resource materials will be sampled, due to sample slot limits.
