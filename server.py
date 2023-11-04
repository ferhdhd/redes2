#! /bin/python3

# LIBS #########################################################################
from config import server_address, udp_socket
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
def add_client(address, last_int):
	new_client = Client(address, last_int)
	client_list.insert(0, new_client)

def remove_client(address):
	for client in client_list:
		if client.address == address:
			client_list.remove(client)
			return

def send(msg, client):
	udp_socket.sendto(msg.encode(), client)
	return

def rcv():
	return udp_socket.recv(1024).decode()

def rnd(last_n):
	last_n = ((a * last_n) + b) % m
	return last_n

def finish_clients():
	global client_list

	for client in client_list:
		send("FINISH", client.address)

# MAIN THREADS #################################################################
def main_queue():
	udp_socket.bind(server_address)

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

def main_send():
	global stop_threads
	while not stop_threads:
		for client in client_list:
			client.last_int	= rnd(client.last_int)
			address = client.address
			roll = str(client.last_int % 6 + 1)
			msg = (str(client.pkg)+","+roll)
			client.pkg += 1
			send(msg, address)
		time.sleep(msg_range)

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
			print(msg_range)

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
