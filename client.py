import socket
import io

from PIL import Image

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("localhost", int(input('Port = ')))
sock.connect(server_address)

while True:
    # Read the size of the image data
    sock.send(b"Fetching")
    size_bytes = sock.recv(4)
    size = int.from_bytes(size_bytes, byteorder='big')

    # Read the image data
    img_byte_arr = b''
    while len(img_byte_arr) < size:
        img_byte_arr += sock.recv(1024)

    sock.send(b"Ready")
    image = Image.open(io.BytesIO(img_byte_arr))
    image.save('test.jpeg')


# print(data)
sock.close()
