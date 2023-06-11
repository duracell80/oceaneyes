#!/usr/bin/python3
import sys, time
import oceaneyes as oe

def main():
	settings, stations = oe.init("192.168.2.20")
	ip = settings["ipaddress"]

	#oe.volume("down")
	#oe.volume("up")
	#oe.volume("mute")
	#oe.volume("unmute")

	#oe.play(<fav id (int)>)
	#oe.play(1)

	print(oe.status())

	#oe.decode_country("0,3,17,-1")

	# Add stations from a text file
	#oe.add_import("./import.pls")

	# Add a new station not on skytune
	#code, station = oe.add("Vivaldi", "https://stream.0nlineradio.com/vivaldi", "1,1,43", "2,18", False)
	#if code == 200:
		#print("Added  : " + station)

	# Add current to favourites
	#code, station = oe.add_current()
	#if code == 200:
	#	print("Added  : " + station)

	# Del current from favourites
	#code, station = oe.del_current()
	#if code == 200:
	#	print("Deleted: " + station)

	#print(oe.list("pls"))


if __name__ == "__main__":
	main()
