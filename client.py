#! /bin/python3

# LIBS #########################################################################
from config import server_ip, server_port, client_ip, client_port, udp_socket
import os

def main():
	udp_socket.bind((client_ip, client_port))

	msg = input()
	udp_socket.sendto(msg.encode(), (server_ip, server_port))

	if msg == 'start':
		ret = udp_socket.recv(1024).decode()
		print(ret)

	udp_socket.close()




if __name__ == "__main__":
	main()
	os.system("rm -rf __pycache__")
