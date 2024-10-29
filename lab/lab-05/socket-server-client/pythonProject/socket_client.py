# socket_client.py

import argparse
import socket
import threading

# Receive Messages Function
def receive_messages(client_socket, client_hostname, max_bytes):
    while True:
        try:
            message = client_socket.recv(max_bytes).decode()
            if not message:
                break
            # just print the message without adding extra prompt
            print(f"\r{message}")  # \r to clear current line
            print(f"{client_hostname}: ", end="", flush=True)  # reprint prompt
        except:
            break
    client_socket.close()

# Client Program
def client_program(ip, port):
    # program introduction
    print("-- Socket Messaging Client --")

    # client information
    client_hostname = socket.gethostname() # client hostname
    ip_addresses = socket.gethostbyname_ex(client_hostname)[-1] # list of client ip addresses

    # edit to "192.168" or "10.0" accordingly
    client_ip = next((ip for ip in ip_addresses if ip.startswith('10.0')), None)
    if not client_ip:
        raise ValueError("No IP address starting with '10.0' found.")

    print("\n[Client Information]")
    print(f"Client Hostname: {client_hostname}")
    print(f"Client IP Addresses: {ip_addresses}")

    # client socket configuration
    server_ip = ip # set server ip that client will contact
    server_port = port # set server port to that client will connect to
    max_bytes = 2048 # set max bytes of packet
    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET: IPv4, SOCK_STREAM: TCP
    client_socket.connect((server_ip, server_port))

    print("\n[Client Configuration]")
    print(f"Client with IP Address {client_ip} set to contact Server with IP Address {server_ip} on Port {server_port}\n")

    # send client hostname to server as first message
    client_socket.send(client_hostname.encode())

    # start receive thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_hostname, max_bytes))
    receive_thread.daemon = True  # make thread daemon so it exits when main thread exits
    receive_thread.start()

    # client loop
    try:
        while True:
            message = input(f"{client_hostname}: ")

            # send disconnect message to server
            if message.lower().strip() == 'exit':
                client_socket.send(message.encode())
                break

            client_socket.send(message.encode())
    except:
        pass
    finally:
        # closedown
        client_socket.close()
        print("\nDisconnected from server.")

# Main Function
if __name__ == '__main__':
    # argument parsing
    parser = argparse.ArgumentParser(description='Socket Messaging Client')
    parser.add_argument('ip', type=str, help='Server IP address to connect to')
    parser.add_argument('port', type=int, help='Port number to connect to')
    args = parser.parse_args()

    # run client program
    client_program(args.ip, args.port)