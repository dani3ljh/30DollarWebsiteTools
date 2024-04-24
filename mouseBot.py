from pynput.keyboard import Key, Controller
import pyautogui

def on_press(key, data, controller: Controller):
    if not hasattr(key, "char"):
        return
    for dataKey in data:
        if key.char == dataKey:
            info = data[dataKey]
            print(f"command {key.char} detected clicking at ({info['x']}, {info['y']})")
            originalPos = pyautogui.position()
            pyautogui.moveTo(info["x"], info["y"])
            pyautogui.click()
            if info["clickCenter"]:
                pyautogui.click(450, 620)
                controller.press(Key.ctrl)
                controller.press('a')
                controller.release('a')
                controller.release(Key.ctrl)
            else:
                pyautogui.moveTo(originalPos)
    
def on_release(key):
    if key == Key.esc or key == Key.delete:
        print(f"{key} pressed, exiting")
        return False # stop listener