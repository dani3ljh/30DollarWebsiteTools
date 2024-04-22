from pynput import keyboard
import pyautogui
import sys
import json

def on_press(key):
    if not hasattr(key, "char"):
        return
    for dataKey in data:
        if key.char == dataKey:
            coords = data[dataKey]
            print(f"command {key.char} detected clicking at ({coords['x']}, {coords['y']})")
            originalPos = pyautogui.position()
            pyautogui.moveTo(coords)
            pyautogui.click()
            pyautogui.moveTo(originalPos)
    
def on_release(key):
    if key == keyboard.Key.esc or key == keyboard.Key.delete:
        print(f"{key} pressed, exiting")
        return False # stop listener

if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise Exception("Key To Coordinates json file path argument not provided")

    f = open(sys.argv[1])
    data = json.load(f)
    f.close

    pyautogui.FAILSAFE = False

    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()