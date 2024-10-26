# socket_server.py

import argparse
import socket
import threading

clients = []

# Client Handler Function
def handle_client(client_socket, client_address, max_bytes):
    # initial connection
    client_hostname = client_socket.recv(max_bytes).decode()
    print(f"{client_hostname} connected with IP Address {str(client_address[0])} from Port {str(client_address[1])}")

    # append to clients list
    clients.append(client_socket)

    # send join message to all clients
    join_message = f"[{client_hostname} has joined the chat]\n"
    print(join_message)
    broadcast(join_message, client_socket, client_hostname)

    # thread loop
    while True:
        try:
            data = client_socket.recv(2048).decode()

            # handle disconnection
            if not data or data.lower().strip() == 'exit':
                exit_message = f"[{client_hostname} has disconnected]"
                print(exit_message)
                broadcast(exit_message, client_socket, client_hostname)
                break

            print(f"{client_hostname}: {data}")
            broadcast(data, client_socket, client_hostname)
        except:
            break

    # closedown
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()

# Broadcast Function
def broadcast(message, client_socket, client_hostname):
    formatted_message = f"\n{client_hostname}: {message}"
    for client in clients:
        if client != client_socket:
            try:
                client.send(formatted_message.encode())
            except:
                if client in clients:
                    clients.remove(client)
                client.close()

# Server Program
def server_program(port):
    # program introduction
    print("-- Socket Messaging Server --")

    # server information
    server_hostname = socket.gethostname() # server hostname
    ip_addresses = socket.gethostbyname_ex(server_hostname)[-1] # list of server ip addresses

    # edit to "192.168" or "10.0" accordingly
    server_ip = next((ip for ip in ip_addresses if ip.startswith('192.168')), None)
    if not server_ip:
        raise ValueError("No IP address starting with '192.168' found.")

    print("\n[Server Information]")
    print(f"Server Hostname: {server_hostname}")
    print(f"Server IP Addresses: {ip_addresses}")

    # server socket configuration
    server_port = port # set port to use for server
    max_bytes = 2048 # set max bytes of packet
    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET: IPv4, SOCK_STREAM: TCP
    server_socket.bind((server_ip, server_port))
    server_socket.listen(4) # have a maximum of 4 clients

    print("\n[Server Configuration]")
    print(f"Server listening on socket bound to IP Address {server_ip} and Port {server_port}")

    print("\nWaiting...\n")

    # server loop
    while True:
        try:
            # accept connection
            client_socket, client_address = server_socket.accept()

            # start client thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, max_bytes))
            client_thread.daemon = True  # make thread daemon so it exits when main thread exits
            client_thread.start()
        except:
            break

    # closedown
    server_socket.close()

# Main Function
if __name__ == '__main__':
    # argument parsing
    parser = argparse.ArgumentParser(description='Socket Messaging Server')
    parser.add_argument('port', type=int, help='Port number to bind the server')
    args = parser.parse_args()

    # run server
    server_program(args.port)