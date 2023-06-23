#!/usr/bin/python3
import sys, time
import oceaneyes as oe

from fastapi import FastAPI
app = FastAPI()


global ip, url
settings, stations = oe.init("192.168.2.20")
ip = settings["ipaddress"]
url = "http://" + str(ip)

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

@app.get("/v1/favourites/vacant", status_code=200)
async def fav_remaining():
	return '{"value": "' + str(oe.get_remaining("fav")) + '"}'

@app.get("/v1/favourites/engaged", status_code=200)
async def fav_total():
	return '{"value": "' + str(oe.get_total("fav")) + '"}'

@app.get("/v1/favourites/play/{c}", status_code=200)
async def fav_play(c):
	if c.isnumeric():
		code, message = oe.play(str(c))
		if code == 200:
			return '{"result": ' + str(code) + ', "message": "' + str(message) + '"}'
		else:
			return '{"result": ' + str(code) + ', "message": "Channel may be out of range"}'

	else:
		return '{"result": 500, "message": "Channel index not a number, try requesting with an integer value"}'


@app.get("/v1/favourites/listen/{c}", status_code=200)
async def fav_listen(c):
	if c.isnumeric():
		code, message = oe.listen(str(c))
		if code == 200:
			return '{"result": ' + str(code) + ', "message": "' + str(message) + '"}'
		else:
			return '{"result": ' + str(code) + ', "message": "Channel may be out of range"}'

	else:
		return '{"result": 500, "message": "Channel index not a number, try requesting with an integer value"}'




@app.get("/v1/favourites/move/{r}", status_code=200)
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
