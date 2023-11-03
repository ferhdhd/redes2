#! /bin/python3

# LIBS #########################################################################
import socket
import time
import argparse
from configparser import ConfigParser

# PARSER DAS OPÇÕES ############################################################
parser = argparse.ArgumentParser(description="DiceRoller")
parser.add_argument('-i', "--init_file", dest="init",
default="cfg.ini", help=".ini file to initial setups")
args = parser.parse_args()

# ARQUIVO DE CONFIGURAÇÃO ######################################################
cfg			= ConfigParser()
cfg.read(args.init)

# CONFIGURAÇÕES DE SERVIDOR ####################################################
server_ip 	= cfg.get('server', 'ip')
server_port	= int(cfg.get('server', 'port'))
server_address = (server_ip, server_port)

# CONFIGURAÇÕES DE CLIENT ######################################################
client_port	= int(cfg.get('client', 'port'))

# INICIANDO O SOCKET ###########################################################
udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, 0)

# STRINGS DE DADO ##############################################################
d_1 = '''\
╭────────────────╮
│                │
│                │
│      ╭──╮      │
│      ╰──╯      │
│                │
│                │
╰────────────────╯\
'''

d_2 = '''\
╭────────────────╮
│           ╭──╮ │
│           ╰──╯ │
│                │
│                │
│ ╭──╮           │
│ ╰──╯           │
╰────────────────╯\
'''

d_3 = '''\
╭────────────────╮
│ ╭──╮           │
│ ╰──╯           │
│      ╭──╮      │
│      ╰──╯      │
│           ╭──╮ │
│           ╰──╯ │
╰────────────────╯\
'''

d_4 = '''\
╭────────────────╮
│ ╭──╮      ╭──╮ │
│ ╰──╯      ╰──╯ │
│                │
│                │
│ ╭──╮      ╭──╮ │
│ ╰──╯      ╰──╯ │
╰────────────────╯\
'''

d_5 = '''\
╭────────────────╮
│ ╭──╮      ╭──╮ │
│ ╰──╯      ╰──╯ │
│      ╭──╮      │
│      ╰──╯      │
│ ╭──╮      ╭──╮ │
│ ╰──╯      ╰──╯ │
╰────────────────╯\
'''

d_6 = '''\
╭────────────────╮
│ ╭──╮      ╭──╮ │
│ ╰──╯      ╰──╯ │
│ ╭──╮      ╭──╮ │
│ ╰──╯      ╰──╯ │
│ ╭──╮      ╭──╮ │
│ ╰──╯      ╰──╯ │
╰────────────────╯\
'''

