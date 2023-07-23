kill -9 "$(ps aux | grep -i "nrsc5" | head -n1 | cut -d " " -f10)"

if [ -x "$(nrsc5 -v)" ]; then
	kill -9 "$(ps aux | grep -i "nrsc5" | head -n1 | cut -d " " -f10)"
else
	exit 1
fi
