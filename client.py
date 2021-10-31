import socket
from random import randrange

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def register():
    sequence_number = randrange(65536)
    user_name = input("Introduce tu nombre: \n >")
    user_password = input("Introduce tu contraseña: \n >")

    msgFromClient = "REG$@%{}$@%{}$@%{}".format(
        str(sequence_number),
        user_name,
        user_password
    )
    bytesToSend = str.encode(msgFromClient)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    validate_response(msgFromServer, sequence_number)


def validate_response(msgFromServer, sequence_number):
    decodedMessage = msgFromServer[0].decode()
    sequence_received = int(decodedMessage.split("$@%", 2)[1])
    operation_received = decodedMessage.split("$@%", 1)[0]
    if 'ANS' == operation_received and sequence_number == sequence_received:
        print("Mensaje recibido del servidor: {}".format(decodedMessage.split("$@%", 2)[2]))


def put_message():
    sequence_number = randrange(65536)
    user_src = input("Introduce tu nombre: \n >")
    user_password = input("Introduce tu contraseña: \n >")
    user_dst = input("Introduce el usuario destinatario: \n >")
    msg_dst = input("Introduce el mensaje: \n >")
    msgFromClient = "PUT$@%{}$@%{}$@%{}".format(
        str(sequence_number),
        msg_dst,
        user_src,
        user_dst,
        user_password
    )
    bytesToSend = str.encode(msgFromClient)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    deocedMessage = msgFromServer[0].decode()
    msg = "Message from Server: {}".format(deocedMessage)
    print(msg)

def main_menu():
    initial_msg = "Selecciona: \n" \
                  "1 => Registrate\n" \
                  "2 => Enviar mensaje\n" \
                  "3 => Leer mensajes\n" \
                  "4 => Salir\n" \
                  ">"
    exit = False
    while not exit:
        entrada = input(initial_msg)
        if entrada == "4":
            print("Adios")
            exit = True
        elif entrada == "1":
            register()
        elif entrada == "2":
            put_message()
        elif entrada == "3":
            #TODO: GET.
            print("GET")
        else:
            print("Valor incorrecto, vuelve a intentarlo, gracias.")

main_menu()