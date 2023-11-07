#! /bin/python3

# LIBS #########################################################################
from config import server_address, client_port, udp_socket, d_1, d_2, d_3, d_4, d_5, d_6
import os
import socket
import time
from datetime import datetime

# VARIAVEIS GLOBAIS ############################################################
client_address = (0, 0)
client_log = []

# FUNCOES ######################################################################

# Recebe o array que representa as faces de um dado e define qual foi 'tirada' mais vezes
def most_rolled_face(arr):
	big = 0
	for i in range(1, 6):
		if arr[i] > arr[big]:
			big = i
	return big

# Printa o desenho da face mais tirada no terminal
def show_die(arr):
	die_faces = [d_1, d_2, d_3, d_4, d_5, d_6]
	big = most_rolled_face(arr)
	print("\033[1;31mO face mais rolada foi:\033[0m")
	print("\033[1;35m" + die_faces[big] + "\033[0m")

# Codifica e envia a mensagem para o servidor
def send(msg):                                                          
	udp_socket.sendto(msg.encode(), server_address)                                     
	return                                                                                

# Recebe e decodifica a mensagem recebida do servidor
def rcv():     
	ret =  udp_socket.recv(1024).decode()                                               
	return ret

# Descobre o IP da máquina onde está sendo executado o programa
def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	local_ip = s.getsockname()[0]
	return local_ip

# Vincula as informações do cliente com o socket
def bind():
	global client_address

	client_address = (get_ip(), client_port)

	while True:
		try:
			udp_socket.bind(client_address)
			break
		except OSError:
			client_address = (client_address[0], client_address[1] + 1)

# A cada mensagem recebida do servidor, determina se ela chegou atrasada/adiantada
# e insere ela no array de mensagens recebidas do servidor
def insert_msg_order(msg, msg_order):
	out_of_order = 0
	# Como as mensagens começam em 1, a lógica do array precisou ser feita com este detalhe
	# msg_order[msg-2] é a posição do pacote anterior recebido
	# Array de pacotes vazio ou pacote chegou fora de ordem e "pra cima" (chegou antes do pacote esperado)
	if msg_order == [] or msg > (len(msg_order)+1) or msg_order[msg-2] == 0:
		# Adiciona 0´s do tamanho do array até o tamanho recebido 
		for i in range(len(msg_order), msg-1):
			msg_order.append(0)
		msg_order.append(1)
	elif msg < len(msg_order):
		msg_order[msg-1] = 1
	else:
		msg_order.append(1)
	# Pacote chegou fora de ordem (atrasado ou adiantado)
	if (msg_order[msg-2] == 0 or msg < len(msg_order)) and len(msg_order) > 2:
		out_of_order = 1

	return out_of_order

# Após a conexão com o servidor ser fechada, calcula
# a quantidade de pacotes/mensagens perdidas
def calc_pkg_lost(arr):
	summ = 0
	for i in range(len(arr)-1):
		if arr[i] == 0:
			summ += 1
			add_msg_log(True, str(i+1), False, False, False)
	
	return str(summ)

# Adiciona uma linha no arquivo de log de acordo com a mensagem recebida,
# que pode ser de pacote perdido, pacote fora de ordem, servidor conectado
# e servidor deconectado 
def add_msg_log(lost, order, out_of_order, init, end):
	timestamp = time.time()

	data_hora = datetime.fromtimestamp(timestamp)
	hora = data_hora.strftime("%H:%M")

	msg = str(data_hora.day) + '/' + str(data_hora.month) + '/' + str(data_hora.year) + " - " + str(hora)
	
	if out_of_order:
		msg = msg + " WARNING - Package " + order + " received out of order \n"
	elif lost:
		msg = msg + " WARNING - Package " + order + " lost \n"
	elif init:
		msg = msg + " SERVER CONNECTED\n"
	elif end:
		msg = msg + " SERVER DISCONNECTED\n"
	else:
		msg = msg + " CONFIRMATION - Package " + order + " received\n"

	client_log.append(msg)

# Adiciona mensagem de fim de programa no arquivo de log
def add_end_msg_log():
	msg = "END OF PROGRAM\n"

	client_log.append(msg)

# Escreve o arquivo de log de fato, onde o arquivo vai ter o nome:
# "nome_da_maquina".txt em um diretório que precisa existir previamente
# chamado "logs"
def write_log_file():
	file_name = str(socket.gethostname()) + ".txt"	

	with open(f"logs/{file_name}", "w") as file:
		file.writelines(client_log)

# Gerencia o recebimento de mensagens enviadas pelo servidor, separa
# a ordem da mensagem do dado em si e trata estas informações com a
# ajuda das funções já descritas acima	
def client_start():
	arr = [0, 0, 0, 0, 0, 0]
	late_pkgs = 0
	out_or_order = False
	msg_data = []
	msg_order = []

	while True:
		ret = rcv()
		if ret == "FINISH":
			msg_stop = "rstop"
			time.sleep(1)
			send(msg_stop)
			add_msg_log(False, False, False, False, True)

			pkg_lost = calc_pkg_lost(msg_order)
			print("SERVER STOP")
			print("UDP PACKAGES LOST: " + pkg_lost)
			print("UDP PACKAGES OUT OF ORDER: " + str(late_pkgs))
			add_end_msg_log()
			break
		msg, rolled 	= ret.split(',')
		msg 			= int(msg)
		rolled			= int(rolled)
		
		if msg == 1:
			add_msg_log(False, False, False, True, False)

		arr[rolled-1] += 1
		msg_data.append(rolled)

		tmp = late_pkgs
		late_pkgs += insert_msg_order(msg, msg_order)

		if tmp != late_pkgs:
			out_or_order = True
		else:
			out_or_order = False
		
		add_msg_log(False, str(msg), out_or_order, False, False)
		
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
	write_log_file()
	udp_socket.close()




if __name__ == "__main__":
	main()
	os.system("rm -rf __pycache__")
