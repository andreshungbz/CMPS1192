import socket
import argparse

def server_program(port):
    # Program Introduction
    print("-- Socket Messaging Server --")

    # Server Information
    server_hostname = socket.gethostname()  # server hostname
    ip_addresses = socket.gethostbyname_ex(server_hostname)[-1]  # list of server ip addresses
    server_ip = next((ip for ip in ip_addresses if ip.startswith('10.0')), None)  # choose ip starting with 10.0
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

    # Initial Connection
    print("\nWaiting...\n")
    client, address = server_socket.accept() # accept new connection
    # store the client's hostname, which is its first message to the server
    client_hostname = client.recv(max_bytes).decode()
    print(f"{client_hostname} connected with IP Address {str(address[0])} from Port {str(address[1])}\n")

    # Server Loop
    while True:
        data = client.recv(max_bytes).decode() # receive data stream

        # exit when client closes the connection
        if not data: # data being 0 bytes does this
            break

        # show client message in server terminal
        print(client_hostname + ": " + str(data))

        # write a message from the server and send to client
        data = server_hostname + ": "
        data += input(" -> ")
        client.send(data.encode()) # convert string data into bytes object

    # Closedown
    client.close() # close client connection
    server_socket.close() # close server socket

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Messaging Server')
    parser.add_argument('port', type=int, help='Port number to bind the server')
    args = parser.parse_args()
    server_program(args.port)