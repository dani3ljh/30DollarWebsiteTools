import sys
from reassign import reassign

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        raise Exception("No arguments provided")

    if args[0] == "reassign":
        if len(args) == 1:
            raise Exception("Input file path argument not provided")
        if len(args) == 2:
            reassign(args[1])
        else:
            reassign(args[1], args[2])
    else:
        raise Exception("Tool not selected")