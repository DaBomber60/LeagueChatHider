import pyautogui
import pydirectinput
import time
import ctypes
import math

# disable PyAutoGUI failsafe and set pause between actions
pyautogui.FAILSAFE = False
delay = 0.01
pyautogui.PAUSE = delay

def calc_chat_topright(window_h, chat_scale):
    """Calculate the top-right corner of the chat window based on the given parameters."""
    chat_scaler = 1 + (chat_scale / 100)
    chat_topr_x = math.floor((window_h * 0.239) * chat_scaler)
    chat_topr_y = math.ceil(window_h - (window_h * 0.128  * chat_scaler) + 1)
    return (chat_topr_x, chat_topr_y)

def run_macro(window_w, window_h, chat_scale):
    chat_topright = calc_chat_topright(window_h, chat_scale)
    """Perform the League of Legends chat mute macro."""
    # focus League of Legends window
    hwnd = ctypes.windll.user32.FindWindowW(None, "League of Legends (TM) Client")
    if hwnd:
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.1)
    initial = (window_w/2, window_h/2)
    pyautogui.moveTo(initial)
    time.sleep(1)
    pyautogui.click()
    time.sleep(delay)
    pydirectinput.press('enter')
    time.sleep(delay)
    pyautogui.moveTo(chat_topright)
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    pyautogui.mouseDown()
    pyautogui.moveTo(0, (window_h - 1))
    pyautogui.mouseUp()
    for _ in range(chat_scale % 10 + 2):
        pyautogui.moveTo(1, (window_h - 2))
        pyautogui.mouseDown()
        pyautogui.moveTo(10, (window_h - 2))
        pyautogui.moveTo(0, (window_h - 1))
        pyautogui.mouseUp()
    time.sleep(delay)
    pydirectinput.press('enter')
    time.sleep(delay)
    pyautogui.moveTo(initial)
    time.sleep(delay)
    pydirectinput.press('space')
    time.sleep(delay)
    pydirectinput.press('enter')
    time.sleep(delay)
    pyautogui.write('/mute all')
    time.sleep(delay)
    pydirectinput.press('enter')
    time.sleep(delay)