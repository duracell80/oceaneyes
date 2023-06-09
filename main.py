#!/usr/bin/python3
import sys, os, logging, time
import oceaneyes as oe



def import_safe(m, v = "0.0.0"):
	if m.isnumeric():
		logging.error("Module parameters incorrect")
		sys.exit()
	try:
		__import__(m)
		result = True
	except ModuleNotFoundError:
		logging.error(f"Module not found: {m} ({v})")
		os.system(f"pip install {m}=={v}")
		result = True
	except:
		os.system(f"pip install {m}=={v}")
		result = True


	if result:
		return True
	else:
		sys.exit()

if import_safe("asyncio", "3.4.3"):
	logging.info("[i] Importing asyncronization module")
	import asyncio









def init():
	logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

	# Get the settings from tinydb to know the ip address and language of device
	global settings, url, ip

	settings, url, ip = oe.init()
	# Backup favourites from primary radio
	#oe.backup(False)

	# Switch to another radio other than the primary one
	#settings, url, ip = oe.switch(2)

	ip = settings["ipaddress"]
	url= "http://" + str(ip)
	if str(ip) == "0.0.0.0":
		oe.scan()
	# Keep these the lines above the online check


def background(f):
	def wrapped(*args, **kwargs):
		return asyncio.new_event_loop().run_in_executor(None, f, *args, **kwargs)

	return wrapped


@background
def api():
	if import_safe("fastapi", "0.97.0"):
		logging.info("[i] FastAPI available")
	if import_safe("uvicorn", "0.22.0"):
		logging.info("[i] Starting FastAPI as background task")
		os.system("uvicorn api:app --host 127.0.0.1 --port 1929")




def main():

	if oe.is_online(ip):

		code, status, playing = oe.status()
		if code == 200:
			print("[i] Radio @" + str(ip) + " status: " + str(status) + " (" + str(playing)  + ")")
		elif code == 400:
			print("[i] Radio @" + str(ip) + " status: " + str(status) + " (" + str(playing)  + ")")
		else:
			print("[i] Radio @" + str(ip) + " status: Offline")

		fav_remaining  = oe.get_remaining("fav")
		fav_total      = oe.get_total("fav")

		print("Presets: Total=" + str(fav_total) + " Remaining=" + str(fav_remaining))

		# Back up favourites to tinydb file (stations.db), set True to atempt to unmask Skytune managed URL's
		#oe.backup(False)

		# Restore favourites from server to currently selected radio
		#oe.restore(False)

		# Exact match search of Community Radio Browser by station name
		#code, result = oe.search("BBC Radio 4", "RadioBrowser", True)
		#if code == 200:
		#	i = 0

		#	while i < len(result):
		#		print(result[i]["chname"] + ","  + result[i]["churl"])
		#		i+=1

		# Use Community Radio Browser to replace a masked URL from skytune
		#print(oe.enrich_url("BBC Radio 4"))

		# Search TuneIn
		#code, result = oe.search("Dash Radio", "TuneIn", False)
        	#print(result)

		#oe.volume("down")
		#oe.volume("up")
		#oe.volume("mute")
		#oe.volume("unmute")

		# Play a station on the remote device
		#code, message, playing = oe.play("1")
		#print(str(code) + ":" + str(message) + ":" + str(playing))

		# Listen to station on local device
		#code, message = oe.listen("45")
		#print(str(code) + ":" + str(message))

		#oe.delete("54")
		#oe.edit("53", "Vivaldi", "https://stream.0nlineradio.com/vivaldi", "3;17;-1", "2;15", "0")


		# Export favourites and attempt to unmask / replace URL's hidden by skytune
		#print(oe.get_list("plain", False))
		#print(oe.get_list("json", True))
		#print(oe.get_list("json-rpp", True))
		#print(oe.get_list("csv", False))
		#print(oe.get_list("ssv", False))
		#print(oe.get_list("m3u", True))
		#print(oe.get_list("pls", False))


		# Move a favourite from one index to another
		#code, message = oe.move("2", "1")
		#print(message)

		#print(oe.decode_country("3", "17", "-1"))
		#print(oe.decode_genre("-1", "1", "6"))


		#Get info from a favourite
		#chid, chname, churl, chcountry, chgenre = oe.info_get("1")
		#print(chid + "," + chname + "," + churl + "," + chcountry + "," + chgenre)



		# Add stations from a pls file
		# Filepath+name, Encode Title <True|False>, Preview with VLC <True|False>
		#added = oe.add_import("./import.pls", False, True)

		# Add stations from a json file
		# Filepath+name, Encode Title <True|False>, Preview with VLC <True|False>
		#added = oe.add_import("./import.json", False, True)



		# Add a new station not on skytune, set True to see if URL is playable before adding it
		#code, station = oe.add("Vivaldi", "https://stream.0nlineradio.com/vivaldi", "3;17;-1", "2;15", False)
		#code, station = oe.add("Jazz FM", "http://edge-bauerall-01-gos2.sharp-stream.com/jazz.mp3", "3;17;-1", "2;21", True)
		#if code == 200:
		#	print("Added  : " + station)
		#else:
		#	print("Failed to add: " + station)

		# Add current to favourites
		#code, station = oe.add_current()
		#if code == 200:
		#	print("Added  : " + station)

		# Del current from favourites
		#code, station = oe.del_current()
		#if code == 200:
		#	print("Deleted: " + station)

		# This may take around 20 minutes due to remote bandwidth constraints, it's a free service and we can wait
		#oe.cache("RadioBrowser")

	else:
		print("Radio offline")
		# Get favourite info by channel id when radio is offline
        	#chid, chname, churl, chcountry, chgenre = oe.info_cached("1")


if __name__ == "__main__":
	init()
	api()
	main()
