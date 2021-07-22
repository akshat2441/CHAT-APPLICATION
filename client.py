import socket
import select
import errno
import sys

my_username=input("Username: ")
HEADER_LENGTH=10

client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "127.0.0.1"
port=1234
client_socket.connect((IP, port))
client_socket.setblocking(False)

username=my_username.encode('utf-8')
username_header=f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header+username)


while True:
    message=input(f"{my_username} > ")

    if message:

        message=message.encode('utf-8')
        message_header=f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header+message)
    
    try:
        while True:
            username_header=client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed be the Server.")
                sys.exit()
            username_length=int(username_header.decode('utf-8').strip())
            username=client_socket.recv(username_length).decode('utf-8')

            message_header=client_socket.recv(HEADER_LENGTH)
            message_length=int(message_header.decode('utf-8').strip())
            message=client_socket.recv(message_length).decode('utf-8')

            
            print(f"{username} > {message}")

    except IOError as e:
        if e.errno!=errno.EAGAIN and e.errno!=errno.EWOULDBLOCK:
            print('Reading Error'.str(e))
        continue

    except Exception as e:
        print('General Exception',str(e))
        sys.exit()
