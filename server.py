#! /bin/python3

# LIBS #########################################################################
from config import server_address, udp_socket
import time
import os
import time
import threading

# VARIÁVEIS GLOBAIS ############################################################
a = 1103515245
b = 12345
m = 1 << 31
stop_threads = False
client_list = []

# CLASSES ######################################################################
class Client:
	def __init__(self, address, last_int):
		self.last_int = last_int
		self.address = address

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
	
def server_start(client):
	while True:
		send(str(rnd() % 6 + 1), client)
		time.sleep(1)

# MAIN THREADS #################################################################
def main_queue():
	udp_socket.bind(server_address)

	global stop_threads
	
	while not stop_threads:
		data, client_address = udp_socket.recvfrom(1024)
		data = data.decode()
		if (data == 's'):
			ts = round(time.time() * 1000)
			add_client(client_address, ts)

	udp_socket.close()
	

def main_send():
	global stop_threads
	while not stop_threads:
		for client in client_list:
			client.last_int	= rnd(client.last_int)
			address = client.address
			roll = str(client.last_int % 6 + 1)
			send(roll, address)
		time.sleep(2)
def main_interrupt():
	global stop_threads
	while not stop_threads:
		inpt = input()
		if inpt == 'stop':
			stop_threads = True

if __name__ == "__main__":
	queue_thread 		= threading.Thread(target=main_queue)
	send_thread 		= threading.Thread(target=main_send)
	interrupt_thread	= threading.Thread(target=main_interrupt)

	queue_thread.start()
	send_thread.start()
	interrupt_thread.start()

	queue_thread.join()
	send_thread.join()
	interrupt_thread.join()

	os.system("rm -rf __pycache__")
