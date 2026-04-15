import pyautogui
import time

def reset_to_start():
    
    # Warps the Knight back to the deployed start Benchwarp hotkeys.
    
    # Open pause menu
    pyautogui.press('escape')
    time.sleep(0.5)

    # Type WD to warp to deployed bench
    pyautogui.press('w')
    pyautogui.press('d')
    time.sleep(4)  

    # Press Esc two time to initiate the increased tick rate
    pyautogui.press('escape')
    time.sleep(0.5)
    pyautogui.press('escape')
