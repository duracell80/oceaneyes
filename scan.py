#!../bin/python3
import sys, os, subprocess, time, logging, socket, requests, urllib, urllib.parse, json
from tinydb import TinyDB, Query

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


# Perform LAN scan
def scan():
	if os.path.isfile("settings.db"):
		dbc     = TinyDB("settings.db")
	else:
		dbc     = TinyDB("settings.db")
		dbc.insert({'ipaddress': '0.0.0.0', 'language': 'English'})

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("1.1.1.1", 80))
	h = s.getsockname()[0].split(".")
	h = str(h[0] + "." + h[1] + "." + h[2])
	s.close()

	hosts   = []
	dev_radios = []
	dev_tuners = []
	d       = 0
	e	= 99
	logging.info("[i] Auto detecting Skytune radios on the LAN, this may take some time ...")
	print("[i] Auto detecting Skytune radios on the LAN ... \n\nPress Ctrl + Z when all known devices are found")
	print("Press Ctrl + C if scanning seems to be stuck\n\n")
	print("--- Tip: Take note of these numbers and then set")
	print("--- static routes on the router for these devices\n\n")
	for i in range(2,256):
		host    = h + "." + str(i)
		try:
			try:
				r = requests.get("http://" + str(host) + ":80", timeout=1)
				if r.status_code == 200:
					p = 80
			except:
				p = 0
				logging.info(f"[i] Looking for a radio at this address ({str(h)}.{str(i)})")

			if p == 80:
				logging.info(f"[i] Looking for a radio at this address ({str(h)}.{str(i)}) [P:80]")

				# test that the radio can be pinged
				result  = str(os.popen("ping " + str(host) + " -w 5 -W 5").read())
			else:
				p = 0
				result = "0 received"
		except:
			p = 0
			result  = "0 received"


		if "5 received" in result:
			try:
				# Detect Skytune Radio
				r = requests.get("http://" + str(host) + "/php/favList.php?PG=0")
				if r.status_code == 200 and 'favListInfo' in r.text:
					d+=1
					dev_radios.append(host)
					dbc.update({'ipaddress': str(host)}, doc_ids=[int(d)])
					logging.info(f"\n[+] Found a skytune radio @{str(host)}:80\n")

			except:
				x=1

			try:
				# Detect HDHomeRun
				g = requests.get("http://" + str(host) + "/lineup.html")
				if g.status_code == 200 and '<title>HDHomeRun Lineup</title>' in g.text:
					e+=1
					dev_tuners.append(host)
					dbc.update({'ipaddress': str(host)}, doc_ids=[int(e)])
					logging.info(f"\n[+] Found a hdhomerun @{str(host)}:80\n")
			except:
				x=1

			hosts.append(host)


	radios = len(dev_radios)

	if radios > 0:
		if radios > 1:
			logging.info(f"\n[i] Found {str(radios)} radios on the network")
		else:
			logging.info(f"\n[i] Found {str(radios)} radio on the network")

		for i in range(0,int(radios)):
			logging.info(f"--- Radio {str(i+1)} @ {str(dev_radios[i])}")

	tuners = len(dev_tuners)

	if tuners > 0:
		if tuners > 1:
			logging.info(f"\n[i] Found {str(tuners)} tuners on the network")
		else:
			logging.info(f"\n[i] Found {str(tuners)} tuner on the network")

		for i in range(0,int(tuners)):
			logging.info(f"--- Tuner {str(i+1)} @ {str(dev_tuners[i])}")

	return hosts, dev_radios

scan()
