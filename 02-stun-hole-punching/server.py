import socket
import sys

serverPort = 12000

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(("", serverPort))
    print("Server ready to receive clients registration")

except socket.error as e:
    print("Connection error: ", e)
    sys.exit(1)

clients_address = []

while True:
    try:
        data, address = serverSocket.recvfrom(2048)
        message = data.decode()

        if message == "REGISTRATION" and address not in clients_address:
                clients_address.append(address)
                print(f"Client registered: {address}")
         
        if len(clients_address) == 2:
            # Send each client the address of the other
            peer_info_0 = f"{clients_address[0][0]}:{clients_address[0][1]}" # formatting address client 0
            peer_info_1 = f"{clients_address[1][0]}:{clients_address[1][1]}" # formatting address client 1
            serverSocket.sendto(peer_info_0.encode(), clients_address[1]) # send client 0's address to client 1
            serverSocket.sendto(peer_info_1.encode(), clients_address[0]) # send client 1's address to client 0
            print("Peers informed, ready for new clients")
    
    except socket.error as e:
        print("Network error: ", e)
        continue

    except KeyboardInterrupt:
        print("Server interrupted by the user")
        serverSocket.close()
        sys.exit(0)

