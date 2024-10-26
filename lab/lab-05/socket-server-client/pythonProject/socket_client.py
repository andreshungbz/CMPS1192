import argparse
import socket
import threading

def receive_messages(client_socket, client_hostname, max_bytes):
    while True:
        try:
            message = client_socket.recv(max_bytes).decode()
            if not message:
                break
            print(message + f"\n{client_hostname}: ", end="")
        except:
            client_socket.close()
            break

def client_program(ip, port):
    # Program Introduction
    print("-- Socket Messaging Client --")

    # Client Information
    client_hostname = socket.gethostname()  # client hostname
    ip_addresses = socket.gethostbyname_ex(client_hostname)[-1]  # list of client ip addresses
    client_ip = next((ip for ip in ip_addresses if ip.startswith('192.168')), None)  # choose ip starting with 10.0
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

    # Start receive thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_hostname, max_bytes))
    receive_thread.start()

    # Client Loop
    message = input(f"{client_hostname}: ")
    while message.lower().strip() != 'exit':
        client_socket.send(message.encode())
        message = input(f"{client_hostname}: ")

    # Closedown
    client_socket.close() # close client socket

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Messaging Client')
    parser.add_argument('ip', type=str, help='Server IP address to connect to')
    parser.add_argument('port', type=int, help='Port number to connect to')
    args = parser.parse_args()
    client_program(args.ip, args.port)