# OceanEyes Radio API
Python API for Ocean Digital Internet Radios
https://www.oceandigitalshop.com/internet-radio

Sick and tired of Internet Radio portals shutting down? Help send a message to the industry that the potential of service shutdowns is leading to the dimise of a whole product category and it need not be this way. Own your URL's!

Future proof your investment with hardware that contains station management onboard. Ocean Digital's products provide a better way to ensure our hardware keeps on working even if they discontinue their skytune service. Tested on the Ocean Digital WR-26F, and likely compatible with other radios that contain a similar server to manage favourites.

### Usage:
To import as a module:

```
#!/usr/bin/python3
import oceaneyes as oe

def main():
	settings, stations = oe.init("192.168.1.200")
	ip = settings["ipaddress"]

	#oe.volume("down")
	#oe.volume("up")
	#oe.volume("mute")
	#oe.volume("unmute")

	#oe.play(<fav id (int)>)
	#oe.play(1)

	print(oe.status())


if __name__ == "__main__":
	main()
```
### Run in terminal

```
$ chmod +x *.py
$ ./main.py
```

## API Methods:
```
oe.play(<favourite index id>)

oe.status() - Returns the currently playing station name.
oe.volume("up|down|mute|unmute")
```

-- You would not believe your eyes if ten million fireflies lit up the world as I fell asleep
