import sys
from reassign import reassign
from pynput.keyboard import Controller, Listener
import mouseBot
import json
import pyautogui

def on_press(key):
    mouseBot.on_press(key, data, controller)

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
            raise Exception("Key To Coordinates json file path argument not provided")

        f = open(args[1])
        data = json.load(f)
        f.close

        controller = Controller()

        pyautogui.FAILSAFE = False

        with Listener(
                on_press=on_press,
                on_release=mouseBot.on_release) as listener:
            listener.join()
    else:
        raise Exception("Tool not selected")