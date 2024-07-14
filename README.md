# 30 Dollar Website

These are some tools I made for GD Colon's [$30 Website](https://thirtydollar.website/)

## How to Run
1. [install python](https://www.python.org/downloads/)
1. download this
1. run `py main.py` followed by a command name and any arguments
1. alternatively run `py <file>` with the same arguments

## Commands
- `reassign` \<inputFilePath\> [\<outputFilePath\>]
  - this will then ask for original sound, an optional new sound, and an optional transposition
  - default outputFilePath is `output.🗿`
- `mousebot` \<dataFilePath\> [\<useKeybinds\>] [\<useMacros\>]
- `combine` \<file1\> \<file2\> [\<file3\>...]
- `translateToCC` \<dataFilePath\> \<inputFilePath\> [\<outputFilePath\>]
  - translates $30 Website code to a computerCraft file that plays it on a speaker
  - wip only can handle tempo(set, add, mult), pause, silence, and loops(havent tested nor expect nested loops to work)
  - in mc can play either a noteblock sound or a mc audio file
  - to send to computerCraft put output into [pastebin](https://pastebin.com) then run `pastebin get <pastebinCode> <newFileName>` in your computer with a [speaker](https://tweaked.cc/peripheral/speaker.html) atop it
  - edit the dataFile to add notes by adding a dict in the list `notesToCC`
  - default outputFilePath is `output.lua`