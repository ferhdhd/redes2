#! /bin/python3

# LIBS #########################################################################
from config import server_address, client_port, udp_socket
import os
import socket

# VARIAVEIS GLOBAIS ############################################################
client_address = (0, 0)

# FUNCOES ######################################################################
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

def calc_pkg_lost(arr):
	summ = 0
	for i in range(len(arr)-1):
		if arr[i+1] - arr[i] > 1:
			summ += 1
			print("Pacotes Recebidos: " + str(arr[i]) + " e " + str(arr[i+1]))
	
	return str(summ)

def client_start():
	lost_msgs = 0
    last_msg = 0
	msg = 0
	while True:
		ret = rcv()
		if ret == "FINISH":
			pkg_lost = calc_pkg_lost(msg_order)
			print("SERVER STOP")
			print("UDP PACKAGES LOST: " + pkg_lost)
			return
		msg = (int(ret.split(',')[0]))
		msg_data.append(int(ret.split(',')[1]))
		
		print("ROLOU " + ret.split(',')[1])

# MAIN #########################################################################
def main():
	bind()
	print(client_address[0], client_address[1])

	msg = input()
	send(msg)

	if msg == 's':
		client_start()
	udp_socket.close()




if __name__ == "__main__":
	os.system("rm -f videos_client/*")
	main()
	os.system("rm -rf __pycache__")
