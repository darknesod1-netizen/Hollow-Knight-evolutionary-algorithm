import socket
import json

class GameBridge:
    """Handles TCP communication with the Hollow Knight mod."""

    def __init__(self, host='localhost', port=11000):
        self.host = host
        self.port = port
        self.client = None
        self.buffer = ""

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        print(f"Connected to game on {self.host}:{self.port}")

    def get_state(self):
        """Read one state frame from the game."""
        while '\n' not in self.buffer:
            data = self.client.recv(1024).decode('utf-8')
            if not data:
                return None
            self.buffer += data

        line, self.buffer = self.buffer.split('\n', 1)
        state = json.loads(line)
        return state

    def close(self):
        if self.client:
            self.client.close()
            self.client = None