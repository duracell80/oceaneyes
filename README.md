# OceanEyes Radio API
Python API for Ocean Digital Internet Radios
https://www.oceandigitalshop.com/internet-radio

Future proof your investment with hardware that contains station management onboard. Ocean Digital's products provide a better way to ensure our hardware keeps on working even if they discontinue their skytune service. Tested on the Ocean Digital WR-26F, and likely compatible with other radios that contain a similar server to manage favourites.

It's just you, me and an MP3 player. OceanEyes hopes to provide easier and consistent programming access to the onboard preset server.

### Usage:
To import as a module.

Be on the same network as your radio device, in the init declare your radio's location on your WiFi network:

```
#!/usr/bin/python3
import oceaneyes as oe

def main():
	settings, stations = oe.init("192.168.1.200")
	ip = settings["ipaddress"]
	
	print(oe.status())


if __name__ == "__main__":
	main()
```
### Example of bulk import from *.pls
```
oe.add_import("./import.pls", False)

[i] Importing station presets from ./import.pls
[+] 1 of 3 ...
[+] 2 of 3 ...
[+] 3 of 3 ...

200,OpenFM - EDM Anthems,http://stream.open.fm/361
200,OpenFM - Trance,http://stream.open.fm/7
200,OpenFM - House,http://stream.open.fm/5
```

### Run in terminal

```
$ chmod +x *.sh
$ chmod +x *.py
$ ./install.sh
$ ./main.py
```

### REST API (Work currently in progress)
Running api.sh in the root directory of the repo will run a FastAPI server that uses the oe module to interact with the device via OceanEyes. 

- Run ./api.sh
- Open a web browser
- Type http://127.0.0.1:1929/docs for all the methods so far.

```
# Search for a station in the Community Radio Browser
http://127.0.0.1:1929/v1/search/radiobrowser/bbc radio 4
```




### Python API methods (documentation update coming soon, still adding features):
```
import sys, time
import oceaneyes as oe

# Declare global data
settings, stations = oe.init("192.168.2.20")
ip = settings["ipaddress"]



# Find out if the radio is online
if oe.is_online():
	print("Radio is online")

# Show name of currently playing channel
print(oe.status()) - Returns the currently playing station name.

# Change volume of your radio
oe.volume("up|down|mute|unmute")

# Get stats on favourite storage
fav_remaining  = oe.get_remaining("fav")
fav_total      = oe.get_total("fav")
print("Presets: Total=" + str(fav_total) + " Remaining=" + str(fav_remaining))


# Play a channel on your radio
oe.play("1")

# Play a channel on your computer instead (install vlc)
oe.listen("1")

# Delete a channel
oe.delete("1")

# Edit a channel
oe.edit("1", "Vivaldi", "https://stream.0nlineradio.com/vivaldi", "3;17;-1", "2;15", "0")

# Move a channel from one favourite placement to another
print(oe.move("2", "1"))


# Decode country and genre codes
print(oe.decode_country("3", "17", "-1"))
print(oe.decode_genre("-1", "1", "6"))

# Encode plain text to a country or genre code
print(encode_country("United Kingdom"))
print(encode_genre("Pop"))

# Get info on a channel
print(oe.info_get("1"))



# Exact match search of Community Radio Browser by station name
code, result = oe.search("BBC Radio 4", "RadioBrowser", True)
if code == 200:
       i = 0

       while i < len(result):
       print(result[i]["chname"] + ","  + result[i]["churl"])
           i+=1

# Use Community Radio Browser to replace a masked URL from skytune
print(oe.enrich_url("BBC Radio 4"))



# Export favourties in these formats 
# (json-rpp exports to Linux Mint's Radio++ Applet directly)
print(oe.get_list("plain", False))
print(oe.get_list("json", True))
print(oe.get_list("json-rpp", True))
print(oe.get_list("csv", False))
print(oe.get_list("ssv", False))
print(oe.get_list("m3u", True))
print(oe.get_list("pls", False))

```

-- You would not believe your eyes if ten million fireflies lit up the world as I fell asleep - Adam Young

### Useful Resources
- https://heyrick.eu/blog/index.php?diary=20230110
- https://github.com/pfbrowning/od-radio-sync
- https://www.radio-browser.info
- https://www.skytune.net

### Ideas and features
- Cache Community Radio Browser locally and direct REST API to look up that instead
- Evolve the onboard web server to allow more playback controls and device configuration
- Automate station selection on a schedule
- Automate emergency alerts by changing the station to an emergency broadcast and back again
- Automate the import of favourites from a local database or online community radio browser
- Export presets in as many formats as possible
- Syncronize station presets across other software
- Display now playing data in a Home Automation Dashboard
- Analyse listening habits and own this data yourself
- Control volume upon system events such as phone or video calls or when playing videos

-- I've never fallen from quite this high, 
Fallin' into your ocean eyes, 
Those ocean eyes - Billie Eilish

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
- Ocean's (WR-50CD, WR-26F, WR-336F, WR-336N, WR-210N, WR-880N, WR-23D, WR-230SF)
- Denver Electronics IR-140
- Denver Electronics IR-135B
- Release WiFi Internet Radios
- Renkforce RF-IR-MONOV2
- Opticum Ton4 DAB+, Internet, FM Radio
- CC WiFi 3 Internet Radio (with Skytune)

To protect your investment and lengthen the life of your device ask community members or reviewers if the device lets you add your own station URL's directly. Avoid known Reciva radios, like older CC Crane's, Grace Digital's, and Sirius radios that have a vested interest in broadcast technologies like satelite radio. Frontier service based devices are also risky unless adding station URl's directly is allowed via upgrade. 

Avoid Pure and Pure Evoke's and Inscabin's, Lemega's, NakiRadio, Sungale's, most Sangean's, AUNA's.

Non-Skytune Radios that have long life potenital: Tivoli, Logitech, Brennan, Raspbery Pi / DIY devices and Single Board based retro handhelds, as well as set-top boxes or streaming devices like Roku, Amazon Fire, Apple TV or iOS devices, Now TV, Android or Android TV devices, Chromecast and AirPlay devices.
