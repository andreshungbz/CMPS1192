import socket

def client_program():
    # Program Introduction

    print("-- Simple Socket Client Messaging Program --")
    print("Ensure the server IP address is configured correctly\n")

    # Client Information

    print("-- Client Information --")

    client_hostname = socket.gethostname() # computer hostname
    print(f"Client Hostname: {client_hostname}")

    ip_addresses = socket.gethostbyname_ex(socket.gethostname())[-1] # list of computer ip addresses
    print(f"Available Client IP Addresses: {ip_addresses}")

    client_ip = next((ip for ip in ip_addresses if ip.startswith('10.0')), None) # choose ip starting with 10.0
    if not client_ip:
        raise ValueError("No IP address starting with '10.' found.") # error checking
    print(f"Chosen Server IP Address: {client_ip}\n")

    # Configure Server to Contact

    server_ip = '10.0.57.166' # set server ip to contact
    port = 6000 # set port
    max_bytes = 2048  # set max bytes of packet

    # Client Socket Configuration

    client_socket = socket.socket() # create socket
    client_socket.connect((server_ip, port)) # connect to server

    # Initial Connection

    # send client host name to server as first message
    client_socket.send(client_hostname.encode())  # send hostname to server

    # Connection Loop

    message = input(" -> ") # accept input
    while message.lower().strip() != 'exit': # exit loop when the input is 'exit'
        client_socket.send(message.encode()) # send message to server
        data = client_socket.recv(max_bytes).decode() # receive server response

        print(data) # show in client terminal

        message = input(" -> ") # accept another input

    client_socket.close() # close connection

if __name__ == '__main__':
    client_program()