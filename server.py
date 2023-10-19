#! /bin/python3

import socket
from configparser import ConfigParser

def main():
# Bloco de inicialização #######################################################
	# Arquivo de configuração
	cfg			= ConfigParser()
	cfg.read("./surpflix.ini")
	# Configurações de servidor
	local_ip 	= cfg.get('server', 'ip')
	local_port	= int(cfg.get('server', 'port'))
	# Iniciando o socket
	udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, 0)
	udp_socket.bind((local_ip, local_port))
################################################################################

	while (True):
		data = udp_socket.recv(1024)
		print(data.decode())
		if (data.decode() == 'q'):
			break

	udp_socket.close()





if __name__ == "__main__":
	main()
