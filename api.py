#!/usr/bin/python3
import sys, time
import oceaneyes as oe

from fastapi import FastAPI
app = FastAPI()


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


@app.get("/v1/search/radiobrowser/{keywords}", status_code=200)
async def search(keywords):
	code, result = oe.search(str(keywords), "RadioBrowser", False)
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
