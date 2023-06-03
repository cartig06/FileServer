import socket
import time
import base64
#SORRY IN ADVANCE FOR THE MESSY CODE
HOST = "" #INSERT THE IP OF THE SERVER HOST HERE
PORT = 4444
ADDR = (HOST, PORT)
FORMAT = "utf-8"
STRBUF = 2048
EXITCODE = "!EXIT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_command(cmd):
    data = cmd.encode(FORMAT)
    client.send(data)

def send_str(msg):
    data = str(len(msg)).encode(FORMAT)
    client.send(data)
    data = msg.encode(FORMAT)
    time.sleep(.5)
    client.send(data)

def upload_file(file_path): #FILES NEED TO BE STORED IN A FOLDER IN THE SAME DIRECTORY AS SCRIPT CALLED "Client Files". THIS IS ALSO WHERE DOWNLOADED FILES WILL BE STORED
    with open(file_path, 'rb') as file:
        data = file.read()
        encoded_data = base64.b64encode(data)
        encoded_string = encoded_data.decode(FORMAT)
        client.send(str(len(encoded_string)).encode(FORMAT))
        time.sleep(.5)
        client.send(encoded_string.encode(FORMAT))
    file_name = input("filename on server: ")
    time.sleep(.5)
    client.send(str(len(file_name)).encode(FORMAT))
    time.sleep(.3)
    client.send(file_name.encode(FORMAT))

def download_file(server_path):
    filenamelen = str(len(server_path)).encode(FORMAT)
    client.send(filenamelen)
    client.send(server_path.encode(FORMAT))
    time.sleep(.2)
    filelen = client.recv(STRBUF).decode(FORMAT)
    filelen = int(filelen)
    time.sleep(.2)
    file_data = client.recv(filelen).decode(FORMAT)
    time.sleep(.2)
    decoded_data = base64.b64decode(file_data)
    with open(f"Client Files\\{server_path}", 'wb') as file:
        file.write(decoded_data)
    print(f"File successfully written to {server_path}")


running = True
print("FILE SERVER\n")
print("[1] Send a message to the server")
print("[2] Upload a file to the server")
print("[3] Download a file from the server")
print("[4] List files on the server")
while running:
    command = input("Command: ")
    if command == "1":
        send_command(command)
        msg = input("Message: ")
        send_str(msg)
        if msg == EXITCODE:
            running = False
    elif command == "2":
        send_command(command)
        filename = input('Filename: ')
        upload_file(f"Client Files\\{filename}")
        print(f"File saved on server as {filename}!")
    elif command == "3":
        send_command(command)
        server_file = input("File on Server: ")
        download_file(server_path=server_file)
    elif command == "4":
        send_command(command)
        time.sleep(.2)
        fileslen = client.recv(STRBUF).decode(FORMAT)
        fileslen = int(fileslen)
        time.sleep(.2)
        files = client.recv(fileslen).decode(FORMAT)
        count=0
        for i in files.split(','):
            if i:
                count+=1
                print(f"[{count}] {i}")
    else:
        running = False

try:
    send_command("1")
    send_str(EXITCODE)
    print("Exiting...")
except:
    print("Exiting...")
client.close()