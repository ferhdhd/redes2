import socket

udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, 0)

#IP da máquina h1 do dinf 
local_ip = '10.254.223.29'
#Porta para rodar o processo
local_port = 33322

udp_socket.bind((local_ip, local_port))

while (True):
        data = udp_socket.recv(1024)
        print(data.decode())


udp_socket.close()