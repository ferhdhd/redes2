#! /bin/python3

# LIBS #########################################################################
from config import server_address, udp_socket, args
import time
import os
import time
import threading
import socket

# VARIÁVEIS GLOBAIS ############################################################
a = 1103515245
b = 12345
m = 1 << 31
stop_threads = False
msg_range = 0.5
client_list = []

# CLASSES ######################################################################
class Client:
	def __init__(self, address, last_int):
		self.last_int = last_int
		self.address = address
		self.pkg = 1

# FUNCOES ######################################################################

# Cria e adiciona um cliente na lista de clientes cadastrados no servidor
def add_client(address, last_int):
	new_client = Client(address, last_int)
	client_list.insert(0, new_client)

# Remove um cliente específico da lista de clientes
def remove_client(address):
	for client in client_list:
		if client.address == address:
			client_list.remove(client)
			return

# Codifica e envia uma mensagem para o cliente
def send(msg, client):
	udp_socket.sendto(msg.encode(), client)
	return

# Recebe e decodifica uma mesagem recebida de um cliente
def rcv():
	return udp_socket.recv(1024).decode()

# Função que gera um número aleatório que é utilizado para calcular a rolagem do dado
def rnd(last_n):
	last_n = ((a * last_n) + b) % m
	return last_n

# Finaliza a comunicação com um cliente e o remove da lista de clientes cadastrados no servidor
def finish_client(client):
	global client_list
	
	while True:	
		try:
			send("FINISH", client.address)
			ret, addr = udp_socket.recvfrom(1024)
			break
		except socket.timeout:
			continue
	ret = ret.decode()
	if (addr == client.address):
		if (ret == "rstop"):
			client_list.remove(client)


# Finaliza a comunicação com todos os clientes e os remove da lista de clientes cadastrados
def finish_clients():
	global client_list
	udp_socket.settimeout(4)

	while client_list != []:
		for client in client_list:
			send("FINISH", client.address)
			try:
				ret, addr = udp_socket.recvfrom(1024)
			except socket.timeout:
				continue
			ret = ret.decode()
			if (addr == client.address):
				if (ret == "rstop"):
					client_list.remove(client)

# MAIN THREADS #################################################################

# Thread responsável por cuidar da lista de clientes ativos
# Fica a todo momento ouvindo possíveis mensagens de clientes
# Se for do tipo 's' adiciona ele na lista
def main_queue():
	udp_socket.bind(server_address)

	udp_socket.settimeout(1)

	global stop_threads
	
	while not stop_threads:
		data = ""
		try:
			data, client_address = udp_socket.recvfrom(1024)
		except socket.timeout:
			continue
		data = data.decode()
		if (data == 's'):
			ts = round(time.time() * 1000)
			add_client(client_address, ts)
			print("Cliente novo: ", end="")
			print(client_address[0], client_address[1])

# Thread responsável por enviar mensagens para os clientes
# cadastrados no servidor em um intervalo de tempo especificado
# na variável msg_range (que por padrão é 0.5, mas pode ser alterado
# durante a execução do servidor). Se existir a flag -l, envia o
# número especificado após ela. 
def main_send():
	global stop_threads
	
	if args.limit:
		limit = int(args.limit)
	else:
		limit = -1

	while not stop_threads:
		for client in client_list:
			client.last_int	= rnd(client.last_int)
			address = client.address
			roll = str(client.last_int % 6 + 1)
			msg = (str(client.pkg)+","+roll)
			send(msg, address)
			if limit != -1 and client.pkg > limit:
				finish_client(client)
				time.sleep(1)
			client.pkg += 1
		time.sleep(msg_range)

# Thread responsável por lidar com os inputs 'stop' e 'r'.
# O stop para finaliza a conexão com todos os clientes e
# finaliza todas as threads ativas. Já o input r espera um
# novo número que vai servir como novo intervalo de tempo
# para envio de mensagens 
def main_inpt_handler():
	print("Quando quiser mudar a frequência de envio das mensagens, pode digitar 'r 5', onde 5 é o intervalo desejado (em segundos), por exemplo")
	print("O tempo padrão de envio das mensagens é 0.5")
	
	global stop_threads
	global msg_range
	udp_socket.settimeout(1)
	while not stop_threads:
		inpt = input()
		if inpt == 'stop':
			stop_threads = True
			finish_clients()
		elif inpt[0] == 'r':
			msg_range = float(inpt.split(" ")[1])

if __name__ == "__main__":
	queue_thread 		= threading.Thread(target=main_queue)
	send_thread 		= threading.Thread(target=main_send)
	handler_thread	= threading.Thread(target=main_inpt_handler)

	queue_thread.start()
	send_thread.start()
	handler_thread.start()

	queue_thread.join()
	send_thread.join()
	handler_thread.join()

	os.system("rm -rf __pycache__")
