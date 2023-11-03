#! /bin/python3

# LIBS #########################################################################
from config import server_address, client_port, udp_socket, d_1, d_2, d_3, d_4, d_5, d_6
import os
import socket

# VARIAVEIS GLOBAIS ############################################################
client_address = (0, 0)

# FUNCOES ######################################################################
def show_die(arr):
	die_faces = [d_1, d_2, d_3, d_4, d_5, d_6]
	big = 0
	for i in range(1, 5):
		if arr[i] > arr[big]:
			big = i
	print("\033[1;31mO face mais rolada foi:\033[0m")
	print("\033[1;35m" + die_faces[big] + "\033[0m")

def send(msg):                                                          
	udp_socket.sendto(msg.encode(), server_address)                                     
	return                                                                                

def rcv():     
	ret =  udp_socket.recv(1024).decode()                                               
	return ret

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	local_ip = s.getsockname()[0]
	return local_ip

def bind():
	global client_address

	client_address = (get_ip(), client_port)

	while True:
		try:
			udp_socket.bind(client_address)
			break
		except OSError:
			client_address = (client_address[0], client_address[1] + 1)

def insert_msg_order(msg, msg_order):
	out_of_order = 0
	# Como as mensagens começam em 1, a lógica do array precisou ser feita com este detalhe
	# msg_order[msg-2] é a posição do pacote anterior recebido
	# Array de pacotes vazio ou pacote chegou fora de ordem e "pra cima" (chegou antes do pacote esperado)
	print("Mensagem: " + str(msg))
	if msg_order == [] or msg > (len(msg_order)+1) or msg_order[msg-2] == 0:
		for i in range(msg-1):
			msg_order.append(0)
		msg_order.append(1)
	elif msg < len(msg_order):
		msg_order[msg-1] = 1
	else:
		msg_order.append(1)
	# Pacote chegou fora de ordem (atrasado ou adiantado)
	if (msg_order[msg-2] == 0 or msg < len(msg_order)) and len(msg_order) > 2:
		out_of_order = 1

	#print("msg: " + str(msg))
	#print("msg_order: " + str(msg_order))
	return out_of_order

def calc_pkg_lost(arr):
	summ = 0
	for i in range(len(arr)-1):
		if arr[i] == 0:
			summ += 1
	
	return str(summ)

def client_start():
	arr = [0, 0, 0, 0, 0, 0]
	late_pkgs = 0
	msg_data = []
	msg_order = []

	while True:
		ret = rcv()
		if ret == "FINISH":
			pkg_lost = calc_pkg_lost(msg_order)
			print("SERVER STOP")
			print("UDP PACKAGES LOST: " + pkg_lost)
			print("UDP PACKAGES OUT OF ORDER: " + str(late_pkgs))
			break
		msg, rolled 	= ret.split(',')
		msg 			= int(msg)
		rolled			= int(rolled)
		print(rolled, msg)

		arr[rolled-1] += 1
		msg_data.append(rolled)

		late_pkgs += insert_msg_order(msg, msg_order)
		
		print("ROLOU " + str(rolled))
	return arr
	
# MAIN #########################################################################
def main():
	arr = []
	die = [] * 6;

	bind()
	print(client_address[0], client_address[1])

	msg = input()
	send(msg)

	if msg == 's':
		arr = client_start()
	print(arr)	
	show_die(arr)
	udp_socket.close()




if __name__ == "__main__":
	os.system("rm -f videos_client/*")
	main()
	os.system("rm -rf __pycache__")
