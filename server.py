import socket
import json
import datetime

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

def isUserIntoJson(user):
    f = open('./data/users.json', )
    data = json.load(f)
    for i in data['users']:
        if i.get("user") == user:
            return True
    f.close()

def writeUserIntoJsonIfNotExists(user, user_password, filename='./data/users.json'):
    if isUserIntoJson(user):
        message = 'Ya existe el usuario: {}. Intentalo de nuevo'.format(user)
        print(message)
        return message
    else:
        writeUserIntoJson(filename, user, user_password)
        return "Usuario: {} registrado OK!".format(user)

def writeUserIntoJson(filename, user, user_password):
    new_data = {'user': user,
                'password': user_password
                }
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["users"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
    print('Usuario registrado con éxito')


def reg_operation(sequence, message_received_str):
    print('is REG message')
    user_name = message_received_str.split("$@%", 3)[2]
    user_password = message_received_str.split("$@%", 3)[3]
    message = writeUserIntoJsonIfNotExists(user_name, user_password)
    response = 'ANS$@%{}$@%{}'.format(
        sequence,
        message
    )
    bytesToSend = str.encode(response)

    UDPServerSocket.sendto(bytesToSend, address)

def put_operation(sequence, message_received_str):
    timestampN = datetime.datetime.now()


while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)
    message_received_str = str(message)
    operation = message_received_str.split("$@%", 2)[0]
    sequence = message_received_str.split("$@%", 2)[1]

    if "REG" in operation:
        reg_operation(sequence, message_received_str)
    elif "PUT" in operation:
        put_operation(sequence, message_received_str)