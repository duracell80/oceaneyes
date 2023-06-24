#!/usr/bin/python3
import os, socket, requests

# Perform LAN scan
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("1.1.1.1", 80))
h = s.getsockname()[0].split(".")
h = str(h[0] + "." + h[1] + "." + h[2])
s.close()

hosts   = []
devices = []

print("[i] LAN scan in progress ... takes about 5 minutes")
for i in range(19,22):
	host 	= h + "." + str(i)
	result 	= str(os.popen("ping " + str(host) + " -w 1").read())
	if "1 received" in result:
		r = requests.get("http://" + str(host) + "/php/favList.php?PG=0")
		if r.status_code == 200:
			devices.append(host)
		hosts.append(host)

radios = len(devices)
if radios > 0:
	if radios > 1:
		print("\n[i] Found " + str(radios) + " Skytune radio1 on the network")
	else:
		print("\n[i] Found " + str(radios) + " Skytune radios on the network")
	for i in range(0,int(radios)):
		print("--- Radio " + str(i+1) + " @" + str(devices[i]))
