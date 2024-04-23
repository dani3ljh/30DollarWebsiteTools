from pynput import keyboard
import pyautogui

def on_press(key, data):
    if not hasattr(key, "char"):
        return
    for dataKey in data:
        if key.char == dataKey:
            coords = data[dataKey]
            print(f"command {key.char} detected clicking at ({coords['x']}, {coords['y']})")
            originalPos = pyautogui.position()
            pyautogui.moveTo(coords["x"], coords["y"])
            pyautogui.click()
            pyautogui.moveTo(originalPos)
    
def on_release(key):
    if key == keyboard.Key.esc or key == keyboard.Key.delete:
        print(f"{key} pressed, exiting")
        return False # stop listener