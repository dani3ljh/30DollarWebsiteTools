from os import path
import sys

def reassign(inputText, outputFilePath):
    originalSound = input("Original Sound: ")
    if not originalSound: return

    newSound = input("New Sound: ")
    if not newSound: return

    transposition = input("Transposition: ") or "0"
    transposition = int(transposition)

    sounds = inputText.split("|")

    print(f"Reassigning {originalSound} to {newSound} with a transposition of {transposition} to file {outputFilePath}")

    with open(outputFilePath, "w") as f:
        def writeComponents(components):
            resSound = "|"

            for component in components:
                resSound += component
                resSound += "@"

            f.write(resSound[:-1]) #remove last @
        
        for sound in sounds:
            if sound == "": 
                continue

            components = sound.split("@")

            if components[0] != originalSound:
                writeComponents(components)
                continue

            components[0] = newSound

            if transposition == 0:
                writeComponents(components)
                continue

            if len(components) == 1:
                components += "0"

            newAmount = int(components[1]) + transposition
            components[1] = str(newAmount)

            if newAmount == 0:
                components.pop() # remove the @0
            
            writeComponents(components)
    print("Done")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0 or not path.isfile(sys.argv[0]):
        raise Exception("input file path not found")
    inputFilePath = args[0]
    if len(args) == 1:
        outputFilePath = "output.🗿"
    else:
        outputFilePath = args[1]
    
    f = open(inputFilePath)
    inputText = f.read()
    f.close()

    reassign(inputText, outputFilePath)