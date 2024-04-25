from pynput.keyboard import Key, Controller
import pyautogui

def on_press(key, data, controller: Controller):
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

    for dataKey in data:
        if key.char != dataKey:
            continue

        info = data[dataKey]
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
            print(f"doesnt contain value key: {info}")
            continue

        controller.press(Key.backspace)
        controller.release(Key.backspace)
        controller.type(info["value"])
        clickPos = data[info["type"]]
        pyautogui.moveTo(clickPos["x"], clickPos["y"])
        pyautogui.click()
        pyautogui.moveTo(originalPos)
    
def on_release(key):
    if key == Key.esc or key == Key.delete:
        print(f"{key} pressed, exiting")
        return False # stop listener