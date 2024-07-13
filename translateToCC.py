import sys
import json
from os import path

preamble = """
local speaker = peripheral.wrap("top")

local function playSound(instrumentIndex, note, delay, isNote)
    if isNote then
        speaker.playNote(instruments[instrumentIndex], 1, note)
    else
        speaker.playSound(instruments[instrumentIndex], 1, note)
    end
    if delay > 0 then
        os.sleep(delay)
    end
end

""".lstrip()

def getNoteFromNotes(notes: list[dict[str, str]], note: str) -> dict[str, str]:
    return next(i for i in notes if i["30DollarWebsiteSound"] == note)
    # return list(filter(lambda i: i["30DollarWebsiteSound"] == note, notes))

def translateToCC(data: dict[str, str | int | dict | list], inputFilePath: str, outputFilePath = "output.lua"):
    notes: list[dict[str, str]] = data["notesToCC"]

    if not path.isfile(inputFilePath):
        raise Exception("input file path isn't a file")

    f = open(inputFilePath)
    sounds = f.read().split("|")
    f.close()

    print(f"Translating from {inputFilePath} to {outputFilePath}")

    res: list[dict[str, str | int | float]] = []
    delay = 60/300
    internalSounds: list[str] = []

    for sound in sounds:
        sound = sound.strip()

        if sound == "": 
            continue
        
        components = sound.split("@")
        
        if components[0] == "!divider":
            res.append({ "type": "divider" })
        elif components[0] == "!combine":
            if len(res) > 0 and "delay" in res[-1]:
                res[-1]["delay"] = 0
        elif components[0] == "_pause":
            res.append({ "type": "pause", "value": delay })
        elif components[0] == "!stop":
            if len(components) == 1:
                continue
            res.append({ "type": "pause", "value": delay * float(components[1])})
        elif components[0] == "!speed":
            if len(components) == 1:
                raise Exception("Sound tempo missing arguments")
            tempo = float(components[1])
            if len(components) == 2:
                delay = 60 / tempo
            elif components[2] == "+":
                # convert delay into tempo, add tempo, convert back to delay
                delay = 60 / (60 / delay + tempo)
            elif components[2] == "x":
                # multiplying to tempo is equivilent to dividing delay
                delay /= tempo
            else:
                # if unknown mode default to delay
                print(f"Unknown Speed Mode: {components[2]}, defaulting to set")
                delay = 60 / tempo
        else:
            if (components[0].startswith("!")):
                raise Exception(f"Sound command {components[0]} not found")

            instrumentDict: dict[str, str] = getNoteFromNotes(notes, components[0])

            if not instrumentDict:
                raise Exception(f"Sound {components[0]} not found")
            
            instrument = instrumentDict["newSound"]

            if instrument not in internalSounds:
                internalSounds.append(instrument.strip())
                index = len(internalSounds)
            else:
                # lua is 1 indexed
                index = internalSounds.index(instrument) + 1

            if len(components) == 1:
                parts = [0, 1]
            else:
                parts = components[1].split("=")

            value = int(parts[0])
            amount = int(parts[1])
            for _ in range(amount):
                res.append({ "type": instrumentDict["type"], "instrument": index, "value": value, "delay": delay })

    with open(outputFilePath, "w") as f:
        f.write("local instruments = { ")
        for sound in internalSounds:
            f.write("\"" + sound + "\", ")
        f.write("}\n")
        f.write(preamble)
        for elem in res:
            # if "type" not in elem:
                # print(elem)
            if elem["type"] == "divider":
                f.write("\n")
            elif elem["type"] == "note":
                f.write(f"playSound({elem["instrument"]}, {elem["value"]}, {elem["delay"]}, true)\n")
            elif elem["type"] == "sound":
                f.write(f"playSound({elem["instrument"]}, {elem["value"]}, {elem["delay"]}, true)\n")
            elif elem["type"] == "pause":
                f.write(f"sleep({elem["value"]})\n")

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