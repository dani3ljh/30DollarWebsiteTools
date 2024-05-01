from os import path

def combine(arrOfInputFilePaths, outputPath = "output.🗿"):
    print("combining files")
    output = ""
    for inputFilePath in arrOfInputFilePaths:
        if not path.isfile(inputFilePath):
            raise Exception("input file path isn't a file")
        output += "|"
        f = open(inputFilePath)
        output += f.read()
        f.close()
    with open(outputPath, "w") as f:
        f.write(output[1:]) # remove first |