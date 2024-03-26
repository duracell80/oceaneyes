#!../bin/python3
import os, sys, subprocess, requests, urllib.parse, time, logging
from threading import Thread

import oceaneyes as oe

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
app = FastAPI()


global sip, ip, url, pid_fm
sip = oe.get_serverip()
settings, url, ip = oe.init()


def isfloat(sin):
	if sin.replace(".", "").isnumeric():
		return True
	else:
		return False



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


@app.get("/v1/{device}/status", status_code=200)
async def online(device):
	settings, surl, sip = oe.init(device)

	if oe.is_online() and device.isnumeric():
		logging.info(f"[i] Status of radio@{ip}: online")
		return '{"result": 200, "status": "online", "ipaddr": ' + str(sip)  + '}'
	else:
		logging.info(f"[i] Status of radio@{ip}: offline")
		return '{"result": 400, "status": "offline, "ipaddr": ' + str(sip)  + '}'

@app.get("/v1/{device}/activate", status_code=200)
async def switch(device):
	if device.isnumeric():
		global settings, url, ip
		settings, url, ip = oe.init(device)

		return '{"result": 200, "status": "active", "message": "Active device switched to radio "' + str(device)  + ', "ipaddr": ' + str(ip)  + '}'
	else:
		return '{"result": 500, "status": "error", "message": "Device index needs to be a number", "ipaddr": 0.0.0.0}'

@app.get("/v1/{device}/app", status_code=200)
async def loadapp_device(device):
	settings, settings_url, settings_ip = oe.switch(device)
	if oe.is_online(settings_ip) and device.isnumeric():
		logging.info(f"[i] Loading the native webapp of radio@{settings_ip}")
		response = RedirectResponse(url=str(settings_url))
		return response
	else:
		return '{"result": 200, "status": "offline", "message": "Please turn on the radio", "ipaddr": ' + str(ip)  + '}'


@app.get("/v1/{device}/playing", status_code=200)
async def status(device):
	settings, settings_url, settings_ip = oe.switch(device)

	if oe.is_online(settings_ip) and device.isnumeric():
		code, status, playing = oe.get_status(settings_ip)
		if code == 200:
			logging.info(f"[i] Status of radio@{settings_ip}: playing - {playing} [{code}]")
			return '{"result": 200, "status": "playing", "message": "' + str(playing)  + '", "ipaddr": ' + str(ip)  + '}'
		else:
			logging.info(f"[i] Status of radio@{settings_ip}: stopped (or FM/DAB playing)")
			return '{"result": 200, "status": "stopped", "message": "None or FM/DAB", "ipaddr": ' + str(ip)  + '}'
	else:
		return '{"result": 500, "status": "error", "message": "Device index needs to be a number", "ipaddr": 0.0.0.0}'

@app.get("/v1/{device}/volume/up", status_code=200)
async def volume_up(device):
	settings, settings_url, settings_ip = oe.switch(device)
	return str(oe.volume(int(device), "up"))

@app.get("/v1/{device}/volume/down", status_code=200)
async def volume_dn(device):
	settings, settings_url, settings_ip = oe.switch(device)
	return str(oe.volume(int(device), "down"))

#@app.get("/v1/{device}/volume/toggle", status_code=200)
#async def volume_tg(device):
#	settings, settings_url, settings_ip = oe.switch(device)
#	return str(oe.volume(int(device), "toggle"))

@app.get("/v1/{device}/volume/mute", status_code=200)
async def volume_mu(device):
	settings, settings_url, settings_ip = oe.switch(device)
	return str(oe.volume(int(device), "mute"))

@app.get("/v1/{device}/volume/unmute", status_code=200)
async def volume_um(device):
	settings, settings_url, settings_ip = oe.switch(device)
	return str(oe.volume(int(device), "unmute"))

@app.get("/v1/{device}/fav/vacant", status_code=200)
async def fav_remaining(device):
	settings, settings_url, settings_ip = oe.switch(device)
	return '{"value": "' + str(oe.get_remaining(int(device), "fav")) + '"}'

@app.get("/v1/{device}/fav/engaged", status_code=200)
async def fav_total(device):
	settings, settings_url, settings_ip = oe.switch(device)
	return '{"value": "' + str(oe.get_total(int(device), "fav")) + '"}'

