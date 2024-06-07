import socket
import os

def send_image(image_path, server_ip, server_port):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    image_length = len(image_data)
    image_length_bytes = image_length.to_bytes(4, 'big')

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_socket.sendall(image_length_bytes + image_data)
    client_socket.close()

