#! /bin/bash

[[ ! $# -eq 1 ]] && \
echo -e "\e[1;31mERROR: incorrect number of arguments
\e[0mUSAGE: cp_config.sh [local,mumm,h1]" && \
exit 1

file=${1}

test=`echo -e "local\nmumm\nh1" | grep -w ${file}`
[[ ! ${test} ]] && \
echo "${file} Não é um arquivo válido" && \
exit 2

cp initFiles/${file}.ini ./cfg.ini
