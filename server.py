#! /bin/python3

# LIBS #########################################################################
from config import server_address, udp_socket
import time
import os
import random

# Variáveis globais ############################################################

def server_start(client, vc):
	udp_socket.sendto(vc.encode(), client)
	return

def main():
	videos = os.listdir("videos_server")

	udp_socket.bind(server_address)
	while (True):
		data, client_address = udp_socket.recvfrom(1024)
		data = data.decode()
		
		print(data)
		if (data == 'start'):
			vc = random.choice(videos)
			server_start(client_address, vc)
		if(data == 'q'):
			break

	udp_socket.close()





if __name__ == "__main__":
	main()
	os.system("rm -rf __pycache__")
