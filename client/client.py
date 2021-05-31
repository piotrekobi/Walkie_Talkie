import socket
import sys

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
# # s.connect(('144.126.244.194', 10000))

# Let's send data through UDP protocol
while True:

    # s.send(send_data.encode('utf-8'))

    # print("\n\n 1. Client Sent : ", send_data, "\n\n")
    send_data = input("Tekst: ")
    s.sendto(send_data.encode('utf-8'), ('144.126.244.194', 10000))
    data, address = s.recvfrom(24)
    print("\n\n 2. Client received : ", data.decode('utf-8'), "\n\n")
    # print(s.recv(1024))
# close the socket
s.close()
