#! /bin/python3

# LIBS #########################################################################
from config import server_address, client_address, udp_socket
import os

def send(msg):                                                          
	udp_socket.sendto(msg.encode(), server_address)                                     
	return                                                                                

def rcv(decode):     
	ret =  udp_socket.recv(1024)                                               
	ret = ret.decode() if decode else ret
	return ret

def client_start():
	ret = rcv(1)
	print("Creating file " + ret)	
	file = open("videos_client/" + ret, "w")
	
	send("N")

	ret = rcv(0)	
	while(ret):
		file.write(ret)
		ret = rcv()
	
	file.close()
	return

def main():
	udp_socket.bind(client_address)

	msg = input()
	send(msg)

	if msg == 'start':
		client_start()

	udp_socket.close()




if __name__ == "__main__":
	os.system("rm -f videos_client/*")
	main()
	os.system("rm -rf __pycache__")
