#!/bin/bash

DIR_PWD=$(pwd)
DIR_APP=$DIR_PWD/app
APP_NME=${PWD##*/}
PIP_INS=$(which python | sed -n "s/.*\(${APP_NME}\).*/\1/p" | wc -l)

if [[ $PIP_INS == 0 ]]; then
  echo -e "[i] Venv active for ${APP_NME}, type exit to deactivate and ./run.sh to run the app in the venv"
  bash -c "source bin/activate; exec /usr/bin/env bash --rcfile <(echo 'PS1=\"(${APP_NME})\${PS1}\"') -i"
else
  echo "[i] Running App from within ... $(pwd)"
  cd $DIR_APP && $DIR_APP/main.py
fi
