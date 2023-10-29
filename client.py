#! /bin/python3

# LIBS #########################################################################
from config import server_address, client_address, udp_socket
import os

def send(msg):                                                          
	udp_socket.sendto(msg.encode(), server_address)                                     
	return                                                                                

def rcv():     
	ret =  udp_socket.recv(1024).decode()                                               
	return ret

def client_start():
	while True:
		ret = rcv()
		print("ROLOU " + ret)

def main():
	udp_socket.bind(client_address)

	msg = input()
	send(msg)

	if msg == 's':
		client_start()
	udp_socket.close()




if __name__ == "__main__":
	os.system("rm -f videos_client/*")
	main()
	os.system("rm -rf __pycache__")
