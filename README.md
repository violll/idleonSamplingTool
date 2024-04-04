# idleonSamplingTool
This is a tool for the game [Legends of Idleon](https://www.legendsofidleon.com/) and generates a list of 3d printer samples for each of your characters.
## Quick Start
Copy and paste your IdleonToolbox raw data into the data.json file.

Run the main.py file. 

A command line will prompt you if you'd like to take samples for the mobs that fuel the refinery (listed in the toolboxKeys.json file as `refineryMobs`). Type "True", "Yes", or "Y" to indicate yes, anything else to indicate no. 

The command line will then prompt you again to ask if there are any vials for which you would like to focus on samples. Typing in the names of mats here will prioritize them in the sampling algorithm. Skilling samples must be typed using the syntax found in the toolboxKeys.json file, under `logsKey`, `bugsKey`, and `fishKey`. For ores, the name of the ore is correct syntax, aside from the shortening of "Platinum" to "Plat".

The `miscMats` key in the `toolboxKeys.json` file has additional space to take or prioritize samples; replace the samples there to add skilling mats you would like to prioritize or mobs you would like to sample.

## The Algorithm
The IdleonToolbox JSON data is needed for two reasons:
1. To determine the class spread of your characters, as samples are assigned based on said class. This is notated in the `classesKey` key of the `toolboxKeys.json` file. If you use a different setup for your samples, feel free to change the `SampleRole` for each class. 
2. To determine which skilling resources you can sample. **Your inventory MUST be autosorted for this feature to work.**

After user input is taken and all desired samples are defined, as described in the Quick Start section above, the sampling algorithm does its work. 

First, if the user wanted to sample refinery mobs mats, those are added to the characters with classes assigned to sample them. **This assumes that at least one class is assigned this sampling role, and that they have at minimum, six sample slots required to sample each mob.** Each mat is assigned one slot for only one character, the reasoning being that refinery demands are relatively low and heavily timegated by rank-ups.

Next, skilling mats for refinery are assigned to the relevant characters (choppin for mages, catching for archers, etc.). Each mat is assigned one slot for only one character, the reasoning being that refinery demands are relatively low and heavily timegated by rank-ups.

Then, the big mats for atom generation are assigned (these are OakLogs and Copper, as listed in the `atomMatSources` key in `toolboxKeys.json`... feel free to change these if you don't want to include copper). These are assigned first and to each relevant character, because maximizing atom production is incredibly important for advancing alchemy. 

Next, vials are assigned, in a similar fashion, to each relevant character to speed up the time required to generate 1000M to max out said vial.

The remaining skilling mats are assigned, one mat is given one sample slot in one relevant character.

Finally, if there are any sampling slots left over, the mats listed in the `miscMats` key in `toolboxKeys.json` are assigned as follows: one mat is given one slot in each relevant character.

## Limitations 
I have bolded the major assumptions I have made in the current tool's algorithm. Below are smaller assumptions/limitations that the tool has, that may be fixed in a future update.
- Currently, only the highest-level classes are listed in `toolboxKeys.json`. Therefore, the tool will not currently work for players who have not yet unlocked them.
- While the tool asks if you'd like to sample mob mats for refinery, it does not ask if you would like to sample skilling mats for refinery... it just assigns them anyway. An easy fix...
- This tool assumes you are at the point where you can generate atoms
- It is possible that not all sample slots will be filled on all characters after the algorithm is completed; that is the purpose of `miscMats`. 
- It is also possible that not all resource materials will be sampled, due to sample slot limits.
