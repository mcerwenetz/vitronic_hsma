import socket
import threading
import os

def handle_client(client_socket):
    try:
        while True:
            # Receive the length of the incoming image
            image_length = client_socket.recv(4)
            if not image_length:
                break

            image_length = int.from_bytes(image_length, 'big')

            # Receive the image data
            image_data = b''
            while len(image_data) < image_length:
                packet = client_socket.recv(image_length - len(image_data))
                if not packet:
                    break
                image_data += packet

            # Save the image
            with open("received_image.jpg", "wb") as image_file:
                image_file.write(image_data)

            print("Image received and saved.")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
