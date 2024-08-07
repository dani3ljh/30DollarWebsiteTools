import sys
import json
import pyautogui
from pynput.keyboard import Controller, Listener
from reassign import reassign
from mouseBot import onPress, onRelease
from combine import combine
from translateToCC import translateToCC

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        raise TypeError("No arguments provided")
    
    command = args[0].lower()

    args = args[1:]

    match command.lower():
        case "reassign":
            if len(args) == 0:
                raise TypeError("Usage: reassign <inputFilePath> [<outputFilePath>]")
            elif len(args) == 1:
                reassign(args[0])
            else:
                reassign(args[0], args[1])
        case "mousebot":
            if len(args) == 0:
                raise TypeError("Usage: mousebot <dataFilePath> [<useKeybinds>] [<useMacros>]")

            with open(args[0]) as f:
                data = json.load(f)

            controller = Controller()

            useKeybinds = args[1].lower() == "true" if len(args) > 1 else True
            useMacros   = args[2].lower() == "true" if len(args) > 2 else True

            pyautogui.FAILSAFE = False

            with Listener(
                    on_press=lambda key: onPress(key, data, controller, useKeybinds, useMacros),
                    on_release=onRelease) as listener:
                listener.join()
        case "combine":
            if len(args) < 1:
                raise TypeError("Usage: combine <file1> <file2> [<file3>...]")
            
            combine(args)
        case "translatetocc":
            if len(args) < 2:
                raise TypeError("Usage: translateToCC <dataFilePath> <inputFilePath> [<outputFilePath>]")

            with open(args[0]) as f:
                data = json.load(f)

            if len(args) == 2:
                translateToCC(data, args[1])
            else:
                translateToCC(data, args[1], args[2])
        case _:
            raise TypeError("Command not selected")