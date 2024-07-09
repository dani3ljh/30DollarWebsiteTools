import sys
import json
import pyautogui
from pynput.keyboard import Controller, Listener
from reassign import reassign
from combine import combine
import mouseBot

def on_press(key):
    mouseBot.on_press(
        key,
        data,
        controller,
        useKeybinds,
        useMacros
    )

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        raise Exception("No arguments provided")

    if args[0].lower() == "reassign":
        if len(args) == 1:
            raise Exception("Input file path argument not provided")
        if len(args) == 2:
            reassign(args[1])
        else:
            reassign(args[1], args[2])
    elif args[0].lower() == "mousebot":
        if len(args) == 1:
            raise Exception("Data json file path argument not provided")

        f = open(args[1])
        data = json.load(f)
        f.close()

        controller = Controller()

        useKeybinds = args[2].lower() == "true" if len(args) > 2 else True
        useMacros   = args[3].lower() == "true" if len(args) > 3 else True

        pyautogui.FAILSAFE = False

        with Listener(
                on_press=on_press,
                on_release=mouseBot.on_release) as listener:
            listener.join()
    elif args[0].lower() == "combine":
        if len(args) < 2:
            raise Exception("Input file path argumnts not provided")
        combine(args[1:])
    else:
        raise Exception("Tool not selected")