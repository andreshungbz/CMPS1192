import argparse
import socket
import threading

clients = []

# Function to Handle Client
def handle_client(client_socket, client_address, max_bytes):
    # Initial Connection
    client_hostname = client_socket.recv(max_bytes).decode()
    print(f"{client_hostname} connected with IP Address {str(client_address[0])} from Port {str(client_address[1])}\n")

    # Append to clients list
    clients.append(client_socket)

    # Thread Loop
    while True:
        try:
            data = client_socket.recv(2048).decode()

            if not data:
                break

            if data.lower().strip() == 'exit':
                exit_message = f"[{client_hostname} has disconnected]"
                print(exit_message)
                broadcast(exit_message, client_socket, client_hostname)
                break

            print(f"{client_hostname}: {data}")
            broadcast(data, client_socket, client_hostname)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

# Function to Broadcast Message to All Clients
def broadcast(message, client_socket, client_hostname):
    formatted_message = f"\n{client_hostname}: {message}"
    for client in clients:
        if client != client_socket: # don't send message to self
            try:
                client.send(formatted_message.encode())
            except:
                clients.remove(client)
                client.close()

# Server Program
def server_program(port):
    # Program Introduction
    print("-- Socket Messaging Server --")

    # Server Information
    server_hostname = socket.gethostname()  # server hostname
    ip_addresses = socket.gethostbyname_ex(server_hostname)[-1]  # list of server ip addresses
    server_ip = next((ip for ip in ip_addresses if ip.startswith('192.168')), None)  # choose ip starting with 10.0
    if not server_ip:
        raise ValueError("No IP address starting with '10.' found.")  # error checking

    print("\n[Server Information]")
    print(f"Server Hostname: {server_hostname}")
    print(f"Server IP Addresses: {ip_addresses}")

    # Server Socket Configuration
    server_port = port # set server port that will listen
    max_bytes = 2048 # set max bytes of packet

    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for IPv4, SOCK_STREAM for TCP
    server_socket.bind((server_ip, server_port)) # bind to socket the ip and port
    server_socket.listen(4) # set max number of simultaneous clients

    print("\n[Server Configuration]")
    print(f"Server listening on socket bound to IP Address {server_ip} and Port {server_port}")

    print("\nWaiting...\n")

    # Server Loop
    while True:
        client_socket, client_address = server_socket.accept() # accept client connection

        # start client thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, max_bytes))
        client_thread.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Messaging Server')
    parser.add_argument('port', type=int, help='Port number to bind the server')
    args = parser.parse_args()
    server_program(args.port)