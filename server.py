#FILES STORED ON THE SERVER WILL GO TO A DIRECTORY CALLED "Server Files" IN THE SAME DIRECTORY AS THIS SCRIPT
import socket
import threading
import time
import base64
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4444
ADDR = (HOST, PORT)
FORMAT = "utf-8"
STRBUF = 2048
EXITCODE = "!EXIT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle(conn, addr):
    connected = True
    print(f"[WELCOME] Welcome, {addr[0]}")
    while connected:
        data = conn.recv(4).decode()
        if data:
            data = int(data)
            if data == 1:
                strlen = conn.recv(STRBUF).decode(FORMAT)
                strlen = int(strlen)
                time.sleep(.2)
                message = conn.recv(strlen).decode(FORMAT)
                if message == EXITCODE:
                    conn.close()
                    connected = False
                    print(f"[DISCONNECT] Goodbye, {addr[0]}")
                else:
                    print(f"[{addr[0]}] {message}")
            elif data == 2:
                filelen = conn.recv(STRBUF).decode(FORMAT)
                filelen = int(filelen)
                time.sleep(.2)
                file_data = conn.recv(filelen).decode(FORMAT)
                time.sleep(.2)
                filenamelen = conn.recv(STRBUF).decode(FORMAT)
                filenamelen = int(filenamelen)
                file_name = conn.recv(filenamelen).decode(FORMAT)
                decoded_data = base64.b64decode(file_data)
                with open(f"Server Files\\{file_name}", 'wb') as file:
                    file.write(decoded_data)
                print(f"File successfully written to {file_name}")
            elif data == 3:
                filenamelen = conn.recv(STRBUF).decode(FORMAT)
                filenamelen = int(filenamelen)
                time.sleep(.2)
                filename = conn.recv(filenamelen).decode(FORMAT)
                filepath = f"Server Files\\{filename}"
                with open(filepath, 'rb') as file:
                    data = file.read()
                    encoded_data = base64.b64encode(data)
                    encoded_string = encoded_data.decode(FORMAT)
                    conn.send(str(len(encoded_string)).encode(FORMAT))
                    time.sleep(.2)
                    conn.send(encoded_string.encode(FORMAT))           
            elif data == 4:
                direct = 'Server Files'
                files=""
                for filename in os.listdir(direct):
                    files+=f"{filename},"
                    conn.send(str(len(files)).encode(FORMAT))
                    time.sleep(.5)
                    conn.send(files.encode(FORMAT))

        

def start():
    server.listen()
    print("[START] Server listening for incoming traffic")
    while True:
        conn, addr = server.accept()
        client = threading.Thread(target=handle, args=(conn,addr))
        client.start()
        print(f"[WELCOME] A new client has connected. There are {threading.active_count()-1} users active.")

print(f"[START] Starting file server on {HOST}:{PORT}")
start()