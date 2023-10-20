#! /bin/python3

# LIBS #########################################################################
from config import server_address, client_address, udp_socket
import os

def client_start():
	ret = udp_socket.recv(1024).decode()
	print(ret)	
	return

def main():
	udp_socket.bind(client_address)

	msg = input()
	udp_socket.sendto(msg.encode(), server_address)

	if msg == 'start':
		client_start()

	udp_socket.close()




if __name__ == "__main__":
	main()
	os.system("rm -rf __pycache__")
