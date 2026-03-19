import socket
import threading
import time
import sys

SERVER_IP = "<YOUR_SERVER_IP>"
SERVER_PORT = 12000

connected = threading.Event()

try:
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as e:
    print("Socket error:", e)
    sys.exit(1)

# Client registration to the server
clientSock.sendto(b"REGISTRATION", (SERVER_IP, SERVER_PORT))
print("Registered to server, waiting for peer...")

data , _ = clientSock.recvfrom(2048)

print("data: ", data)
peer_ip, port = data.decode().split(":")
peer_port = int(port)
peer_address = (peer_ip, peer_port)
print("Peer address: ", peer_address)

# Receiver Thread
def receive_loop():

    while True:
        try:
            data, addr = clientSock.recvfrom(2048)
            message = data.decode()

            if not connected.is_set():
                connected.set()
                print("\nConnection established with", addr)

            if message == "PUNCH":
                clientSock.sendto(b"PUNCH_ACK", addr)
                continue

            if message == "PUNCH_ACK":
                continue

            print("\npeer:", message)

        except (socket.error) as e:
            print("Socket error:", e)
            continue

        except (UnicodeDecodeError) as e:
            print("Decode error:", e)
            continue

# Hole Punching thread
def punching_loop():
    print("Starting hole punching...")

    for i in range(120):

        if connected.is_set():
            break

        try:
            clientSock.sendto(b"PUNCH", peer_address)
            print("Punch attempt", i + 1)
            time.sleep(0.1)

        except socket.error as e:
            print("error:", e)

# Start thread
recv_thread = threading.Thread(target=receive_loop, daemon=True)
recv_thread.start()

punch_thread = threading.Thread(target=punching_loop, daemon=True)
punch_thread.start()

# Waiting connection
connected.wait()
print("Ready to chat!")

# Chat loop
try:
    while True:
        message = input("you: ")

        # Checking message is not empty
        if not message:
            continue # Come back to message input

        clientSock.sendto(message.encode(), peer_address)

except KeyboardInterrupt:
    print("\nClosing chat")
    clientSock.close()
    sys.exit(0)