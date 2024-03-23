#!/usr/bin/bash
DIR_PWD=$(pwd)
DIR_ENV=$HOME/python-apps
DIR_APP=$DIR_ENV/oceaneyes

chmod +x $DIR_PWD/*.sh
chmod +x $DIR_PWD/*.py

# Deal with YouTube Downloading
# yt-dlp: The minimum recommended Python version has been raised to 3.8

#rm -f /usr/bin/yt-dlp
#sudo mv -f /usr/bin/yt-dlp /usr/bin/yt-dlp.bckup

# Detect Raspberry Pi ARM
ARC=$(uname -m)

if [[ "${ARC}" == "aarch64" ]]; then
	# RPI
	sudo wget -O /usr/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/download/2023.09.24/yt-dlp_linux_aarch64
	sudo chmod a+x /usr/bin/yt-dlp
else
    	# X86
	sudo wget -nc -O /usr/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_linux
	sudo chmod a+x /usr/bin/yt-dlp
fi

sudo apt install -y python3-dev
sudo apt install -y portaudio19-dev
sudo apt install -y wget vlc ffmpeg icecast2
sudo sed -i 's|<port>8000</port>|<port>3345</port>|g' /etc/icecast2/icecast.xml
sudo sed -i 's|hackme|<port>rdo</port>|g' /etc/icecast2/icecast.xml
sudo /etc/init.d/icecast2 restart

# VENV - Setup
VER_PYT=$(python3 --version | cut -d " " -f2 | cut -d "." -f1-2 | cut -d "" -f1)
if (( $(echo "$VER_PYT == 3.9" | bc -l ) )); then
	sudo apt install -y python3.9-venv
else
	sudo apt install -y python3-venv
fi

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

cp $DIR_PWD/requirements.txt ./

#pip install -r requirements.txt
$DIR_APP/bin/pip3 install -r $DIR_APP/requirements.txt
echo -e "\n\n[i] Installed requirements in the venv ..."

$DIR_APP/bin/pip list && echo -e "\n\n"

mv -f $DIR_APP/app/run.sh $DIR_APP
rm -f $DIR_APP/app/install.sh


# TODO: Support other init systems
install_service () {
	echo -e "\n\n[i] Installing service, in systemd use 'sudo systemctl disable oe.service' to stop it running on boot ..."
	echo -e "[i] To see the status of the service use 'watch systemctl status oe.service'"

	cp $DIR_PWD/oe.service $DIR_PWD/oe.service.tmp
	sed -i "s|~/|$HOME/|g" $DIR_PWD/oe.service.tmp

	cp $DIR_PWD/oe.start $DIR_APP
	cp $DIR_PWD/oe.stop $DIR_APP
	cp $DIR_PWD/oe.status $DIR_APP

	sudo mv $DIR_PWD/oe.service.tmp /lib/systemd/system/oe.service
	sudo systemctl daemon-reload
	sudo systemctl enable oe.service
	sudo systemctl start oe.service

	# watch systemctl status oe.service
}

install_startup () {
	echo -e "\n\n"
	echo -e "[i] To run go to ~/python-apps/oceaneyes"
	echo -e "$ ./run.sh\n\n"

	echo -e "[i] OR to manually start the server in a python venv follow these steps:\n"
	echo "$ cd ~/python-apps/oceaneyes"
	echo "$ source bin/activate oceaneyes"
	echo "$ cd app"
	echo "$ ../bin/python3 main.py"

	echo -e "\n\n"
	echo -e "[i] To re/scan for radios on the network, make sure all your known devices are switched on ..."
	echo -e "$ cd ~/python-apps/oceaneyes/app"
	echo -e "$ ./scan.py"

}

while true; do
    read -p "[Q] Run Oceaneyes as a service? (y/n)" yn
    case $yn in
        [Yy]* ) install_service; break;;
        [Nn]* ) install_startup; break;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo -e "\n\n[i] While the server is starting, turn on your internet radio device then open a browser tab to http://yourip:1929/v1/device/scan"
echo "[i] Scanning may take about 5 minutes"
echo "[i] When done, set your active radio device index in a browser tab http://yourip:1929/v1/device/switch/1"
echo "[i] To play preset 16 copy to a browser tab http://yourip:1929/v1/fav/play/16"
echo -e "\n\n"
echo -e "\n[i] To test the rest of the API go to http://yourip:1929/docs\n\n"

#$DIR_APP/run.sh
