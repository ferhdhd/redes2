#! /bin/python3

# LIBS #########################################################################
import socket
import time
from configparser import ConfigParser

# Variáveis globais ############################################################
init_return = "Iniciado Conexão!!"

def main():
# Bloco de inicialização #######################################################
	# Arquivo de configuração
	cfg			= ConfigParser()
	cfg.read("./initFiles/godp.ini")
	# Configurações de servidor
	local_ip 	= cfg.get('server', 'ip')
	local_port	= int(cfg.get('server', 'port'))
	# Configurações de client
	client_ip	= cfg.get('client', 'ip')
	client_port	= int(cfg.get('client', 'port'))
	# Iniciando o socket
	udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, 0)
	udp_socket.bind((local_ip, local_port))
################################################################################

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
