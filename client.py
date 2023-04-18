import socket
import sounddevice as sd
import numpy as np
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("localhost", int(input('Port = ')))
sock.connect(server_address)

def callback(indata: np.ndarray, frames, time, status):
    data = pickle.dumps(indata)
    size = len(data).to_bytes(4, byteorder='big')
    sock.send(size)
    sock.send(data)
    pass

rate = 8000
blocksize = int(rate/10)
stream = sd.InputStream(callback=callback, blocksize=blocksize, samplerate=rate, dtype='int16', channels=1)

stream.start()

while True:
    pass

# sock.close()
