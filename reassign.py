from os import path

def reassign(inputFilePath, outputFilePath = "output.🗿"):
    if not path.isfile(inputFilePath):
        raise Exception("input file path isn't a file")
    
    originalSound = input("Original Sound: ")
    if not originalSound: return

    newSound = input("New Sound: ")
    if not newSound: return

    transposition = input("Transposition: ") or "0"
    transposition = int(transposition)

    f = open(inputFilePath)
    sounds = f.read().split("|")
    f.close()


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

            components = sound.strip().split("@")

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