#!/bin/bash

DIR_PWD=$(pwd)
DIR_APP=$DIR_PWD/app

if [ -d "./bin" ];then
  echo "[i] Press Ctrl+D to deactivate"
  bash -c ". bin/activate; exec /usr/bin/env bash --rcfile <(echo 'PS1=\"(oceaneyes)\${PS1}\"') -i"
  cd ./app
else
  echo "[i] Venv active ... cd ./app && ./main.py"
fi