@app.get("/v1/{device}/fav/save-current", status_code=200)
async def fav_save(device):
	settings, settings_url, settings_ip = oe.switch(device)

	code, station = oe.add_current(int(device))
	if code == 200:
		return '{"result": 200", "message": "' + str(station)  + ' added to favourites"}'
	else:
		return '{"result": 400, "message": "Currently playing station not saved to favourites"}'

@app.get("/v1/{device}/fav/backup", status_code=200)
async def fav_backup(device):
	settings, settings_url, settings_ip = oe.switch(device)

	list = oe.get_list(int(device), "backup", False)
	message = "Exported from radio@" + str(settings_ip) + " to local database ~/python-apps/oceaneyes/app/stations_device" + str(device) + ".db"
	logging.info(f"[i] : {message}")
	return '{"result": 200, "message": "' + str(message) + '", "stations:", "' + str(list) + '"}'

@app.get("/v1/{device}/fav/play/{c}", status_code=200)
async def fav_play(device = 1, c = 1):
	if c.isnumeric():
		settings, settings_url, settings_ip = oe.switch(device)

		logging.info(f"[i] Request to play preset {str(c)} on radio@{settings_ip} ... checking stream")
		chid, chname, churl, country_str, genre_str = oe.info_get(int(device), str(c))
		#streamable = oe.is_streamable(str(churl), False)
		streamable = True

		if streamable:
			code, message, playing = oe.play(int(device), str(c))
			if code == 200:
				logging.info(f"[i] Playing preset {str(int(chid) + 1)} on radio@{settings_ip}")
				logging.info(f"--- {churl}")
				return '{"result": ' + str(code) + ', "message": "' + str(message) + '"}'
			else:
				logging.info(f"[i] Cannot play preset {str(int(chid) + 1)} on radio@{settings_ip} ... Preset out of range")
				return '{"result": ' + str(code) + ', "message": "Preset may be out of range"}'
		else:
			logging.info(f"[i] Cannot play preset {str(int(chid) + 1)} on radio@{settings_ip}")
			logging.info(f"--- {churl}")
			return '{"result": 404, "message": "Station not streamable"}'
	else:
		return '{"result": 500, "message": "Preset not a number, try requesting with an integer value"}'


@app.get("/v1/{device}/streamto/vlc/{chid}", status_code=200)
async def fav_stream_vlc(device = 1, chid = 1):
	if chid.isnumeric():
		settings, settings_url, settings_ip = oe.switch(device)

		code, message = oe.listen(int(device), str(chid))
		if code == 200:
			return '{"result": ' + str(code) + ', "message": "' + str(message) + '"}'
		else:
			return '{"result": ' + str(code) + ', "message": "Preset may be out of range"}'

	else:
		return '{"result": 500, "message": "Preset index not a number, try requesting with an integer value"}'


@app.get("/v1/{device}/streamto/browser/{chid}", status_code=200)
async def fav_stream_browser(device = 1, chid = 1):
	if chid.isnumeric():
		settings, settings_url, settings_ip = oe.switch(device)

		ichid 		= chid
		chname 		= "not set"
		churl		= "not set"
		country_str	= "not set"
		genre_str	= "not set"

		if oe.is_online(settings_ip):
			chid, chname, churl, country_str, genre_str = oe.info_get(int(device), str(int(chid)))
		else:
			chid, chname, churl, chcountry, chgenre = oe.info_cached(int(device), str(int(chid)))

		if "http" in str(churl):
			logging.info(f"[i] Listening to preset {str(int(chid) + 1)} from radio@{settings_ip} on a local browser")
			logging.info(f"--- proxyto={churl}")
			response = RedirectResponse(url=str(churl))
			return response
		else:
			logging.info(f"[i] Listening to preset {chid} from radio@{settings_ip} not possible or is masked by skytune")
			return '{"result": 400, "message": "Prest may not be playable"}'

	else:
		logging.info(f"[i] Attempting to listen to preset {ichid} and input is not a number, try an integer")
		return '{"result": 500, "message": "Preset index not a number, try requesting with an integer value"}'





