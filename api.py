#!/usr/bin/python3
import os, sys, time, logging
import oceaneyes as oe

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.responses import PlainTextResponse
app = FastAPI()


global ip, url

settings, url, ip = oe.init()






@app.post("/v1/fav/add", status_code=200)
async def fav_add(n, u):
	if "http" in u:
		c = "1;1;-1"
		g = "2;68"

		code, station = oe.add(str(n), str(u), str(c), str(g), False)
		if code == 200:
			return '{"result": ' + str(code) + ', "message": "Added: ' + str(station) + '"}'
		elif code == 404:
			return '{"result": ' + str(code) + ', "message": "Not Found: ' + str(station) + '"}'
		else:
			return '{"result": ' + str(code) + ', "message": "Failed to add: ' + str(station) + '"}'
	else:
		return '{"result": 500, "message": "Failed to add: ' + str(station) + '"}'


@app.get("/v1/device/scan", status_code=200)
async def scan():
	hosts, devices = oe.scan()
	radios = len(devices)
	radiol = ""
	if radios > 0:
		for i in range(0,int(radios)):
			radiol += "Radio " + str(i+1) + "@" + str(devices[i]) + ","

		return '{"result": 200, "message": "' + str(radios) + ' radio(s) found on this network ", "devices": "' + str(radiol) + '", "webhosts": "' + str(hosts) + '"}'
	else:
		return '{"result": 404, "message": "No radios found on this network", "webhosts": "' + str(hosts) + '"}'


@app.get("/v1/device/status/{device}", status_code=200)
async def online(device):
	#global settings, url, ip
	ssettings, surl, sip = oe.init(device)

	if oe.is_online():
		logging.info(f"[i] Status of radio@{ip}: online")
		return '{"result": 200, "status": "online", "ipaddr": ' + str(sip)  + '}'
	else:
		logging.info(f"[i] Status of radio@{ip}: offline")
		return '{"result": 400, "status": "offline, "ipaddr": ' + str(sip)  + '}'

@app.get("/v1/device/switch/{device}", status_code=200)
async def switch(device):
	global settings, url, ip
	settings, url, ip = oe.init(device)

	return '{"result": 200, "status": "active", "message": "Active device switched to radio "' + str(device)  + ', "ipaddr": ' + str(ip)  + '}'



@app.get("/v1/device/app", status_code=200)
async def loadapp():
	if oe.is_online():
		logging.info(f"[i] Loading the native webapp of radio@{ip}")
		response = RedirectResponse(url=str(url))
		return response
	else:
		return '{"result": 200, "status": "offline", "message": "Please turn on the radio", "ipaddr": ' + str(ip)  + '}'

@app.get("/v1/playing", status_code=200)
async def status():
	code, status, playing = oe.get_status()
	if code == 200:
		logging.info(f"[i] Status of radio@{ip}: playing - {playing} [{code}]")
		return '{"result": 200, "status": "playing", "message": "' + str(playing)  + '", "ipaddr": ' + str(ip)  + '}'
	else:
		logging.info(f"[i] Status of radio@{ip}: stopped (or FM/DAB playing)")
		return '{"result": 200, "status": "stopped", "message": "None", "ipaddr": ' + str(ip)  + '}'

@app.get("/v1/volume/up", status_code=200)
async def volume_up():
	return str(oe.volume("up"))

@app.get("/v1/volume/down", status_code=200)
async def volume_dn():
	return str(oe.volume("down"))

@app.get("/v1/volume/mute", status_code=200)
async def volume_mu():
	return str(oe.volume("mute"))

@app.get("/v1/volume/unmute", status_code=200)
async def volume_um():
	return str(oe.volume("unmute"))

@app.get("/v1/fav/vacant", status_code=200)
async def fav_remaining():
	return '{"value": "' + str(oe.get_remaining("fav")) + '"}'

@app.get("/v1/fav/engaged", status_code=200)
async def fav_total():
	return '{"value": "' + str(oe.get_total("fav")) + '"}'

@app.get("/v1/fav/save", status_code=200)
async def fav_save():
	code, station = oe.add_current()
	if code == 200:
		return '{"result": 200", "message": "' + str(station)  + ' added to favourites"}'
	else:
		return '{"result": 400, "message": "Currently playing station not saved to favourites"}'

@app.get("/v1/fav/backup", status_code=200)
async def fav_backup():
	list = oe.get_list("backup", False)
	message = "Exported from radio@" + str(ip) + " to local database stations.db"
	logging.info(f"[i] : {message}")
	return '{"result": 200, "message": "' + str(message) + '", "stations:", "' + str(list) + '"}'

@app.get("/v1/fav/play/{c}", status_code=200)
async def fav_play(c):
	if c.isnumeric():
		logging.info(f"[i] Request to play preset {str(c)} on radio@{ip} ... checking stream")
		chid, chname, churl, country_str, genre_str = oe.info_get(str(c))
		if oe.is_streamable(str(churl), False):
			code, message, playing = oe.play(str(c))
			if code == 200:
				logging.info(f"[i] Playing preset {str(int(chid) + 1)} on radio@{ip}")
				logging.info(f"--- {churl}")
				return '{"result": ' + str(code) + ', "message": "' + str(message) + '"}'
			else:
				logging.info(f"[i] Cannot play preset {str(int(chid) + 1)} on radio@{ip} ... Preset out of range")
				return '{"result": ' + str(code) + ', "message": "Preset may be out of range"}'
		else:
			logging.info(f"[i] Cannot play preset {str(int(chid) + 1)} on radio@{ip}")
			logging.info(f"--- {churl}")
			return '{"result": 404, "message": "Station not streamable"}'
	else:
		return '{"result": 500, "message": "Preset not a number, try requesting with an integer value"}'


