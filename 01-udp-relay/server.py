import socket
import sys

serverPort = 12000

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(("", serverPort))
    print("Server ready to receive")
except socket.error as e:
    print("Connection error: ", e)
    sys.exit(1)


while True:
    try:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.decode().upper()
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    except socket.error as e:
        print("Network error: ", e)
        continue

    except KeyboardInterrupt:
        print("Server interrupted by the user")
        serverSocket.close()
        sys.exit(0)

