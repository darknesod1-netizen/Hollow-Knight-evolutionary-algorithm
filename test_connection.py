import socket
import json
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 11000))
print("Connected! Reading game state...")

buffer = ""
last_print = 0

while True:
    data = client.recv(1024).decode('utf-8')
    buffer += data
    while '\n' in buffer:
        line, buffer = buffer.split('\n', 1)
        state = json.loads(line)
        
        now = time.time()
        if now - last_print >= 5.0:
            print(f"x={state['x']:.2f} y={state['y']:.2f}", flush=True)
            last_print = now