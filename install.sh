#!/usr/bin/bash
DIR_PWD=$(pwd)
DIR_ENV=$HOME/python-apps
DIR_APP=$DIR_ENV/oceaneyes

sudo apt install -y wget vlc ffmpeg icecast2
sudo sed -i 's|<port>8000</port>|<port>3345</port>|g' /etc/icecast2/icecast.xml
sudo sed -i 's|hackme|<port>rdo</port>|g' /etc/icecast2/icecast.xml
sudo /etc/init.d/icecast2 restart

#rm -f /usr/bin/yt-dlp
sudo mv -f /usr/bin/yt-dlp /usr/bin/yt-dlp.bckup

#X86
#sudo wget -nc -O /usr/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_linux
#sudo chmod a+x /usr/bin/yt-dlp

#RPI
sudo wget -O /usr/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/download/2023.09.24/yt-dlp_linux_aarch64
sudo chmod a+x /usr/bin/yt-dlp

# VENV - Setup
sudo apt install -y python3.9-venv
mkdir -p $DIR_ENV && cd $DIR_ENV

# VENV - OceanEyes
python3 -m venv oceaneyes
source $DIR_APP/bin/activate


# VENV - Install requirements
mkdir -p $DIR_APP/app
cd $DIR_APP

cp $DIR_PWD/*.sh $DIR_APP/app
cp $DIR_PWD/*.db $DIR_APP/app
cp $DIR_PWD/*.py $DIR_APP/app
cp $DIR_PWD/export-rpp.json $DIR_APP/app

cp $DIR_PWD/oe.start $DIR_APP
cp $DIR_PWD/oe.stop $DIR_APP
cp $DIR_PWD/oe.status $DIR_APP

cp $DIR_PWD/requirements.txt ./
pip install -r requirements.txt

mv -f $DIR_APP/app/run.sh $DIR_APP
rm -f $DIR_APP/app/install.sh

cp $DIR_PWD/oe.service $DIR_PWD/oe.service.tmp
sed -i "s|~/|$HOME/|g" $DIR_PWD/oe.service.tmp
sudo mv $DIR_PWD/oe.service.tmp /lib/systemd/system/oe.service
sudo systemctl daemon-reload
sudo systemctl enable oe.service
sudo systemctl start oe.service

#$DIR_APP/run.sh

cd $DIR_APP
echo "[i] Installed requirements in the venv ..."
$DIR_APP/bin/pip list
sleep 3

watch systemctl status oe.service
