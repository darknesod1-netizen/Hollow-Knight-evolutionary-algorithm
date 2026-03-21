import pyautogui
import time

def reset_to_start():
    """
    Warps the Knight back to the deployed start bench using Benchwarp hotkeys.
    """
    # Open pause menu
    pyautogui.press('escape')
    time.sleep(0.5)

    # Type WD to warp to deployed bench
    pyautogui.press('w')
    time.sleep(0.1)
    pyautogui.press('d')
    time.sleep(1.5)  # Wait for warp animation to complete