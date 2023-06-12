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

	#print(oe.move("2", "1"))

	#oe.decode_country("0,3,17,-1")
	#print(oe.decode_genre("1", "6"))

	#oe.delete("47")

	# Add stations from a text file
	#added = oe.add_import("./import.pls", False)
	#print("\n" + added)

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

	#print(oe.list("pls"))


if __name__ == "__main__":
	main()
