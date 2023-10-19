import socket

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

#IP da máquina h2 do dinf
local_ip = '10.254.223.30'
#Porta para rodar o processo
local_port = 33377

server_ip = '10.254.223.29'
server_port = 33322

msg = "Hello World!"

udp_socket.sendto(msg.encode(), (server_ip, server_port))

udp_socket.close()