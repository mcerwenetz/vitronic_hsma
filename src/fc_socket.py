import socket
import threading
import os
import inference
import sql_funcs
import psycopg2
import cv2
import numpy as np
from time import time
USED_IMAGE = 5

def setup_db():
    connection = psycopg2.connect(dbname="vitronicdb", user="vitronic",
                                  password="vitronicpasswd", host="141.19.96.152", port="5432")
    cursor = connection.cursor()
    return connection,cursor

def recv_image(client_socket,parcel_count):
    image_length = client_socket.recv(4)
    if not image_length:
        return

    image_length = int.from_bytes(image_length, 'big')

    # Receive the image data
    image_data = b''
    while len(image_data) < image_length:
        packet = client_socket.recv(image_length - len(image_data))
        if not packet:
            break
        image_data += packet

    # Save the image
    with open(f"{parcel_count}_{USED_IMAGE}.jpg", "wb") as image_file:
        image_file.write(image_data)


def cl_model_func(model,im):
    print("[INFO] Starting classification")
    result = (model.infer(image=im))

    return result[0].predicted_classes[0]

def handle_client(client_socket,parcel_count,model,connection, db_cursor):
    ts_fc_0 = time()
    try:
        while True:
            status = 1
            # Receive the length of the incoming image
            
            recv_image(client_socket,parcel_count)

            print("[INFO] Image received and saved.")

            cl_calc = cl_model_func(model,f"{parcel_count}_{USED_IMAGE}.jpg")
            
            if cl_calc == "bad":
                status = 2

####################

            recv_image(client_socket,parcel_count)

            array_length_data = client_socket.recv(4)
            if not array_length_data:
                break

            array_length = int.from_bytes(array_length_data, 'big')
            
            # If array_length is zero, it indicates the end of the session
            if array_length == 0:
                break

            # Receive the array data
            array_data = b''
            while len(array_data) < array_length:
                packet = client_socket.recv(array_length - len(array_data))
                if not packet:
                    break
                array_data += packet



            feature= np.frombuffer(array_data,dtype=np.uint8)
            feature = feature.reshape(500,32)

            ts_fc_1 = time()

            print("[INFO] Finished classification and feature detection")
            print("[INFO] Results: ")
            print()
            print(f"[INFO] Gate: 0")
            print(f"[INFO] Classification: {cl_calc}")
           # print(f"[INFO] Feature Vector: {}")
            print()
            print(f"[INFO] classification and feature detection took {ts_fc_1-ts_fc_0} s")
            sql_funcs.addEntry(connection,db_cursor,parcel_count/2,status,feature,feature.shape)
            print("[INFO] database query was send")


    except Exception as e:
        print(f"Exception: {e}")
    finally:
        client_socket.close()

def start_server():
    print("[INFO] starting model setup")
    model = inference.get_model("classification-ofjuw/3")
    print("[INFO] starting database setup")
    connection, db_cursor = setup_db()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen(5)
    print("Server listening on port 8080")
    pc = 0
    while True:
        pc += 1
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,pc,model,connection, db_cursor))
        client_handler.start()

if __name__ == "__main__":
    start_server()
