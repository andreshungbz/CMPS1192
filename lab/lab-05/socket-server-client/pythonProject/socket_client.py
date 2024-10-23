import socket
import argparse

def client_program(ip, port):
    # Program Introduction
    print("-- Socket Messaging Client --")

    # Client Information
    client_hostname = socket.gethostname()  # client hostname
    ip_addresses = socket.gethostbyname_ex(client_hostname)[-1]  # list of client ip addresses
    client_ip = next((ip for ip in ip_addresses if ip.startswith('10.0')), None)  # choose ip starting with 10.0
    if not client_ip:
        raise ValueError("No IP address starting with '10.' found.")  # error checking

    print("\n[Client Information]")
    print(f"Client Hostname: {client_hostname}")
    print(f"Client IP Addresses: {ip_addresses}")

    # Client Socket Configuration
    server_ip = ip # set server ip that client will contact
    server_port = port # set server port to that client will connect to
    max_bytes = 2048  # set max bytes of packet

    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for IPv4, SOCK_STREAM for TCP
    client_socket.connect((server_ip, server_port)) # connect to server

    print("\n[Client Configuration]")
    print(f"Client with IP Address {client_ip} set to contact Server with IP Address {server_ip} on Port {server_port}\n")

    # Initial Connection
    # send client host name to server as first message
    client_socket.send(client_hostname.encode())  # send hostname to server

    # Client Loop
    message = input(" -> ") # accept input
    while message.lower().strip() != 'exit': # exit loop when the input is 'exit'
        client_socket.send(message.encode()) # send message to server

        data = client_socket.recv(max_bytes).decode() # receive server response
        print(data) # show server message in client terminal

        message = input(" -> ") # accept another input

    # Closedown
    client_socket.close() # close client socket

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Messaging Client')
    parser.add_argument('ip', type=str, help='Server IP address to connect to')
    parser.add_argument('port', type=int, help='Port number to connect to')
    args = parser.parse_args()
    client_program(args.ip, args.port)