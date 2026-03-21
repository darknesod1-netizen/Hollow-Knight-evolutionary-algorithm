import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 11000))
print("Connected! Reading game state...")

buffer = ""
while True:
    data = client.recv(1024).decode('utf-8')
    buffer += data
    while '\n' in buffer:
        line, buffer = buffer.split('\n', 1)
        print(line)