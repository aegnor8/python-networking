import socket
import sys

serverName = "<YOUR_SERVER_IP>"
serverPort = 12000

try:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as e:
    print ("Creation socket error:", e)
    sys.exit(1)

try:
    message = input("input lowercase message: ")
    clientSocket.sendto(message.encode(), (serverName, serverPort))

    clientSocket.settimeout(2)
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print("response:", modifiedMessage.decode())

except socket.timeout:
    print("Timeout error - no response from the server")

except socket.error as e:
    print("Network error:", e)

finally:
    clientSocket.close()