@app.get("/v1/fav/listen/vlc/{chid}", status_code=200)
async def fav_listen(chid):
	if chid.isnumeric():
		code, message = oe.listen(str(chid))
		if code == 200:
			return '{"result": ' + str(code) + ', "message": "' + str(message) + '"}'
		else:
			return '{"result": ' + str(code) + ', "message": "Preset may be out of range"}'

	else:
		return '{"result": 500, "message": "Preset index not a number, try requesting with an integer value"}'


@app.get("/v1/fav/listen/browser/{chid}", status_code=200)
async def fav_listen(chid):
	if chid.isnumeric():
		ichid 		= chid
		chname 		= "not set"
		churl		= "not set"
		country_str	= "not set"
		genre_str	= "not set"

		if oe.is_online():
			chid, chname, churl, country_str, genre_str = oe.info_get(str(int(chid)))
		else:
			chid, chname, churl, chcountry, chgenre = oe.info_cached(str(int(chid)))

		if "http" in str(churl):
			logging.info(f"[i] Listening to preset {str(int(chid) + 1)} from radio@{ip} on a local device")
			logging.info(f"--- proxyto={churl}")
			response = RedirectResponse(url=str(churl))
			return response
		else:
			logging.info(f"[i] Listening to preset {chid} from radio@{ip} not possible or is masked by skytune")
			return '{"result": 400, "message": "Prest may not be playable"}'

	else:
		logging.info(f"[i] Attempting to listen to preset {ichid} and input is not a number, try an integer")
		return '{"result": 500, "message": "Preset index not a number, try requesting with an integer value"}'

@app.get("/v1/fav/playlist/{format}", status_code=200)
async def fav_playlist(format = "m3u"):
	if format == "pls":
		list = oe.get_list("pls")
	elif format == "m3u":
		list = oe.get_list("m3u")
	elif format == "json":
		list = oe.get_list("json")
	elif format == "csv":
		list = oe.get_list("csv")
	elif format == "ssv":
		list = oe.get_list("ssv")
	elif format == "plain":
		list = oe.get_list("plain")
	else:
		list = oe.get_list("m3u")

	response = PlainTextResponse(content=str(list), status_code=200)
	return response

@app.get("/v1/fav/sync/linux-mint", status_code=200)
async def fav_rpp(format = "json-rpp"):
	code = os.system("cinnamon --version")
	if code == 32512:
		return '{"result": 500, "message": "Linux Mint or Cinnamon Desktop Environment not detected on server"}'
	else:
		message = oe.get_list("json-rpp")
		code = 200

		return '{"result": ' + str(code) + ', "message": ' + str(message) + '}'


@app.get("/v1/fav/move/{r}", status_code=200)
async def fav_move(r):
	if ":" in r:
		r_bits = r.split(":")
		if r_bits[0].isnumeric() and r_bits[1].isnumeric() and r_bits[0].isdigit() and r_bits[1].isdigit():
			code, message = oe.move(str(r_bits[0]), str(r_bits[1]))
			if code == 200:
				logging.info(f"[i] Moved preset from {r_bits[0]} to {r_bits[1]}")
				return '{"result": ' + str(code) + ', "message": ' + str(message) + '}'
			else:
				logging.info(f"[!] Preset move failed")
				return '{"result": ' + str(code) + ', "message": ' + str(message) + '}'
		else:
			logging.info(f"[!] Preset move failed, input given needed to be integers")
			return '{"result": 500, "message": "To move a preset to another position supply in this format 2:20 to move from 2 to 20"}'
	else:
		logging.info(f"[!] To move a preset to another position supply in this format 2:20 to move from 2 to 20")
		return '{"result": ' + str(code) + ', "message": "To move a preset to another position supply in this format 2:20 to move from 2 to 20"}'












@app.get("/v1/search/radiobrowser/{keywords}", status_code=200)
async def search(keywords):
	code, result = oe.search(str(keywords), "RadioBrowser", False)
	if code == 200:
		return result
	else:
		return '{"chname": "Station Not Found", "churl": "https://streaming.radio.co/s5c5da6a36/listen"}'

@app.get("/v1/search/tunein/{keywords}", status_code=200)
async def search(keywords):
	code, result = oe.search(str(keywords), "TuneIn", False)
	if code == 200:
		return result
	else:
		return '{"chname": "Station Not Found", "churl": "https://streaming.radio.co/s5c5da6a36/listen"}'

















def main():
	global ip
	settings, stations = oe.init("192.168.2.20")
	ip = settings["ipaddress"]

	print("main")

	if oe.is_online():

		print(oe.status())

		fav_remaining  = oe.get_remaining("fav")
		fav_total      = oe.get_total("fav")

		#print("Presets: Total=" + str(fav_total) + " Remaining=" + str(fav_remaining))
	else:
		x=1+1

if __name__ == "__main__":
	main()
