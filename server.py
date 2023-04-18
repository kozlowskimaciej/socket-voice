import socket
import threading
import struct
import time
import sounddevice as sd
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an available port
sock.bind(('', 0))

# Get the port number that was assigned to the socket
port = sock.getsockname()[1]
print(f'Socket bound to port {port}')

sock.listen()

client_threads = []

def handle_client(client_socket):
    client_socket.setsockopt(
        socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0)
    )

    with sd.OutputStream(samplerate=8000, blocksize=800, dtype='int16', channels=1) as stream:
        while True:
            sent_t = time.perf_counter()

            size_bytes = client_socket.recv(4)
            size = int.from_bytes(size_bytes, byteorder='big')

            data = client_socket.recv(int(size))

            data = pickle.loads(data)
            print(len(data))

            stream.write(data)

            print(time.perf_counter() - sent_t)


    # client_socket.close()

while True:
    # Wait for a connection
    client_socket, client_address = sock.accept()
    # Create a new thread to handle the connection
    client_thread = threading.Thread(
        target=handle_client, args=(client_socket,))
    client_threads.append(client_thread)
    client_thread.start()

    for t in client_threads:
        t.join(timeout=5)
