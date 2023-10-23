#! /bin/python3

# LIBS #########################################################################
from config import server_address, udp_socket
import time
import os
import random

# FUNCOES ######################################################################
def send(msg, client, encode):
	msg = msg.encode() if encode else msg
	udp_socket.sendto(msg, client)
	return

def rcv():
	return udp_socket.recv(1024).decode()

def server_start(client, vc):
	send(vc, client, 1)	
	ret = rcv()
	if(ret != "N"):
		return
	
	print("Sending " + vc + " video data")
	window = 512
	with open("videos_server/" + vc, "rb") as file:
		i = 0
		while True:
			file_bin = file.read(window)
			if not file_bin:
				break
			send(file_bin, client, 0)
			print("Enviado! msg ", + i)
			i += 1	
			#print(file_bin)
	final_msg = "Fim do Arquivo"

	send(final_msg, client, 1)
	return

# MAIN #########################################################################
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
