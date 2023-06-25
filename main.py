#!/usr/bin/python3
import sys, time
import oceaneyes as oe


def main():
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

	if oe.is_online():

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

	#else:
		#print("Radio offline")
		# Get favourite info by channel id when radio is offline
        	#chid, chname, churl, chcountry, chgenre = oe.info_cached("1")


if __name__ == "__main__":
	main()
