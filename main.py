#!/usr/bin/python3
import sys, time
import oceaneyes as oe


def main():
	settings, stations = oe.init()
	ip = settings["ipaddress"]
	url= "http://" + str(ip)

	#code = oe.cache("RadioBrowser")
	#print(code)

	if oe.is_online():

		print(oe.status(url))

		fav_remaining  = oe.get_remaining("fav")
		fav_total      = oe.get_total("fav")

		print("Presets: Total=" + str(fav_total) + " Remaining=" + str(fav_remaining))

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
		#code, message = oe.play("1")
		#print(str(code) + ":" + str(message))

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



		# Add a new station not on skytune
		#code, station = oe.add("Vivaldi", "https://stream.0nlineradio.com/vivaldi", "3;17;-1", "2;15", False)
		#if code == 200:
		#	print("Added  : " + station)

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


if __name__ == "__main__":
	main()
