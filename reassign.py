import sys
from os import path

def combineComponents(components: list[str]) -> str:
    resSound = "|"

    for component in components:
        resSound += component + "@"

    return resSound[:-1] #remove last @

def reassign(inputFilePath: str, outputFilePath = "output.🗿"):
    if not path.isfile(inputFilePath):
        raise Exception("input file path isn't a file")
    
    originalSound = input("Original Sound: ")
    if not originalSound: return

    newSound = input("New Sound: ") or originalSound

    transposition = input("Transposition: ") or "0"
    transposition = int(transposition)

    f = open(inputFilePath)
    sounds = f.read().split("|")
    f.close()


    print(f"Reassigning {originalSound} to {newSound} with a transposition of {transposition} to file {outputFilePath}")

    with open(outputFilePath, "w") as f:
        for sound in sounds:
            sound = sound.strip()

            if sound == "": 
                continue
            
            if sound == "!divider":
                f.write("|!divider\n")
                continue

            components = sound.split("@")

            if components[0] != originalSound:
                f.write(combineComponents(components))
                continue

            components[0] = newSound

            if transposition == 0:
                f.write(combineComponents(components))
                continue

            if len(components) == 1:
                components += "0"

            newAmount = int(components[1]) + transposition
            components[1] = str(newAmount)

            if newAmount == 0:
                components.pop() # remove the @0
            
            f.write(combineComponents(components))

    print("Done")

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        raise TypeError("Usage: reassign <inputFilePath> [<outputFilePath>]")
    elif len(args) == 1:
        reassign(args[0])
    else:
        reassign(args[0], args[1])