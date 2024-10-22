import socket

def server_program():
    # Program Introduction

    print("-- Simple Socket Server Messaging Program --")
    print("Ensure the socket client program is configured with the chosen server IP address\n")

    # Server Information

    print("-- Server Information --")

    server_hostname = socket.gethostname() # computer hostname
    print(f"Server Hostname: {server_hostname}")

    ip_addresses = socket.gethostbyname_ex(socket.gethostname())[-1] # list of computer ip addresses
    print(f"Available Server IP Addresses: {ip_addresses}")

    server_ip = next((ip for ip in ip_addresses if ip.startswith('10.0')), None) # choose ip starting with 10.0
    if not server_ip:
        raise ValueError("No IP address starting with '10.' found.") # error checking
    print(f"Chosen Server IP Address: {server_ip}")

    # Server Socket Configuration

    port = 6000 # set port
    max_bytes = 2048 # set max bytes of packet
    server_socket = socket.socket() # create socket
    server_socket.bind((server_ip, port)) # bind to socket the ip and port
    server_socket.listen(4) # set max number of simultaneous clients

    print("\nWaiting...\n")

    # Initial Connection

    connection, address = server_socket.accept() # accept new connection

    # store the client's hostname, which is its first message to the server
    client_hostname = connection.recv(max_bytes).decode()
    print(f"Connection from {str(address[0])} (hostname: {client_hostname})\n")

    # Connection Loop

    while True:
        data = connection.recv(max_bytes).decode() # receive data stream

        # exit when client closes the connection
        if not data:
            break

        # show client message on server terminal
        print(client_hostname + ": " + str(data))

        # write a message from the server and send to client
        data = server_hostname + ": "
        data += input(" -> ")
        connection.send(data.encode())

    connection.close() # close connection

if __name__ == '__main__':
    server_program()