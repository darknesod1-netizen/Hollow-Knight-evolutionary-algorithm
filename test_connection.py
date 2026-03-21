import socket
import json
import pyautogui
import time

# Map actions to keyboard keys (default HK bindings)
KEY_MAP = {
    "left": "left",
    "right": "right",
    "jump": "z",
    "dash": "x",
    "attack": "c",
    "none": None
}

def send_action(action):
    key = KEY_MAP.get(action)
    if key:
        pyautogui.keyDown(key)
        time.sleep(0.05)
        pyautogui.keyUp(key)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 11000))
print("Connected! Reading game state...")

buffer = ""
actions = ["right", "right", "jump", "right", "none"]
action_idx = 0

while True:
    data = client.recv(1024).decode('utf-8')
    buffer += data
    while '\n' in buffer:
        line, buffer = buffer.split('\n', 1)
        state = json.loads(line)
        print(f"x={state['x']:.1f} y={state['y']:.1f} onGround={state['onGround']}", flush=True)
        
        # Send a test action every frame
        action = actions[action_idx % len(actions)]
        send_action(action)
        action_idx += 1