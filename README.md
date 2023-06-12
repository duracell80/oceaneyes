# OceanEyes Radio API
Python API for Ocean Digital Internet Radios
https://www.oceandigitalshop.com/internet-radio

Future proof your investment with hardware that contains station management onboard. Ocean Digital's products provide a better way to ensure our hardware keeps on working even if they discontinue their skytune service. Tested on the Ocean Digital WR-26F, and likely compatible with other radios that contain a similar server to manage favourites.

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

### API methods:
```
oe.play(<favourite index id>)

oe.status() - Returns the currently playing station name.
oe.volume("up|down|mute|unmute")

# Decode a country or genre code
oe.decode_country("0,3,17,-1")

# Delete a preset by index
oe.delete("47")

# Add a new station not on skytune
code, station = oe.add("Vivaldi", "https://stream.0nlineradio.com/vivaldi", "3;17;-1", "2;15", False)
if code == 200:
    print("Added  : " + station)

# Add stations from a text file
added = oe.add_import("./import.pls", False)
print("\n" + added)

# Add current playing to favourites
code, station = oe.add_current()
if code == 200:
    print("Added  : " + station)
```

-- You would not believe your eyes if ten million fireflies lit up the world as I fell asleep

### Useful Resources
- https://github.com/pfbrowning/od-radio-sync
- https://www.radio-browser.info
- https://www.skytune.net

### Ideas and features
- Evolve the onboard web server to allow more playback controls and device configuration
- Automate station selection on a schedule
- Automate emergency alerts by changing the station to an emergency broadcast and back again
- Automate the import of favourites from a local database or online community radio browser
- Export presets in as many formats as possible
- Syncronize station presets across other software
- Display now playing data in a Home Automation Dashboard
- Analyse listening habits and own this data yourself
- Control volume upon system events such as phone or video calls or when playing videos

### Own your URL's!
Open Source our radio preset systems! Sick and tired of Internet Radio portals shutting down? Help send a message to the industry that the potential of service shutdowns is leading to the dimise of a whole product category and it need not be this way. Internet Radio as a standalone category of hardware can continue to grow if we invest in the right ways to allow people to manage their own databases.

### Ways we can solve this problem
- As buyers, make preset data a high priority in product research
- As buyers, ask for technical teardowns by community members
- As reviewers, review the features of a device that would allow the device to operate without service
- As reviewers, update reviews if a device has been broken by a brand and offer their remediation path
- As providers, free the station database or category browser from an online only service
- As providers, cache the entire database in a format like sqlite3, schedule updates directly to the device
- As providers, allow end users to update this cache of data also
- As providers, standardize an import and export file format that allows portablity of preset data
- As providers, protect buyers of your products with a sandboxed portion of the device that the user can own, even a simple samba share and M3U file could save the device from landfill!
- As providers, offer more than one way for the device to browse a list of stations
- As buyers, reviewers and providers; maintain a healthy ecosystem by investing in open software and right to repair


### What is Right to Repair?
https://www.eff.org/issues/right-to-repair

https://www.repair.org/stand-up

https://www.zdnet.com/home-and-office/sustainability/right-to-repair-what-it-means-and-why-it-matters-to-you/

https://hackaday.io/project/183339-saving-a-reciva-box-from-the-landfill

### Radios that may use Skytune:
- Most Ocean Digital's
- Denver Electronics IR-140 Internet Radio
- Release WiFi Internet Radios
- Renkforce RF-IR-MONOV2
- CC WiFi 3 Internet Radio (with Skytune)

To protect your investment and lengthen the life of your device, avoid known Reciva radios, like older CC Crane's, Grace Digital's Sangean's, and Sirius radios that have a vested interest in broadcast technologies like satelite radio. Avoid Pure and Pure Evoke's and Inscabin's, Lemega's, NakiRadio, Sungale's, most Sangean's, AUNA's.

Non-Skytune Radios that have long life potenital: Tivoli, Logitech, Brennan, Raspbery Pi, as well as settop boxes or streaming devices like Roku, Amazon Fire, Apple TV, Now TV, Android or Android TV devices, Chromecast and AirPlay devices.