@app.get("/v1/{device}/fav/playlist/{format}", status_code=200)
async def fav_playlist(device = 1, format = "m3u"):

	settings, settings_url, settings_ip = oe.switch(device)

	if format == "pls":
		list = oe.get_list(int(device), "pls")
	elif format == "m3u":
		list = oe.get_list(int(device), "m3u")
	elif format == "m3u-yt":
		list = oe.get_list(int(device), "m3u-yt")
	elif format == "json":
		list = oe.get_list(int(device), "json")
		list = str(list).replace("'", "")
		response = PlainTextResponse(content=list, status_code=200)
		response.headers["content-type"] = "application/json"

		return response
	elif format == "json-yt":
		list = oe.get_list(int(device), "json-yt")
		response = PlainTextResponse(content=list, status_code=200)
		response.headers["content-type"] = "application/json"

		return response
	elif format == "csv":
		list = oe.get_list(int(device), "csv")
	elif format == "ssv":
		list = oe.get_list(int(device), "ssv")
	elif format == "plain":
		list = oe.get_list(int(device), "plain")
	else:
		list = oe.get_list(int(device), "m3u")

	response = PlainTextResponse(content=str(list), status_code=200)
	return response

#installed_cinnamon = subprocess.getoutput('cinnamon --version')
#if "cinnamon" in installed_cinnamon.lower():
@app.get("/v1/fav/sync/linux-mint", status_code=200)
async def fav_rpp(format = "json-rpp"):
	message = oe.get_list("json-rpp")
	code = 200

	return '{"result": ' + str(code) + ', "message": ' + str(message) + '}'

@app.get("/v1/fav/sync/radioplusplus", status_code=200)
async def fav_rpp(format = "json-rpp-out"):
	message = oe.get_list("json-rpp-out")
	#code = 200
	#return '{"result": ' + str(code) + ', "message": ' + str(message) + '}'

	response = PlainTextResponse(content=message, status_code=200)
	response.headers["content-type"] = "application/json"

	return response

# INPUT FORMAT - from:to for example move channel 20 to 25 ... /v1/fav/move/20:25
@app.get("/v1/{device}/fav/move/{r}", status_code=200)
async def fav_move(device = 1, r = "1:2"):
	settings, settings_url, settings_ip = oe.switch(device)

	if ":" in r:
		r_bits = r.split(":")
		if r_bits[0].isnumeric() and r_bits[1].isnumeric() and r_bits[0].isdigit() and r_bits[1].isdigit():
			code, message = oe.move(int(device), str(r_bits[0]), str(r_bits[1]))
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




@app.get("/v1/listen/fmradio/{f}", status_code=200)
async def listen_fmradio(f = "90.3"):
	if isfloat(str(f)):
		url_rdio = "http://"+ str(sip) +":3345/fmradio-" + str(f)
		url_rm3u = "http://"+ str(sip) +":3345/fmradio" + str(f) + ".m3u"

		thread_fm = Thread(target=lambda: oe.fmradio(str(f), f"Local FM Radio - {f}Mhz", "3345", "rdo"))
		thread_fm.start()
		time.sleep(8)

		pid_fm = os.system('ps aux | grep -i "rtl_fm" | head -n1 | cut -d " " -f9')
		logging.info(f"[i] FM Tuner PID: {pid_fm}")

		response = RedirectResponse(url=str(url_rdio))
		return response
	else:
		return '{"result": 500, "message": "Supply the FM frequency for example listen/fmradio/90.3"}'


@app.get("/v1/listen/wxradio/{f}", status_code=200)
async def listen_wxradio(f = "162.50"):
	if isfloat(str(f)):
		url_rdio = "http://"+ str(sip) +":3345/wxradio"
		url_rm3u = "http://"+ str(sip) +":3345/wxradio.m3u"

		thread_wx = Thread(target=lambda: oe.wxradio(str(f), f"Local WX Radio - {f}Mhz", "3345", "rdo"))
		thread_wx.start()
		time.sleep(8)

		pid_wx = os.system('ps aux | grep -i "rtl_fm" | head -n1 | cut -d " " -f9')
		logging.info(f"[i] FM Tuner PID: {pid_wx}")

		response = RedirectResponse(url=str(url_rdio))
		return response
	else:
		return '{"result": 500, "message": "Supply the FM frequency for example listen/fmradio/90.3"}'


