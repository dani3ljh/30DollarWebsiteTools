import sys
from reassign import reassign
from pynput import keyboard
import mouseBot
import json
import pyautogui

def on_press(key):
    mouseBot.on_press(key, data)

def on_release(key):
    mouseBot.on_release(key, data)

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
    elif args[0] == "mouseBot":
        if len(args) == 1:
            raise Exception("Key To Coordinates json file path argument not provided")

        f = open(args[1])
        data = json.load(f)
        f.close

        pyautogui.FAILSAFE = False

        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()
    else:
        raise Exception("Tool not selected")