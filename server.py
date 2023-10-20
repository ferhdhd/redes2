#! /bin/python3

# LIBS #########################################################################
from config import server_ip, server_port, client_ip, client_port, udp_socket
import time
import os

# Variáveis globais ############################################################
init_return = "Iniciado Conexão!!"

def main():
	udp_socket.bind((server_ip, server_port))
	while (True):
		data = udp_socket.recv(1024).decode()
		print(data)
		if (data == 'start'):
			udp_socket.sendto(init_return.encode(), (client_ip, client_port))
		if(data == 'q'):
			break
		time.sleep(5)

	udp_socket.close()





if __name__ == "__main__":
	main()
	os.system("rm -rf __pycache__")