@app.get("/v1/listen/hdradio/{c}/{p}", status_code=200)
async def listen_hdradio(c = "90.3", p = "0" ):
	if isfloat(str(c)) and p.isnumeric():
		url_rdio = "http://"+ str(sip) +":3345/hdradio-" + str(c) + "-" + str(p)
		url_rm3u = "http://"+ str(sip) +":3345/hdradio-" + str(c) + "-" + str(p) + ".m3u"

		thread_fm = Thread(target=lambda: oe.hdradio(str(c), str(p), f"Local HD Radio - {c}Mhz P:{p}", "3345", "rdo"))
		thread_fm.start()
		time.sleep(15)

		response = RedirectResponse(url=str(url_rdio))
		return response
	else:
		return '{"result": 500, "message": "Supply the FM frequency and then the hybrid program index for example listen/hdradio/90.3/0"}'


# For listening to newer stream technology such as HLS or FLAC on older equipment (transcoding to Vorbis to help retain quality)
@app.get("/v1/listen/cdradio", status_code=200)
async def listen_cdradio(s = "https://hls.somafm.com/hls/groovesalad/FLAC/program.m3u8"):
	if "http" in str(s).lower():
		url_prox = "http://"+ str(sip) +":3372/cdradio.ogg"
		os.system("cvlc " + str(s) +" --prefetch-buffer-size=8000 --sout-mux-caching=8000 --sout '#transcode{acodec=vorb,ab=320}:standard{access=http,mux=ogg,dst=" + str(sip) + ":3372/cdradio.ogg}'")
		time.sleep(3)

		return '{"result": 200, "message": "Add this url to your radio device: "' + str(url_prox) + '}'
	else:
		return '{"result": 500, "message": "Supply the url with protocol for example https://hls.somafm.com/hls/groovesalad/FLAC/program.m3u8"}'


@app.get("/v1/listen/ytradio/{c}/{p}/{n}", status_code=200)
async def listen_ytradio(c = "jfKfPfyJRdk", p = "91", n = "YouTube Radio" ):
	if p.isnumeric():
		thread_yt = Thread(target=lambda: oe.ytradio(str(c), str(p), str(n), "3345", "rdo"))
		thread_yt.start()
		time.sleep(10)
		url_rdio = "http://" + str(sip) + ":3345/ytradio-" + str(c)
		url_rm3u = "http://" + str(sip) + ":3345/ytradio-" + str(c) + ".m3u"

		response = RedirectResponse(url=str(url_rdio))
		return response

		#return '{"result": 200, "message": "Add this url to your radio device: "' + str(url_prox) + '"}'
	else:
		return '{"result": 500, "message": "Supply the youtube stream ID as an integer number for example 91"}'

@app.get("/v1/listen/bbcradio/{c}", status_code=200)
async def listen_bbcradio(c = "m001p1n9"):
	thread_bbc = Thread(target=lambda: oe.bbcradio(str(c), "3345", "rdo"))
	thread_bbc.start()
	time.sleep(15)
	url_rdio = "http://" + str(sip) + ":3345/bbcradio-" + str(c)
	url_rm3u = "http://" + str(sip) + ":3345/bbcradio-" + str(c) + ".m3u"

	response = RedirectResponse(url=str(url_rdio))
	return response


@app.get("/v1/listen/tv/{c}", status_code=200)
async def listen_hdhomerun(c):
	url_iptv = "http://192.168.2.221:5004/auto/v"
	url_rdio = "http://"+ str(sip) +":3345/hdhomerun"
	url_rm3u = "http://"+ str(sip) +":3345/hdhomerun.m3u"
	if c:
		chid = c
	else:
		chid = 2.1

	os.system(f"ffmpeg -re -i {url_iptv}{chid} -vn -codec:a libmp3lame -b:a 192k -f mp3 -content_type audio/mpeg icecast://source:rdo@{sip}:3345/hdhomerun &")
	time.sleep(10)
	#playlist = requests.get(url_rm3u)
	#response = PlainTextResponse(content=str(playlist), status_code=200)

	#response = RedirectResponse(url=str(url_rdio))
	response = RedirectResponse(url=str(url_rm3u))
	return response


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
