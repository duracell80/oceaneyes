#!/usr/bin/bash
# DEV
#pip install beautifulsoup4
#pip install html5lib
#pip install requests_html
#pip install pyradios

# PROD
pip install fastapi uvicorn[standard]
pip install python-vlc
pip install opml
pip install tinydb

sudo apt install -y wget vlc icecast2
sudo sed -i 's|<port>8000</port>|<port>3345</port>|g' /etc/icecast2/icecast.xml
sudo /etc/init.d/icecast2 restart

#sudo apt install yt-dlp
sudo wget -O /usr/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_linux
sudo chmod a+x /usr/bin/yt-dlp
yt-dlp -U
