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


# Logic of practise UD3

def is_user_into_json(user, filename='./data/users.json'):
    file = open(filename, 'r+')
    data = json.load(file)
    is_user = len(list(filter(lambda e: e.get("user") == user, data['users']))) != 0
    file.close()
    return is_user


def write_user_into_json_if_not_exists(user, user_password, filename='./data/users.json'):
    if is_user_into_json(user):
        message = 'Ya existe el usuario: {}. Intentalo de nuevo'.format(user)
        return message
    else:
        new_data = {'user': user, 'password': user_password, 'messages': []}
        write_user_into_json(new_data, filename)
        return "Usuario: {} registrado OK!".format(user)


def write_user_into_json(new_data, filename='./data/users.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["users"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
    print('Usuario registrado con éxito')


def send_put_response(sequence, user_src, timestamp, text):
    response = 'ANS$@%{}$@%{}@%{}@%{}@%{}'.format(
        sequence,
        'Se ha almacenado su mensaje con éxito!',
        user_src,
        timestamp,
        text
    )
    bytes_to_send = str.encode(response)
    UDPServerSocket.sendto(bytes_to_send, address)


def write_message_into_user(new_data, usr_dst, filename='./data/users.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        for elem_data in file_data['users']:
            if elem_data.get('user') == usr_dst:
                elem_data['messages'].append(new_data)
                print(elem_data)
                break
        file.seek(0)
        json.dump(file_data, file, indent=4)



def reg_operation(sequence, message_received_str):
    user_name = message_received_str.split("$@%", 3)[2]
    user_password = message_received_str.split("$@%", 3)[3]
    message = write_user_into_json_if_not_exists(user_name, user_password)
    send_generic_response(message, sequence)


def send_generic_response(message, sequence):
    response = generic_response(message, sequence)
    bytes_to_send = str.encode(response)
    UDPServerSocket.sendto(bytes_to_send, address)


def generic_response(message, sequence):
    response = 'ANS$@%{}$@%{}'.format(
        sequence,
        message
    )
    return response


def is_valid_user(user_src, password_src):
    file = open('./data/users.json', )
    data = json.load(file)
    filtered_list = list(
        filter(lambda e: e.get("user") == user_src and e.get("password") == password_src, data['users']))
    is_valid = len(filtered_list) != 0

    file.close()
    return is_valid


def put_operation(sequence, message_received_str):
    timestamp = str(datetime.datetime.now())
    text = message_received_str.split("$@%", 5)[2]
    user_src = message_received_str.split("$@%", 5)[3]
    usr_dst = message_received_str.split("$@%", 5)[4]
    password_src = message_received_str.split("$@%", 5)[5]

    validate_users_and_put_message(sequence, timestamp, text, user_src, usr_dst, password_src)


def check_usr_dst_and_put_message(sequence, timestamp, text, user_src, usr_dst):
    if is_user_into_json(usr_dst):
        new_data = {'usr_src': user_src, 'timestamp': timestamp, 'text': text}
        write_message_into_user(new_data, usr_dst)
        send_put_response(sequence, user_src, timestamp, text)
    else:
        send_generic_response('Usuario de destino: {} no existe. Intentalo de nuevo'.format(usr_dst), sequence)


def validate_users_and_put_message(sequence, timestamp, text, user_src, usr_dst, password_src):
    if is_valid_user(user_src, password_src):
        check_usr_dst_and_put_message(sequence, timestamp, text, user_src, usr_dst)
    else:
        send_generic_response('Usuario y/o contraseña incorrecto/s', sequence)


def main():
    global address
    while (True):
        #try:
            bytes_address_pair = UDPServerSocket.recvfrom(bufferSize)
            message = bytes_address_pair[0].decode()
            address = bytes_address_pair[1]
            client_msg = "Message from Client:{}".format(message)
            client_ip = "Client IP Address:{}".format(address)
            print(client_msg)
            print(client_ip)
            operation = message.split("$@%", 2)[0]
            sequence = message.split("$@%", 2)[1]

            if "REG" in operation:
                reg_operation(sequence, message)
            elif "PUT" in operation:
                put_operation(sequence, message)
        #except:
        #    send_generic_response('Error no controlado', 1)

main()
