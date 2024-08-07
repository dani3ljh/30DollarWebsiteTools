import sys
import json
from pynput.keyboard import Key, Controller, Listener
import pyautogui

def onPress(key: Key, data: dict[str, str | int | dict | list], controller: Controller, useKeybinds: bool, useMacros: bool):
    if key == Key.left:
        posX = pyautogui.position()[0]
        if posX > data["minX"] and posX > data["maxX"]:
            return
        print("command left detected")
        pyautogui.moveRel(-data["xStep"], 0)
        if pyautogui.position()[0] >= data["minX"]:
            return
        pyautogui.moveRel(data["xStep"] * data["columns"], -data["yStep"])
        return

    if key == Key.right:
        posX = pyautogui.position()[0]
        if posX > data["minX"] and posX > data["maxX"]:
            return
        print("command right detected")
        pyautogui.moveRel(data["xStep"], 0)
        if pyautogui.position()[0] <= data["maxX"]:
            return
        pyautogui.moveRel(-data["xStep"] * data["columns"], data["yStep"])
        return

    if not hasattr(key, "char"):
        return

    for dataKey in data["keys"]:
        info = data["keys"][dataKey]

        if (key.char != dataKey or
            (not useKeybinds and info["type"] == "keybind") or
            (not useMacros   and info["type"] == "macro")):
                continue

        print(f"command {key.char} detected clicking at ({info['x']}, {info['y']})")

        originalPos = pyautogui.position()

        pyautogui.moveTo(info["x"], info["y"])
        pyautogui.click()

        if not info["clickCenter"]:
            pyautogui.moveTo(originalPos)
            continue
        
        pyautogui.click(450, 620)
        with controller.pressed(Key.ctrl):
            controller.press('a')
            controller.release('a')
        
        if not "value" in info:
            continue

        controller.press(Key.backspace)
        controller.release(Key.backspace)
        controller.type(info["value"])
        clickPos = data[info["clickAt"]]
        pyautogui.moveTo(clickPos["x"], clickPos["y"])
        pyautogui.click()
        pyautogui.moveTo(originalPos)
    
def onRelease(key):
    if key == Key.esc or key == Key.delete:
        print(f"{key} pressed, exiting")
        return False # stop listener

if __name__ == "__main__":
    args = sys.argv[1:]

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