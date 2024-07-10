from os import path

preamble = """
local speaker = peripheral.wrap("top")

local function playSound(instrumentIndex, note, delay)
    speaker.playNote(instruments[instrumentIndex], note)
    if delay > 0 then
        os.sleep(delay)
    end
end

""".lstrip()

def translate(data: dict[str, str | int | dict], inputFilePath: str, outputFilePath = "output.lua"):
    notesDict: dict[str, str] = data["notesToCC"]

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
            if "delay" in res[-1]:
                res[-1].delay = 0
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
        elif components[0].startswith("!") or components[0] not in notesDict:
            raise Exception(f"Sound {components[0]} not found")
        else:
            instrument = notesDict[components[0]]
            if instrument not in internalSounds:
                internalSounds.append(instrument.strip())
                index = len(internalSounds)
            else:
                # lua is 1 indexed
                index = internalSounds.index(instrument) + 1
            parts = components[1].split("=")
            value = int(parts[0])
            amount = int(parts[1]) if len(parts) > 1 else 1
            for _ in range(amount):
                res.append({ "type": "note", "instrument": index, "value": value, "delay": delay })

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
                f.write(f"playSound({elem["instrument"]}, {elem["value"]}, {elem["delay"]})\n")
            elif elem["type"] == "pause":
                f.write(f"os.sleep({value})\n")

    print("Done")