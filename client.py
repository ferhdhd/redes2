#! /bin/python3

import socket
from configparser import ConfigParser


def main():
# Bloco de inicialização #######################################################
	# Arquivo de configuração
	cfg 		= ConfigParser()
	cfg.read("./surpflix.ini")
	# Configurações de cliente
	local_ip 	= cfg.get('client', 'ip')
	local_port 	= int(cfg.get('client', 'port'))
	# Configurações de servidor
	server_ip	= cfg.get('server', 'ip')
	server_port	= int(cfg.get('server', 'port'))
	# Iniciando o socket
	udp_socket 	= socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
################################################################################
	
	msg = input()
	if msg == '':
		msg = "Hello, World!"
	
	udp_socket.sendto(msg.encode(), (server_ip, server_port))
	udp_socket.close()




if __name__ == "__main__":
	main()
