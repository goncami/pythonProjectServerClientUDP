import datetime
import socket
from random import randrange

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


def common_initial_prompt():
    sequence_number = str(randrange(65536))
    user_src = input("Introduce tu nombre: \n >")
    user_password = input("Introduce tu contraseña: \n >")
    return sequence_number, user_password, user_src


def send_data(msg_from_client):
    bytes_to_send = str.encode(msg_from_client)
    UDPClientSocket.sendto(bytes_to_send, serverAddressPort)


def capture_response(sequence):
    msg_from_server = UDPClientSocket.recvfrom(bufferSize)
    validate_response(msg_from_server, sequence)


def create_send_data_and_capture_response(msg_from_client, sequence: str):
    send_data(msg_from_client)
    capture_response(sequence)


def register():
    sequence_str, user_password, user_name = common_initial_prompt()

    msg_from_client = "REG$@%{}$@%{}$@%{}".format(
        sequence_str,
        user_name,
        user_password
    )
    create_send_data_and_capture_response(msg_from_client, sequence_str)


def put_message():
    sequence_str, user_password, user_src = common_initial_prompt()
    user_dst = input("Introduce el usuario destinatario: \n >")
    text = input("Introduce el mensaje: \n >")
    msg_from_client = "PUT$@%{}$@%{}$@%{}$@%{}$@%{}".format(
        sequence_str,
        text,
        user_src,
        user_dst,
        user_password
    )
    create_send_data_and_capture_response(msg_from_client, sequence_str)


def get_messages():
    sequence_str, user_password, user_src = common_initial_prompt()
    msg_from_client = "GET$@%{}$@%{}$@%{}".format(
        sequence_str,
        user_src,
        user_password
    )
    create_send_data_and_capture_response(msg_from_client, sequence_str)


def validate_response(msg_from_server, sequence:str):
    decoded_message = msg_from_server[0].decode()
    sequence_received = decoded_message.split("$@%", 2)[1]
    operation_received = decoded_message.split("$@%", 1)[0]
    print(datetime.datetime.now(), '{}'.format(decoded_message.split('$@%')))
    if 'ANS' == operation_received and sequence == sequence_received:
        if len(decoded_message.split('$@%')) >= 6:
            print('{}'.format(decoded_message.split('$@%')[2]))
            list_messages = decoded_message.split('$@%')
            count = 0
            while count < 3:
                del list_messages[0]
                count += 1
            for sub_list_count in range(0, len(list_messages), 3):
                print('- Mensaje: "{}"'
                      ' - de: {}'
                      ' - fecha: {}'.format(
                    list_messages[sub_list_count:sub_list_count + 3][2],
                    list_messages[sub_list_count:sub_list_count + 3][0],
                    list_messages[sub_list_count:sub_list_count + 3][1]
                ))
        else:
            print('Mensaje recibido del servidor: {}'.format(decoded_message.split('$@%')[2]))


def main():
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
            UDPClientSocket.close()
            exit = True
        elif entrada == "1":
            register()
        elif entrada == "2":
            put_message()
        elif entrada == "3":
            get_messages()
        else:
            print("Valor incorrecto, vuelve a intentarlo, gracias.")


main()
