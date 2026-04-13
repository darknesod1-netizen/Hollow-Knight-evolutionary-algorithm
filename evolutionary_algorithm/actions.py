import pyautogui
import time

# Default Hollow Knight key bindings
KEY_MAP = {
    0: 'left',
    1: 'right',
    2: 'z',      # jump
    3: 'x',      # attack
}

# How long each keypress lasts in seconds
PRESS_DURATION = 0.05

def perform_action(output_activations):
    """
    Takes NEAT network outputs (list of 5 floats)
    and presses the corresponding keys if activation > 0.5.
    Multiple keys can be pressed at once.
    """
    keys_to_press = []
    for i, activation in enumerate(output_activations):
        if activation > 0.5:
            keys_to_press.append(KEY_MAP[i])

    for key in keys_to_press:
        pyautogui.keyDown(key)

    time.sleep(PRESS_DURATION)

    for key in keys_to_press:
        pyautogui.keyUp(key)