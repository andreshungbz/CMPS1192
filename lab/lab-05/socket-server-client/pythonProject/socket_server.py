# socket_server.py
import argparse
import socket
import threading

clients = []

def handle_client(client_socket, client_address, max_bytes):
    # Initial Connection
    client_hostname = client_socket.recv(max_bytes).decode()
    print(f"{client_hostname} connected with IP Address {str(client_address[0])} from Port {str(client_address[1])}\n")

    # Append to clients list
    clients.append(client_socket)

    # Send join message to all clients
    join_message = f"[{client_hostname} has joined the chat]"
    print(join_message)
    broadcast(join_message, client_socket, client_hostname)

    # Thread Loop
    while True:
        try:
            data = client_socket.recv(2048).decode()

            if not data or data.lower().strip() == 'exit':
                exit_message = f"[{client_hostname} has disconnected]"
                print(exit_message)
                broadcast(exit_message, client_socket, client_hostname)
                break

            print(f"{client_hostname}: {data}")
            broadcast(data, client_socket, client_hostname)
        except:
            break

    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()

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

def server_program(port):
    # Program Introduction
    print("-- Socket Messaging Server --")

    # Server Information
    server_hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(server_hostname)[-1]
    server_ip = next((ip for ip in ip_addresses if ip.startswith('192.168')), None)
    if not server_ip:
        raise ValueError("No IP address starting with '10.' found.")

    print("\n[Server Information]")
    print(f"Server Hostname: {server_hostname}")
    print(f"Server IP Addresses: {ip_addresses}")

    # Server Socket Configuration
    server_port = port
    max_bytes = 2048

    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(4)

    print("\n[Server Configuration]")
    print(f"Server listening on socket bound to IP Address {server_ip} and Port {server_port}")
    print("\nWaiting...\n")

    # Server Loop
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, max_bytes))
            client_thread.daemon = True  # Make thread daemon so it exits when main thread exits
            client_thread.start()
        except:
            break

    # Closedown
    server_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Messaging Server')
    parser.add_argument('port', type=int, help='Port number to bind the server')
    args = parser.parse_args()
    server_program(args.port)