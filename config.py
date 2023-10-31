#! /bin/python3

# LIBS #########################################################################
import socket
import time
import argparse
from configparser import ConfigParser

# Bloco de inicialização #######################################################

# Parser das opções
parser = argparse.ArgumentParser(description="DiceRoller")
parser.add_argument('-i', "--init_file", dest="init",
default="cfg.ini", help=".ini file to initial setups")
args = parser.parse_args()

# Arquivo de configuração
cfg			= ConfigParser()
cfg.read(args.init)

# Configurações de servidor
server_ip 	= cfg.get('server', 'ip')
server_port	= int(cfg.get('server', 'port'))
server_address = (server_ip, server_port)

# Configurações de client
#client_ip = cfg.get('client', 'ip')
client_port	= int(cfg.get('client', 'port'))
#client_address = (client_ip, client_port)

# Iniciando o socket
udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, 0)
################################################################################
