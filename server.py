import socket
import threading
import struct
import io
import time

import pyautogui

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

    while True:
        sent_t = time.perf_counter()

        data = client_socket.recv(1024)

        screenshot = pyautogui.screenshot()

        # Convert the image to JPEG format
        screenshot = screenshot.convert('RGB')

        # Resize the image to a smaller size (optional)
        screenshot = screenshot.resize((1920, 1080))

        img_byte_arr = io.BytesIO()

        screenshot.save(img_byte_arr, format='JPEG', quality=30)
        img_byte_arr = img_byte_arr.getvalue()

        size = len(img_byte_arr)
        client_socket.send(size.to_bytes(4, byteorder='big'))

        try:
            client_socket.send(img_byte_arr)
        except BrokenPipeError:
            break

        print(time.perf_counter() - sent_t)

    client_socket.close()


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
