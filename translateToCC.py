import sys
import json
from os import path

def getNoteFromNotes(notes: list[dict[str, str]], note: str) -> dict[str, str]:
    return next(i for i in notes if i["30DollarWebsiteSound"] == note)
    # return list(filter(lambda i: i["30DollarWebsiteSound"] == note, notes))

def getIntermedite(notes: list[dict[str, str]] , sounds: list[str]) -> tuple[list[dict[str, str | int | float]], list[str]]:
    intermedite: list[dict[str, str | int | float]] = []
    delay = 60/300
    soundList: list[str] = []
    openStartLoop = False
    startLoopIndex = -1

    for sound in sounds:
        sound = sound.strip()

        if sound == "": 
            continue
        
        components = sound.split("@")
        
        if "=" in components[-1]:
            parts = components[-1].split("=")
            repitions = parts[1]
            components[-1] = parts[0]
        else:
            repitions = 1
        
        if components[0] == "!divider":
            for _ in range(repitions):
                intermedite.append({ "type": "divider" })
        elif components[0] == "!combine":
            if len(intermedite) > 0 and "delay" in intermedite[-1]:
                intermedite[-1]["delay"] = 0
        elif components[0] == "!stop" or components[0] == "_pause":
            if len(components) == 1:
                count = repitions
            else:
                count = float(components[1]) * repitions
            
            intermedite.append({ "type": "pause", "value": delay * count })
        elif components[0] == "!speed":
            if len(components) == 1:
                raise Exception("Sound tempo missing arguments")
            
            tempo = float(components[1])

            if len(components) == 2:
                delay = 60 / tempo
            elif components[2] == "+":
                # convert delay into tempo, add tempo, convert back to delay
                delay = 60 / (60 / delay + tempo * repitions)
            elif components[2] == "x":
                # multiplying to tempo is equivilent to dividing delay
                delay /= tempo * repitions
            else:
                # if unknown mode default to set
                print(f"Unknown Speed Mode: {components[2]}, defaulting to set")
                delay = 60 / tempo
        elif components[0] == "!looptarget":
            if openStartLoop:
                # dont waste operations removing but still get rid of data
                intermedite[startLoopIndex] = {}
            else:
                openStartLoop = True

            startLoopIndex = len(intermedite)

            intermedite.append({ "type": "startLoop", "count": 0 })
        elif components[0] == "!loop" or components[0] == "!loopmany":
            if len(components) == 1:
                count = repitions
            else:
                count = int(components[1]) * repitions
            
            openStartLoop = False

            if startLoopIndex == -1:
                intermedite.insert(0, { "type": "startLoop", "count": count })
                startLoopIndex = 0
            else:
                intermedite[startLoopIndex]["count"] += count
            
            if intermedite[-1]["type"] == "endLoop":
                intermedite.pop()
            
            intermedite.append({ "type": "endLoop" })
        else:
            if (components[0].startswith("!")):
                raise Exception(f"Sound command {components[0]} not found")

            instrumentDict: dict[str, str] = getNoteFromNotes(notes, components[0])

            if not instrumentDict:
                raise Exception(f"Sound {components[0]} not found")
            
            instrument = instrumentDict["newSound"]

            if instrument not in soundList:
                soundList.append(instrument.strip())
                index = len(soundList)
            else:
                # lua is 1 indexed
                index = soundList.index(instrument) + 1

            value = int(components[1])
            for _ in range(repitions):
                intermedite.append({ "type": instrumentDict["type"], "instrument": index, "value": value, "delay": delay })
    
    return (intermedite, soundList)

def writeToOutput(preamble: str, outputFilePath: str, soundList: list[str], intermedite: list[dict[str, str | int | float]]):
    with open(outputFilePath, "w") as f:
        f.write("local instruments = { ")

        for sound in soundList:
            f.write("\"" + sound + "\", ")

        f.write("}\n" + preamble)

        for elem in intermedite:
            if "type" not in elem:
                print("empty elem")
                continue

            if elem["type"] == "note":
                f.write(f"playSound({elem["instrument"]}, {elem["value"]}, {elem["delay"]}, true)\n")
            elif elem["type"] == "sound":
                f.write(f"playSound({elem["instrument"]}, {elem["value"]}, {elem["delay"]}, true)\n")
            elif elem["type"] == "divider":
                f.write("\n")
            elif elem["type"] == "pause":
                f.write(f"sleep({elem["value"]})\n")
            elif elem["type"] == "startLoop":
                f.write(f"count = {elem["count"]}\nrepeat {{\n")
            elif elem["type"] == "endLoop":
                f.write(f"if count > 0 then\n\tcount = count - 1\nelse\n\tbreak\nend\n}}\n")

def translateToCC(data: dict[str, str | int | dict | list], inputFilePath: str, outputFilePath = "output.lua"):
    notes: list[dict[str, str]] = data["notesToCC"]

    preamble = """
local speaker = peripheral.wrap("top")

local function playSound(instrumentIndex, note, delay, isNote)
    if isNote then
        speaker.playNote(instruments[instrumentIndex], 1, note)
    else
        speaker.playSound(instruments[instrumentIndex], 1, note)
    end
    if delay > 0 then
        sleep(delay)
    end
end

""".lstrip()

    if not path.isfile(inputFilePath):
        raise Exception("input file path isn't a file")

    f = open(inputFilePath)
    sounds = f.read().split("|")
    f.close()

    print(f"Translating from {inputFilePath} to {outputFilePath}")

    (intermedite, soundList) = getIntermedite(notes, sounds)

    writeToOutput(preamble, outputFilePath, soundList, intermedite)

    print("Done")

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) < 2:
        raise TypeError("Usage: translateToCC <dataFilePath> <inputFilePath> [<outputFilePath>]")

    with open(args[0]) as f:
        data = json.load(f)

    if len(args) == 2:
        translateToCC(data, args[1])
    else:
        translateToCC(data, args[1], args[2])