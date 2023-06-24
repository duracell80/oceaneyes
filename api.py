#!/usr/bin/python3
import sys, time
import oceaneyes as oe

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
app = FastAPI()


global ip, url

settings, stations = oe.init()
ip = settings["ipaddress"]
url= "http://" + str(ip)







@app.post("/v1/status/network/{ipaddr}", status_code=200)
async def online(ipaddr):
	global ip
	settings, stations = oe.init(ipaddr)
	ip = settings["ipaddress"]

	if oe.is_online():
		return '{"status": "online"}'
	else:
		return '{"status": "offline"}'

@app.get("/v1/status/network/info", status_code=200)
async def network():
        return '{"ip": ' + str(ip) + '}'


@app.get("/v1/status", status_code=200)
async def status():
	return str(oe.status(url))

@app.get("/v1/volume/up", status_code=200)
async def status():
	return str(oe.volume("up"))

@app.get("/v1/volume/down", status_code=200)
async def status():
	return str(oe.volume("down"))

@app.get("/v1/volume/mute", status_code=200)
async def status():
	return str(oe.volume("mute"))

@app.get("/v1/volume/unmute", status_code=200)
async def status():
	return str(oe.volume("unmute"))

@app.get("/v1/channel/vacant", status_code=200)
async def fav_remaining():
	return '{"value": "' + str(oe.get_remaining("fav")) + '"}'

@app.get("/v1/channel/engaged", status_code=200)
async def fav_total():
	return '{"value": "' + str(oe.get_total("fav")) + '"}'

@app.get("/v1/channel/save", status_code=200)
async def fav_save():
	code, station = oe.add_current()
	if code == 200:
		return '{"result": 200", "message": "' + str(station)  + ' added to favourites"}'
	else:
		return '{"result": 400, "message": "Currently playing station not saved to favourites"}'

@app.get("/v1/channel/backup", status_code=200)
async def fav_save():
	oe.get_list("plain", False)
	return '{"result": 200, "message": "Exported from IPRadio to local database stations.db"}'

@app.get("/v1/channel/play/{c}", status_code=200)
async def fav_play(c):
	if c.isnumeric():
		code, message = oe.play(str(c))
		if code == 200:
			return '{"result": ' + str(code) + ', "message": "' + str(message) + '"}'
		else:
			return '{"result": ' + str(code) + ', "message": "Channel may be out of range"}'

	else:
		return '{"result": 500, "message": "Channel index not a number, try requesting with an integer value"}'


@app.get("/v1/channel/listen/vlc/{chid}", status_code=200)
async def fav_listen(chid):
	if c.isnumeric():
		code, message = oe.listen(str(chid))
		if code == 200:
			return '{"result": ' + str(code) + ', "message": "' + str(message) + '"}'
		else:
			return '{"result": ' + str(code) + ', "message": "Channel may be out of range"}'

	else:
		return '{"result": 500, "message": "Channel index not a number, try requesting with an integer value"}'


@app.get("/v1/channel/listen/browser/{ichid}", status_code=200)
async def fav_listen(ichid):
	if ichid.isnumeric():
		chid 		= None
		chname 		= "not set"
		churl		= "not set"
		country_str	= "not set"
		genre_str	= "not set"
		chid, chname, churl, country_str, genre_str = oe.info_get(str(int(ichid)))
		if str(ichid).isnumeric():
			response = RedirectResponse(url=str(churl))
			return response
		else:
			return '{"result": 400, "message": "Channel may be out of range"}'

	else:
		return '{"result": 500, "message": "Channel index not a number, try requesting with an integer value"}'


@app.get("/v1/channel/move/{r}", status_code=200)
async def fav_move(r):
	if ":" in r:
		r_bits = r.split(":")
		code, message = oe.move(str(r_bits[0]), str(r_bits[1]))
		return '{"result": ' + str(code) + ', "message": ' + str(message) + '}'
	else:
		return '{"result": ' + str(code) + ', "message": ""}'
















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
