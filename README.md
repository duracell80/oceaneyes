# OceanEyes Radio API
Python API for Ocean Digital Internet Radios
https://www.oceandigitalshop.com/internet-radio

Open Source our radio preset systems! Sick and tired of Internet Radio portals shutting down? Help send a message to the industry that the potential of service shutdowns is leading to the dimise of a whole product category and it need not be this way. Internet Radio as a standalone category of hardware can continue to grow if we invest in the right ways to allow people to manage their own databases.

### Own your URL's!

Future proof your investment with hardware that contains station management onboard. Ocean Digital's products provide a better way to ensure our hardware keeps on working even if they discontinue their skytune service. Tested on the Ocean Digital WR-26F, and likely compatible with other radios that contain a similar server to manage favourites.

### Ways we can solve this problem
- As buyers, make preset and station data a high priority in product research
- As buyers, ask for technical teardowns by community members to ensure a device can boot / function beyond a service shutdown
- As reviewers, communicate to buyers the features of a device that would allow the device to operate if the provider withdrew
- As providers, free the station database or category browser from an online only service, consider offline data storage
- As providers, cache the entire database onboard in a format like sqlite3, schedule updates to the URL's directly to the device
- As providers, allow end users to update this cache of data in the event you as a provider become unable / unwilling to
- As providers, standardize an import and export file format that allows portablity of preset data from one device to the next
- As providers, protect buyers of your products by allowing open access to a sandboxed portion of the device that the user can own

It's just you, me and an MP3 player. OceanEyes hopes to provide easier and consistent programming access to the onboard preset server.

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
