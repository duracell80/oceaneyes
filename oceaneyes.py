#!../bin/python3
import sys, os, subprocess, time, logging, socket, requests, urllib, urllib.parse, json
from threading import Thread

#try:
#	from tinydb import TinyDB, Query
#except ModuleNotFoundError:
#	os.system('pip install tinydb')
from tinydb import TinyDB, Query

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


global headers, url_placeholder, name_placeholder, country_placeholder, genre_placeholder
url_placeholder 	= "https://streaming.radio.co/s5c5da6a36/listen"
name_placeholder	= "Bird Song radio"
country_placeholder	= "United Kingdom"
genre_placeholder	= "Nature Sounds & Spa Music"

headers = {
	"User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"Accept-Encoding": "gzip,deflate",
	"Upgrade-Insecure-Requests": "1",
	"Connection": "keep-alive"
}


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
	import asyncio


def background(f):
	def wrapped(*args, **kwargs):
		return asyncio.new_event_loop().run_in_executor(None, f, *args, **kwargs)
	return wrapped

def main():
	return


def switch(device = 1):
	global url, ip, settings

	try:
		dbc	= TinyDB("settings.db")
		dip	= dict((dbc.get(doc_id=int(device))))

		ip	= str(dip["ipaddress"])
		url	= str("http://" + ip)
		dbc.close()

		settings = {
                	"ipaddress" : ip,
                	"url"       : url,
                	"language"  : "English"
		}

		return settings, url, ip
	except:
		settings = {
			"ipaddress" : "0.0.0.0",
			"url"       : "http://0.0.0.0",
			"language"  : "English"
		}
		return settings, settings["url"], settings["ip"]

def get_serverip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(0)
	try:
		s.connect(('1.1.1.1', 1))
		sip = s.getsockname()[0]
	except Exception:
		sip = '127.0.0.1'
	finally:
		s.close()
	return sip




def init_yt():
	# Store previously played YouTube Radio stations
	if os.path.isfile("stations_yt.db"):
		dby     = TinyDB("stations_yt.db")

		if os.path.getsize('stations_yt.db') == 0:
			for i in range(0,100):
				dby.insert({'vid': '00000000000', 'aid': '00', 'sid': 'YouTube Stream Name'})

	else:
		dby     = TinyDB("stations_yt.db")
		# Create 99 radio stations in YouTube storage with id 100 = last played
		for i in range(0,100):
			dby.insert({'vid': '00000000000', 'aid': '00', 'sid': 'YouTube Stream Name'})


def init(device = 1):
	global url, ip, sip, settings, pid_fm, pid_hd
	sip = get_serverip()

	# Attempt to find or set an ipaddress
	if os.path.isfile("settings.db"):
		dbc     = TinyDB("settings.db")

		if os.path.getsize('settings.db') == 0:
			for i in range(0,10):
				dbc.insert({'ipaddress': '0.0.0.0', 'language': 'English'})
			hosts, devices = scan()
			code = oe.cache("RadioBrowser")

		else:
			conf    = dict((dbc.get(doc_id=int(device))))
		conf    = dict((dbc.get(doc_id=int(device))))
	else:
		dbc     = TinyDB("settings.db")
		# Create 20 radio devices in setting storage
		for i in range(0,20):
			dbc.insert({'ipaddress': '0.0.0.0', 'language': 'English'})

	# Fallback on init to detect radio devices on network
	try:
		ip = str(conf['ipaddress'])
	except:
		init()

	# Setup YouTube Radio storage
	init_yt()

	settings, url, ip  = switch(int(device))
	settings = {
		"ipaddress" : ip,
		"url"       : url,
		"language"  : "English"
	}

	stations = {
		"100":  {
			"name"    : "BBC World Service",
			"url"     : "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
			"country" : "United Kingdom",
			"genre"   : "Public Radio"
		}
	}

	dbc.close()

	return settings, url, ip

def scan():
	if os.path.isfile("settings.db"):
		dbc     = TinyDB("settings.db")
	else:
		dbc     = TinyDB("settings.db")
		dbc.insert({'ipaddress': '0.0.0.0', 'language': 'English'})



	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("1.1.1.1", 80))
	h = s.getsockname()[0].split(".")
	h = str(h[0] + "." + h[1] + "." + h[2])
	s.close()

	hosts   = []
	devices = []
	d	= 0
	logging.info("[i] Auto detecting Skytune radios on the LAN, this may take some time ...")
	print("[i] Auto detecting Skytune radios on the LAN ... \n\nPress Ctrl + Z when all known devices are found")
	print("Press Ctrl + C if scanning seems to be stuck\n\n")
	print("--- Tip: Take note of these numbers and then set")
	print("--- static routes on the router for these devices\n\n")
	for i in range(1,255):
		host    = h + "." + str(i)
		try:
			try:
				r = requests.get("http://" + str(host) + ":80", timeout=1)
				if r.status_code == 200:
					p = 80
			except:
				p = 0
				logging.info(f"[i] Looking for a radio at this address ({str(h)}.{str(i)})")
			if p == 80:
				logging.info(f"[i] Looking for a radio at this address ({str(h)}.{str(i)}) [P:80]")


				# test that the radio can be pinged
				result  = str(os.popen("ping " + str(host) + " -w 5 -W 5").read())
			else:
				p = 0
				result = "0 received"
		except:
			p = 0
			result  = "0 received"
			#print("[i] Looking for a radio at this address (" + str(h) + "." + str(i) + ")")

		if "5 received" in result:
			try:
				r = requests.get("http://" + str(host) + "/php/favList.php?PG=0")
				if r.status_code == 200:
					d+=1
					devices.append(host)
					dbc.update({'ipaddress': str(host)}, doc_ids=[int(d)])
					logging.info(f"\n[+] Found a radio @{str(host)}:80\n")
			except:
				x=1

			hosts.append(host)

	radios = len(devices)
	if radios > 0:
		if radios > 1:
			logging.info(f"\n[i] Found {str(radios)} Skytune radios on the network")
		else:
			logging.info(f"\n[i] Found {str(radios)} Skytune radio on the network")
		for i in range(0,int(radios)):
			logging.info(f"--- Radio {str(i+1)} @ {str(devices[i])}")

	return hosts, devices


def convert_l2d(lst):
	# Converts a list to a dictionary
	res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}

	return res_dct

def isfloat(sin):
	if sin.replace(".", "").isnumeric():
		return True
	else:
		return False


def is_online(ip = "0.0.0.0"):
	args = socket.getaddrinfo(ip, 80, socket.AF_INET, socket.SOCK_STREAM)
	for family, socktype, proto, canonname, sockaddr in args:
		s = socket.socket(family, socktype, proto)
		try:
			s.connect(sockaddr)
		except socket.error:
			return False
		else:
			s.close()
			r = requests.get(url + "/php/favList.php?PG=0", headers=headers)
			if r.status_code == 404:
				return False
			else:
				return True

def is_streamable(churl = url_placeholder, chpreview = False):
	if "fm://" in churl or "dab://" in churl:
		return True
	else:
		try:
			import vlc

			vlc_ins = vlc.Instance('--input-repeat=-1', '-q')
			vlc_pla = vlc_ins.media_player_new()
			vlc_med = vlc_ins.media_new(str(churl))

			vlc_pla.set_media(vlc_med); vlc_pla.play()
			if chpreview == False:
				vlc_pla.audio_set_mute(True); time.sleep(5)
			time.sleep(10)

			did_play = str(vlc_pla.is_playing()); time.sleep(1); vlc_pla.stop()


			result = False
			if str(vlc_pla.get_state()) == "State.Stopped":
				if did_play == "1":
					result = True
				else:
					vlc_pla.stop()

		except ModuleNotFoundError:
			return True

	return result


def listen(chid = "1", chduration = 21600):
	if int(chid) > 99 or chduration > 21600:
		code = 500
		message = "Duration or channel preset out of range, must be below 100 and less than 1 hour playback"
	else:
		try:
			import vlc
			if is_online():
				chid, chname, churl, country_str, genre_str = info_get(str(int(chid)))
			else:
				chid, chname, churl, country_str, genre_str = info_cached(str(int(chid)))

			print("[i] Playing " + str(chname) + " locally ...")

			vlc_ins = vlc.Instance('--input-repeat=-1', '-q')
			vlc_pla = vlc_ins.media_player_new()
			vlc_med = vlc_ins.media_new(str(churl))

			vlc_pla.set_media(vlc_med); vlc_pla.play()
			vlc_pla.audio_set_mute(False);
			time.sleep(chduration)

			did_play = str(vlc_pla.is_playing()); time.sleep(1); vlc_pla.stop()


			code = 400
			message = ""
			if str(vlc_pla.get_state()) == "State.Stopped":
				if did_play == "1":
					code = 200
					message = "Now listening to " + str(chname) + " on local device"
				else:
					vlc_pla.stop()

		except ModuleNotFoundError:
			os.system('pip install python-vlc')
			code = 500
			message = "Module python-vlc was installed with pip, pleaase try the request again"
			return code, message

	return code, message

def search(keyword = "BBC Radio 1",  source = "radiobrowser", match_exact = True):
	station_data    = []
	station_name    = "not set"
	station_url     = "not set"
	station_codec   = "not set"
	station_bitrate = "not set"
	station_genre   = "not set"
	station_country = "not set"
	station_language= "not set"

	l = []
	code = 0

	# SEARCH RadioBrowser
	if str(source.lower()) == "radiobrowser":
		try:
			from pyradios import RadioBrowser
			source = RadioBrowser()
			result = source.search(name=str(keyword), name_exact=match_exact)

			i = 0; l = []

			for item in result:
				for key, value in item.items():

					if str(key).lower() == "hls":
						station_hls = str(value)
					if str(key).lower() == "codec":
						station_codec = str(value)
					if str(key).lower() == "bitrate":
						station_bitrate = str(value)
					if str(key).lower() == "name":
						station_name = str(value)
					if str(key).lower() == "url":
						station_url  = str(value)
					if str(key).lower() == "countrycode":
						station_country = str(value)
						if str(key).lower() == "state":
	                                               	station_country = station_country + ";" + str(value)
					if str(key).lower() == "language":
						station_language = str(value)

					if str(key).lower() == "tags":
                                                station_genre = str(value)



				station_data = {'chindex': int(i), 'chname': str(station_name), 'churl': str(station_url), 'chcodec': str(station_codec), 'chbitrate': str(station_bitrate), 'chhls': int(str(station_hls)), 'chgenre': str(station_genre), 'chcountry': str(station_country), 'chlanguage': str(station_language)}
				l.append(station_data)

				i+=1
			if i > 1:
				code = 200
			else:
				code = 404

		except ModuleNotFoundError:
			os.system('pip install pyradios')
			station_data = {'chindex': 0, 'source': 'radiobrowser', 'chname': 'not found', 'churl': 'not found', 'chcodec': 'MP3', 'chbitrate': '320', 'chhls': 0, 'chgenre': 'notfound', 'chcountry': 'not found', 'chlanguage': 'not found'}
			l = []
			l.append(station_data)
			code = 404

			return code, l

	# SEARCH : TuneIn
	elif str(source.lower()) == "tunein":
		try:
			import opml

			data = opml.parse("http://opml.radiotime.com/Search.ashx?event=lit&query=" + str(keyword))
			i = 0
			c = 0

			for d in data:
				try:
					if str(data[i].type).lower() == "audio" and str(data[i].item).lower() == "station" and i <= int(len(data)):
						c+=1
						try:
							station_name    = str(data[i].text)
							station_url     = str(data[i].URL)

							f = urllib.request.urlopen(str(station_url))
							station_url = str(f.read())
							station_url = station_url.replace("b'http", "http").replace("\\n'", "")
							f.close()

						except:
							station_name	= str(url_placeholder)
							station_url	= str(name_placeholder)
						try:
							station_codec   = str(data[i].formats)
							station_bitrate = str(data[i].bitrate)
						except:
							station_code	= "not"
							station_bitrate	= "0"
						try:
							data[i].genre_id
							station_genre   = str(data[i].genre_id)
						except:
							station_genre	= "g0"
						try:
							station_country = str(data[i].guide_id)
						except:
							station_country = str(data[i].guide_id)
						try:
							station_language = str(data[i].subtext)
						except:
							station_language = "s0"


						station_data = {'chindex': int(c), 'chname': str(station_name), 'churl': str(station_url), 'chcodec': str(station_codec), 'chbitrate': str(station_bitrate), 'chhls': 0, 'chgenre': str(station_genre), 'chcountry': str(station_country), 'chlanguage': str(station_language)}
						l.append(station_data)
					i+=1
				except:
					station_data = {'chindex': 0, 'chname': 'not found', 'source': 'none', 'churl': 'not found', 'chcodec': 'MP3', 'chbitrate': '320', 'chhls': 0, 'chgenre': 'notfound', 'chcountry': 'not found', 'chlanguage': 'not found'}


			if len(data) > 2:
				code = 200
			else:
				code = 404

		except ModuleNotFoundError:
			os.system('pip install opml')
			station_data = {'chindex': 0, 'source': 'tunein', 'chname': 'not found', 'churl': 'not found', 'chcodec': 'MP3', 'chbitrate': '320', 'chhls': 0, 'chgenre': 'notfound', 'chcountry': 'not found', 'chlanguage': 'not found'}
			l = []
			l.append(station_data)
			code = 404
	else:
		station_data = {'chindex': 0, 'chname': 'not found', 'source': 'none', 'churl': 'not found', 'chcodec': 'MP3', 'chbitrate': '320', 'chhls': 0, 'chgenre': 'notfound', 'chcountry': 'not found', 'chlanguage': 'not found'}
		l = []
		l.append(station_data)
		code = 404

	return code, l

def cache(source = "RadioBrowser"):
	code = 400
	if str(source).lower() == "radiobrowser":
		dest_file	= "cache_radiobrowser.sql.gz"
		source_url 	= "https://backups.radio-browser.info"
		source_file	= str(source_url) + "/latest.sql.gz"
		r 		= requests.get(source_url)
		code 		= r.status_code

		if int(code) == 200 and os.path.isfile(dest_file) == False:
			print("[i] Downloading entire Radio Browser database, please wait (this may take up 20 minutes) ...")
			d               = requests.get(source_file, allow_redirects=True)
			code            = d.status_code
			open(dest_file, 'wb').write(d.content)
		else:
			print("[i] Radio Browser already cached, delete latest.sql.gz to force a download")
	return code

def enrich_url(chname = "BBC Radio 1"):
	code, result = search(str(chname).lower(), "RadioBrowser", False)
	chplays = False

	if code == 200:
		i = 0

		# Return a list of URL's matching station name, attempt to play with vlc, return the first playable URL
		while i < len(result):
			print("[i] Atempting to enrich URL for " + str(chname))
			if is_streamable(result[i]["churl"], False):
				chplays = True
				churl   = result[i]["churl"]

				print("[i] Found a working URL!")
				break
				# found a playable url, break
			else:
				chplays = False
			i+=1
	if chplays:
		return churl
	else:
		return url_placeholder


def get_total(thing = "fav"):
	t = 0
	if thing == "fav":
		r = requests.get(url + "/php/favList.php?PG=0")
		s = str(r.text).split("\n")
		i = len(s)
		c = s[i-2].split(":")
		f = c[2].split(",")
		t = int(f[0])

	return t

def get_remaining(thing = "fav"):
	t = 0
	if thing == "fav":
		f = int(get_total("fav"))
		t = 99 - f
	return int(t)


def get_status():
	status = "Unknown"
	try:
		r = requests.get("http://" + str(ip) + "/php/playing.php")
		d = json.loads(str(r.text).replace("'", '"'))

		if d["result"] == "success":
			status = "playing"
			playing = str(d["name"])
			code = 200
		else:
			status = "stopped"
			playing = "None"
			code = 400
	except Exception as e:
		status = "unknown"
		playing= "None"
		code = 404

	#logging.info(f"[i] Status of radio@{ip}: {playing} [{code}]")
	return  code, status, playing


def info_get(chid = "1"):
	chid = str(int(chid)-1)

	t = get_total("fav")

	if int(chid) > t:
		chname = str(name_placeholder)
		churl  = str(url_placeholder)
		chcountry = "United Kingdom"
		chgenre = "Nature Sounds & Spa Music"

		return chid, chname, churl, chcountry, chgenre
	else:
		station_ids, station_names, station_urls, station_countries, station_genres = list_get()

		chid      = station_ids[int(chid)]
		chname    = station_names[int(chid)]
		churl     = station_urls[int(chid)]
		chcountry = station_countries[int(chid)]
		chgenre   = station_genres[int(chid)]

		country_bit = chcountry.split(",")
		country_str = decode_country(int(country_bit[0]), int(country_bit[1]), int(country_bit[2]))

		genre_bit = chgenre.split(",")
		genre_str = decode_genre(int(genre_bit[0]), int(genre_bit[1])).replace("and", "&")

		return chid, chname, churl, country_str, genre_str


def info_cached(chid = "1"):
	t = 99

	if int(chid) > t:
		chid		= "100"
		chname		= str(name_placeholder)
		churl		= str(url_placeholder)
		chcountry	= str(country_placeholder)
		chgenre		= str(genre_placeholder)

		return chid, chname, churl, chcountry, chgenre
	else:
		dbs	= TinyDB("stations.db")
		chl	= dict((dbs.get(doc_id=int(chid))))
		dbs.close()

		chid	= str(chl['channel'])
		chname	= str(chl['name'])
		churl	= str(chl['url'])
		chcountry = str(chl['country'])
		chgenre	= str(chl['genre'])

		return chid, chname, churl, chcountry, chgenre



def edit(chid = "0", newchname = name_placeholder, newchurl = url_placeholder, forcechcountry = "3;17;-1", forcechgenre = "1;45", forceskytune = "0"):
	if str(chid).isnumeric():
		t = get_total("fav")

		if int(chid) <= t:
			data 	  = info_get(str(chid))
			chid	  = str(int(chid) - 1)
			chname 	  = data[1]
			churl 	  = data[2]
			chcountry = data[3]
			chgenre   = data[4]

			code, newchgenre	= encode_genre(str(chgenre))
			newchcountry		= str(chcountry).replace(",", ";")
			newchskytune		= "0"
			#newchname		= urllib.parse.quote_plus(str(newchname))


			f = {'chName': str(newchname), 'chUrl': str(newchurl), 'chCountry': str(newchcountry), 'chGenre': str(newchgenre), 'chSkytune': str(newchskytune)}
			r = requests.post(url + "/updateCh.cgi?CI=" + str(int(chid)), data=f)

			code = int(r.status_code)

			return code, str(chid), str(newchname), str(newchurl), str(newchcountry), str(newchgenre), str(newchskytune)
		else:
			code = 500
			skyt = 0
			print("Error: Preset Out Of Range")
			return code, str("Null"), str("Null"), str("Null"), str("Null"), str("Null"), str(skyt)
	else:
		code = 500
		skyt = 0
		print("Error: Preset Out Of Range")

		return code, str("Null"), str("Null"), str("Null"), str("Null"), str("Null"), str(skyt)


def play(ch = "0"):
	t = get_total("fav")
	if int(ch) <= t:
		r = requests.get(url + "/doApi.cgi", params = {"AI":"16", "CI": str(int(ch) - 1)})
		if r.status_code == 200:
			code, status, playing = get_status()
			message = "Changing channel"
			return code, message, playing
		else:
			code = 500
			message = "Failed to change channel"
			playing = "None"
	else:
		code = 404
		message = "Failed to change channel"
		playing = "None"

	return code, message, playing




def add(chname = "Local Streaming", churl = "http://192.168.1.200:1234/stream.mp3", chcountry = "-1", chgenre = "-1", chplay = False):
	t = 0
	c = get_total("fav")

	if c > 99:
		code = 403
		station = "Presets Full"
		return code, station
	else:
		f = {'EX': '0', 'chName': str(chname), 'chUrl': str(churl), 'chCountry': str(chcountry), 'chGenre': str(chgenre)}
		if chplay:
			if is_streamable(churl, False):
				r = requests.post(url + "/addCh.cgi", data=f)
				if r.status_code == 200:
					print("[i] Added station " + str(chname) + " to radio @" + str(ip))
		else:
			r = requests.post(url + "/addCh.cgi", data=f)
			if r.status_code == 200:
				print("[i] Added station " + str(chname) + " to radio @" + str(ip))

		time.sleep(8)
		t = get_total("fav")

		if t > c:
			code = 200
			station = str(chname)
		else:
			code = 500
			station = str(chname)

		return code, station



def add_import(filename = "./import.pls", encode = False, chpreview = False):
	c=0
	s=0
	added = ""

	if ".pls" in filename:
		print("[i] Importing station presets from " + str(filename))
		lines = [i.split("=") for i in open(filename).readlines()]
		t = int(len(lines)-1)

		while c < t:
			if "file" in str(lines[c][0]).lower() and "://" in str(lines[c][1]).lower():
				s+=1
				if encode:
					churl           = str(urllib.parse.quote_plus(str(lines[c][1]).replace("\n", "")))
					chname		= str(urllib.parse.quote_plus(str(lines[c+1][1]).replace("\n", "")))
				else:
					churl           = str(lines[c][1]).replace("\n", "")
					chname          = str(lines[c+1][1]).replace("\n", "")
				chcountry	= "3;17;-1"
				chgenre		= "2;14"
				chplays		= False

				if is_streamable(churl, chpreview):
					chplays		= True
					code, station 	= add(chname, churl, chcountry, chgenre, False)
				else:
					code 		= 404
					station 	= chname
					churl 		= url_placeholder
					chplays		= False


				if code == 200 and chplays:
					added += str(str(code) + "," + str(station) + "," + str(churl) + "\n")
					print("[+] " + str(s) + " of " + str(int((t/3))) + " ... [C-" + str(code) + ":P-" + str(chplays) + ":" + str(chname) + ":" + str(churl) + "]")
				elif code == 404 or chplays == False:
					print("[!] " + str(s) + " of " + str(int((t/3))) + " ... [C-" + str(code) + ":P-" + str(chplays) + ":" + str(chname) + " Cannot be contacted, double check the url or your internet connection]")
				else:
					print("[!] " + str(s) + " of " + str(int((t/3))) + " ... [C-" + str(code) + ":P-" + str(chplays) + ":" + str(chname) + "]")
					added += str(str(code) + "," + str(station) + "," + str(churl) + "\n")
			c+=1
	elif ".json" in filename:
		# Get genres and locations into global scope
		decode_genre(1, 11)
		decode_country(1,1,75)

		print("[i] Importing station presets from " + str(filename))

		with open(filename) as json_file:
			data = json.load(json_file)

		for q in data['stations']:
			t = int(len(data['stations']))
		for i in data['stations']:
			s+=1
			chname		= str(i['name'])
			churl		= str(i['url'])
			chcountry       = str(i['country'])
			chgenre         = str(i['genre'])

			gcode, chgenre   = encode_genre(str(i['genre']))
			ccode, chcountry = encode_country(str(i['country']))

			chplays         = False

			if is_streamable(churl, chpreview):
				chplays         = True
				code, station   = add(chname, churl, chcountry, chgenre, False)
			else:
				code            = 404
				station         = chname
				churl           = url_placeholder
				chplays         = False

			if code == 200 and chplays:
				added += str(str(code) + "," + str(station) + "," + str(churl) + "\n")
				print("[+] " + str(s) + " of " + str(int((t))) + " ... [C-" + str(ccode) + ":G-" + str(gcode) + ":L-" + str(ccode) + ":P-" + str(chplays) + ":" + str(chname) + ":" + str(churl) + "]")
			elif code == 404 or chplays == False:
				print("[!] " + str(s) + " of " + str(int((t))) + " ... [C-" + str(ccode) + ":G-" + str(gcode) + ":L-" + str(ccode) + ":P-" + str(chplays) + ":" + str(chname) + " Cannot be contacted, double check the url or your internet connection]")
			else:
				print("[!] " + str(s) + " of " + str(int((t))) + " ... [C-" + str(ccode) + ":G-" + str(gcode) + ":L-" + str(ccode) + ":P-" + str(chplays) + ":" + str(chname) + "]")
				added += str(str(code) + "," + str(station) + "," + str(churl) + "," + str(chgenre) + "," + str(chcountry) + "\n")

			c+=1
	else:
		added = "None"

	return added



def add_current():
	# Get current number of favs first
	t = 0
	c = get_total("fav")

	code, status, playing = get_status()
	if "stopped" in status.lower():
		station = "None"
	else:
		# Set new fav
		r = requests.get(url + "/doApi.cgi", params = {"AI":"8"})
		t = get_total("fav")

		# Read currently playing
		code, status, playing = get_status()
		station = playing

	if t > c:
		code 	= 200
	else:
		code 	= 500

	return code, station

def del_current():
	# Get current number of favs first
	t = 0
	c = get_total("fav")

	code, status, playing = get_status()
	if "stopped" in status.lower():
		station = "None"
	else:
		# Del currently playing
		r = requests.get(url + "/doApi.cgi", params = {"AI":"4"})
		t = get_total("fav")

		# Read currently playing
		code, status, playing = get_status()
		station = playing

	if t < c:
		code    = 200
	else:
		code    = 500

	return code, station

def move(f = "2", t = "1"):
	#/moveCh.cgi?CI=49&DI=48&EX=0
	# offset by 1 so -1 off values supplied in method
	f = int(int(f)-1)
	t = int(int(t)-1)

	c = get_total("fav")

	if f > 99 or t > 99 or t > c or f > c or f < 0 or t < 0:
		code   = 400
		string = "Cannot move - presets out of range"
		return code, string
	else:
		r = requests.post(url + "/moveCh.cgi?EX=0&CI="+ str(int(f)) +"&DI="+ str(int(t)))

		code   = 200
		string = "Moved preset " + str(int(f)+1) + " to " + str(int(t)+1)
		return code, string


def volume(dir = "down"):
	# volume down 	VL=-1
	# volume up	VL=1
	# mute 		VL=128
	# unmute 	VL=0
	inc = "0"

	if dir.isnumeric() == False:
		if dir == "down":
			inc = "-" + str(inc)
		elif dir == "up":
			inc = str(inc)
		elif dir == "mute":
			inc = "128"
		elif dir == "unmute":
			inc = "0"
		else:
			inc = "-1"

		r = requests.get(url + "/php/doVol.php", params = {"VL":str(inc)})
		d = json.loads(str(r.text).replace("'", '"'))


		data_level = d["level"]
		data_muted = d["muted"]
	else:
		data_level = "0"

	return data_level



def list_get():
	station_countries 	= []
	station_genres		= []
	station_names 		= []
	station_urls  		= []
	station_ids		= []

	r = requests.get(url + "/php/favList.php?PG=0")
	s = str(r.text).split("\n")
	f = str(s[int(len(s)-2)]).split(":")
	n = (str(f[2])).split(",")


	data_size = int(n[0])			# Total of favourites
	data_page = round(data_size/10)		# Pages of favourites
	data_delta= abs(int(data_size) - int(data_page*10))

	if data_delta > 0:
		data_page += 1

	i = 0
	h = 0
	while i < data_page:
		c = 0
		r = requests.get(url + "/php/favList.php?PG=" + str(i))
		s = str(r.text).split("\n")

		while c < int(len(s)):
			if c >= 2 and c < int(len(s)-2):
				if s[c] is not None:
					data_item  = str(s[c]).replace("myFavChannelList.push", "").split('"')
					data_name  = str(html_decode(str(data_item[1])))
					data_cbit  = str(html_decode(str(data_item[4]))).replace("]", "").replace(");", "").split("[")
					data_cont  = str(data_cbit[2][:-1])
					data_genre = str(data_cbit[3])

					data_url  = str(data_item[3]).replace("****** Channel URL is maintained by Skytune", url_placeholder)
					# URL's maintained by Skytune are masked, play birdsong instead

					if i == 0:
						h = str(str(int(c-1)))
					elif i == 1:
						h = str("1" + str(int(c-1)))
					elif i == 2:
						h = str("2" + str(int(c-1)))
					elif i == 3:
						h = str("3" + str(int(c-1)))
					elif i == 4:
						h = str("4" + str(int(c-1)))
					elif i == 5:
						h = str("5" + str(int(c-1)))
					elif i == 6:
						h = str("6" + str(int(c-1)))
					elif i == 7:
						h = str("7" + str(int(c-1)))
					elif i == 8:
						h = str("8" + str(int(c-1)))
					elif i == 9:
						h = str("9" + str(int(c-1)))
					else:
						h = "0"

					if h == "110":
						h = str("20")
					elif h == "210":
						h = str("30")
					elif h == "310":
						h = str("40")
					elif h == "410":
						h = str("50")
					elif h == "510":
						h = str("60")
					elif h == "610":
						h = str("70")
					elif h == "710":
						h = str("80")
					elif h == "810":
						h = str("90")
					elif h == "910":
						h = str("100")

					#print(str(int(h)) + ";" + str(data_name) + ";" + str(data_url) + ";" + str(data_cont) + ";" + str(data_genre))

					station_countries.append(data_cont)
					station_genres.append(data_genre)
					station_names.append(data_name)
					station_urls.append(data_url)
					station_ids.append(str(int(h)-1))
			c+=1
		i+=1

	return station_ids, station_names, station_urls, station_countries, station_genres

def set_list(chid = 0, chname = "not set", churl = "not set", chcountry = "not set", chgenre = "not set"):
	dbs = TinyDB("stations.db")
	dbs.insert({'channel': int(chid), 'name': str(chname), 'url': str(churl), 'country': str(chcountry), 'genre': str(chgenre)})
	dbs.close()
	return None


def get_list(format = "plain", enrich = False):
	dbs     = TinyDB("stations.db")
	dby     = TinyDB("stations_yt.db")
	dbs.truncate()
	dbs.close()

	n       = 0

	list    = ""
	pls_1   = "[playlist]"
	pls_2   = "NumberOfEntries=0"
	pls     = str(pls_1)
	m3u     = "#EXTM3U"
	jsn     = ""
	jsn_1   = '{"stations":['
	jsn_2   = ']}'
	jsn_3   = '"value":['
	jsn_4   = ']'
	csv     = "" # comma
	ssv     = "" # semicolon

	if format == "m3u-yt":
		n=0
		t=0
		for idx, doc in enumerate(dby.all()):
			row = dby.get(doc_id=int(idx+1))
			vid = row['vid']
			if vid != "00000000000":
				t += 1

		for idx, doc in enumerate(dby.all()):
			row = dby.get(doc_id=int(idx+1))

			vid = row['vid']
			aid = row['aid']
			sid = row['sid']

			url_prx = f"http://{sip}:1929/v1/listen/ytradio/{vid}/{aid}/{urllib.parse.quote(sid)}"
			url_icy = f"http://{sip}:3345/ytradio-{vid}"
			url_web = f"https://www.youtube.com/watch?v={vid}"

			if vid != "00000000000":
				n += 1
				m3u += '\n#EXTINF:-1, ' + str(sid) + ' \n'+ str(url_prx)

		list = m3u

		file_out = "export_yt.m3u"
		with open(file_out, "w") as o:
			o.write(list)

		m3u = ""
		return list

	elif format == "json-yt":
		n=0
		t=0
		for idx, doc in enumerate(dby.all()):
			row = dby.get(doc_id=int(idx+1))
			vid = row['vid']
			if vid != "00000000000":
				t += 1

		for idx, doc in enumerate(dby.all()):
			row = dby.get(doc_id=int(idx+1))

			vid = row['vid']
			aid = row['aid']
			sid = row['sid']

			url_prx = f"http://{sip}:1929/v1/listen/ytradio/{vid}/{aid}/{urllib.parse.quote(sid)}"
			url_icy = f"http://{sip}:3345/ytradio-{vid}"
			url_web = f"https://www.youtube.com/watch?v={vid}"

			if vid != "00000000000":
				n += 1
				jsn += '{"channel":"' + str(int(idx)+1) + '","name":"' + str(row['sid']) + '","url_prx":"' + str(url_prx) + '","url_icy":"' + str(url_icy) + '","url_web":"' + str(url_web) + '","vid":"' + str(vid) + '", "aid":"' + str(aid) + '"}'
				if int(int(n)) != int(t):
					jsn += ','


		list = str(jsn_1) + str(jsn) + str(jsn_2)
		file_out = "export_yt.json"
		with open(file_out, "w") as o:
		       o.write(list)

		jsn = ""
		return list


	id, name, url, country, genre = list_get()

	if format == "json-rpp":
		code = os.system("cinnamon --version")
		if code == 32512:
			return jsn_1 + '{"code": 404}' + jsn_2
		else:
			print("[i] Exporting to Radio++ ...")
	elif format == "json-rpp-out":
		print("[i] Exporting to Radio++ ...")

	while n < int(len(name)):
		if name is not None:
			# Keep encoded country and genre entries
			chcountry = country[n]
			chgenre   = genre[n]

			# Decode country and genre codes into words
			genre_bit = genre[n].split(",")
			genre_str = decode_genre(code_1 = int(genre_bit[0]), code_2 = int(genre_bit[1]))
			country_bits  = country[n].split(",")

			# Attempt to export unmasked Skytune stations using Community Radio Browser without querying Skytune
			if str(url[n]).lower() == str(url_placeholder).lower() and enrich:
				name_bits       = str(name[n]).split(" ")
				try:
					if len(name_bits) > 2:
						search	= str(name_bits[0] + " " + name_bits[1] + " " + name_bits[2])
					else:
						search  = str(name_bits[0] + " " + name_bits[1] + " " + name_bits[2])
				except:
					search  = name_placeholder
				churl           = enrich_url(str(search.upper()))
			else:
				churl = str(url[n])

			# Update offline storage of favourites
			if format == "backup":
				set_list(str(int(n)+1), str(name[n]), str(churl), str(chcountry), str(chgenre))
				list += str(int(n)+1) + ":" + name[n] + " [url=" + churl + "] [genre=" + str(genre_str)  + "] [country=" + str(decode_country(country_bits[0], country_bits[1], country_bits[2])) + "\n"
			elif format == "plain":
				list += str(int(n)+1) + ":" + name[n] + " [url=" + churl + "] [genre=" + str(genre_str)  + "] [country=" + str(decode_country(country_bits[0], country_bits[1], country_bits[2])) + "\n"
			elif format == "csv":
				csv += str(int(n)+1) + "," + name[n] + "," + churl + "," + str(genre_str).replace(",", ";") + "," + str(decode_country(country_bits[0], country_bits[1], country_bits[2])).replace(",", ";") +  "\n"
			elif format == "ssv":
                                ssv += str(int(n)+1) + ";" + name[n] + ";" + churl + ";" + str(genre_str) + ";" + str(decode_country(country_bits[0], country_bits[1], country_bits[2])) + "\n"
			elif format == "pls":
                                pls += '\nFile' + str(int(n)+1)  + '=' + str(churl) + '\nTitle' + str(int(n)+1)  + '=' + str(name[n]) + '\nLength' + str(int(n+1)) + '=-1'
			elif format == "m3u":
                                m3u += '\n#EXTINF:-1, ' + str(name[n]) + ' \n'+ str(churl)
			elif format == "json":
				jsn += '{"channel":"' + str(int(n)+1) + '","name":"' + str(name[n]) + '","url":"' + str(churl) + '","country":"' + str(decode_country(country_bits[0], country_bits[1], country_bits[2])) + '","genre":"' + str(genre_str).replace("and", "&") + '"}'
				if int(int(n)+1) != int(len(name)):
					jsn += ','
			elif format == "json-rpp" or format == "json-rpp-out":
				jsn += '\n\t{\n\t"inc": true,\n\t"name":"' + str(name[n]) + '",\n\t"url":"' + str(churl) + '"\n\t}'
				if int(int(n)+1) != int(len(name)):
					jsn += ','
			else:
				print("Error: Format not supplied (plain, json, json-rpp, pls, m3u, csv, ssv)")
			n+=1

	if format == "backup":
		with open('stations.db', 'r') as file:
			data = file.read()
		return data

	elif format == "plain":
		list = list
	elif format == "csv":
		list = csv
	elif format == "ssv":
		list = ssv
	elif format == "pls":
		pls += "\n" + str(pls_2).replace("0", str(int(len(name))))
		list = pls
		file_out = "export.pls"
		with open(file_out, "w") as o:
			o.write(list)
	elif format == "m3u":
		list = m3u
		file_out = "export.m3u"
		with open(file_out, "w") as o:
			o.write(list)
	elif format == "json":
		list = str(jsn_1) + str(jsn) + str(jsn_2)
		file_out = "export.json"
		with open(file_out, "w") as o:
			o.write(list)
	elif format == "json-rpp":
		# Linux Mint - Radio++ Applet
		list = str(jsn_3) + str(jsn) + str(jsn_4)

		file_rpp  = "./export-rpp.json"
		file_out1 = str(os.path.expanduser('~') + "/Radio/rpp-conf.json")
		file_out2 = str(os.path.expanduser('~') + "/.config/cinnamon/spices/radio@driglu4it/radio@driglu4it.json")
		file_out3 = str(os.path.expanduser('~') + "/.cinnamon/configs/radio@driglu4it/radio@driglu4it.json")


		os.system("mkdir -p " + str(os.path.expanduser('~') + "/Radio"))
		os.system("cp -f " + str(os.path.expanduser('~') + "/.config/cinnamon/spices/radio@driglu4it/radio@driglu4it.json " + str(os.path.expanduser('~') + "/Radio/rpp-conf_") + str(int(time.time())) + ".json"))
		os.system("cp -f " + str(os.path.expanduser('~') + "/.cinnamon/configs/radio@driglu4it/radio@driglu4it.json " + str(os.path.expanduser('~') + "/Radio/rpp-conf_") + str(int(time.time())) + ".json"))

		# https://specifications.freedesktop.org/notification-spec/notification-spec-latest.html
		os.system('notify-send --urgency=normal --category=transfer.complete --icon=audio-x-generic-symbolic "Radio++ Stations Updated" "Favourite presets have been synced with your physical internet radio device!"')

		with open(file_rpp) as i:
			nt=i.read().replace('"stations": [{"name":"toreplace"}]', str(list))

		with open(file_out1, "w") as o:
    			o.write(nt)

		with open(file_out2, "w") as j:
			j.write(nt)

		with open(file_out3, "w") as s:
                        s.write(nt)

		i.close()
		o.close()
		j.close()
		s.close()


		return "Exported stations from your Ocean Digital radio to your ~/Radio directory and imported these stations for you!"
	elif format == "json-rpp-out":
		list = str(jsn_3) + str(jsn) + str(jsn_4)
		file_rpp  = "./export-rpp.json"

		with open(file_rpp) as i:
                        nt=i.read().replace('"stations": [{"name":"toreplace"}]', str(list))
		i.close()
		return str(nt)
	else:
		list = str(name_placeholder) + "," + str(url_placeholder)

	return list




def backup(enrich = False):
	list = get_list("backup", enrich)
	return list

def delete(chid = "100"):
	chid = str(int(chid)-1)
	r = requests.get(url + "/delCh.cgi?CI="+str(chid))
	if r.status_code == 200:
		print("[i] Deleted channel " + str(int(chid)+1) + " from radio @" + str(ip))
		return True
	else:
		return False


def cleaner():
	t = get_total()
	i = 0
	s = 0
	d = False
	while i < t:
		d = delete(str(int(i)+1))
		if d:
			time.sleep(3)
			s+=1
		i+=1

	return int(s)

def restore(enrich = False):
	list 	= []
	dbs	= TinyDB("stations.db")

	deleted = cleaner()

	if int(deleted) > 0:
		i=1
		while i <= int(len(dbs)):
			if i < 100:
				record = dict((dbs.get(doc_id=int(i))))
				chname		= record["name"]
				churl		= record["url"]
				chcountry	= record["country"].replace(",", ";")
				chgenre		= record["genre"].replace(",", ";")

				add(chname, churl, chcountry, chgenre, False)
				time.sleep(2)

			i+=1

	dbs.close()
	return True

def html_decode(s):
	htmlCodes = (
		("", '&#39;'),
		("", '&apos;'),
		('', '&quot;'),
		('_', '&gt;'),
		('_', '&lt;'),
		('and', '&amp;')
	)
	for code in htmlCodes:
		s = s.replace(code[1], code[0])
	return s

def decode_genre(code_1 = 1, code_2 = 66):
	G1 = {
                "name" : "Talk",
                "data" : {
                        "genre" : "Talks-based",
			"1" : {
				"4"  : "Arts and Culture",
				"80" : "Business, Finance and Politics",
				"74" : "Chinese Story Telling",
				"3"  : "Comedy and Humor",
				"5"  : "Education",
				"6"  : "Entertainment and Life Style",
				"2"  : "Kids and Family",
				"11" : "News, Traffic and Weather",
				"7"  : "News,Talk and Information",
				"45" : "Old Time Radio",
				"66" : "Public Radio",
				"8"  : "Religious",
				"10" : "Science and Technology",
				"9"  : "Sports",
			}
		}
	}

	G2 = {
		"name" : "Music",
		"data" : {
			"genre" : "Music",
			"2": {
				"88" : "00s and 10s",
				"89" : "20s, 30s, 40s and Earlier",
				"1"  : "50s, 60s, and Oldies",
				"13" : "70s, 80s, 90s and Classic Hits",
				"65" : "AC - Hot",
				"28" : "AC - Soft AC",
				"75" : "Acoustic and Instrumental",
				"14" : "Adult Contemporary",
				"56" : "African, Tropical and Caribbean",
				"70" : "Art Music",
				"57" : "Asian Music",
				"84" : "Big Bands",
				"78" : "Bluegrass",
				"17" : "Blues, Soul and Funk",
				"58" : "Bollywood",
				"81" : "Chill-out and Lounge",
				"73" : "Chinese Pop",
				"72" : "Chinese Traditional Music",
				"54" : "Christian Contemporary and Christian Rock",
				"18" : "Classical, Opera and Culture",
				"49" : "College Rock",
				"31" : "Community Radio (Variety)",
				"24" : "Country Music",
				"19" : "Dance and Disco",
				"40" : "Drama",
				"87" : "Drum and Bass",
				"85" : "Easy Listening and Relaxation",
				"20" : "EDM, Club, Trance, House and Techno",
				"53" : "European Music",
				"35" : "Folk Music",
				"33" : "Guitar and Piano",
				"27" : "HipHop, RnB, Rap and Urban",
				"55" : "Holiday and Seasonal",
				"60" : "Islamic",
				"21" : "Jazz",
				"22" : "Jazz - Smooth Jazz",
				"69" : "Latin, Spanish and Portugal Music",
				"48" : "Legends",
				"42" : "LGBTQ",
				"43" : "Live Shows",
				"82" : "Love and Romantic",
				"46" : "Mexican Music",
				"44" : "Mid East",
				"32" : "Mix, Remix and Retro",
				"50" : "Movie Soundtracks",
				"77" : "Nature Sounds and Spa Music",
				"25" : "New Age Music",
				"26" : "New Releases, Indie and Unsigned Artists",
				"64" : "News and Music",
				"76" : "Nostalgia",
				"59" : "Office",
				"23" : "Pop",
				"71" : "Punjabi",
				"83" : "Reggae",
				"15" : "Rock - Alternative and Indie Rock",
				"52" : "Rock - Classic Rock",
				"29" : "Rock - Heavy Rock",
				"38" : "Rock - Punk and Goth",
				"30" : "Rock - Soft Rock",
				"37" : "Schlager",
				"16" : "Sleep and Meditation",
				"39" : "Spiritual",
				"41" : "Tamil",
				"12" : "Teen Pop",
				"86" : "Top 40 and CHR",
				"36" : "Underground Music",
				"68" : "Various",
				"34" : "Workout and Exercises",
				"51" : "World Music"
			}
		}
	}

	global genres
	genres = {
		"G1" : G1,
		"G2" : G2
	}
	if code_1 == -1:
		string = "Not Set"
	else:
			string = str(genres["G"+str(code_1)]["data"][str(code_1)][str(code_2)])

	return string

def encode_genre(gstring = "Various"):
	c 	 = 0
	g	 = "1;66"
	gstring  = gstring.replace("&", "and").replace("&amp;", "and")
	key_list = list(genres["G2"]["data"]["2"].keys())
	val_list = list(genres["G2"]["data"]["2"].values())

	try:
		p = val_list.index(str(gstring))
		c = 200
		g = "2;" + key_list[p]
	except NameError:
  		c = 504
	except ValueError:
		c = 404
		key_list = list(genres["G1"]["data"]["1"].keys())
		val_list = list(genres["G1"]["data"]["1"].values())
		try:
			p = val_list.index(str(gstring))
			c = 200
			g = "1;" + key_list[p]
		except NameError:
			c = 504
		except ValueError:
			c = 404
		except:
			c = 604
	except:
		c = 604

	return int(c), str(g)

def decode_country(code_1 = 3, code_2 = 17, code_3 = -1):
	# /php/get_CG.php
	# 1  = Americas
	# 1  = United States
	# 34 = Alabama

	R5 = {
		"name" : "Africa",
		"data" : {
			"country": "Africa",
			"5": {
				"51"  : "Algeria",
				"52"  : "Angola",
				"261" : "Burkina Faso",
				"262" : "Burundi",
                                "267" : "Cabo Verde",
				"108" : "Cameroon",
                                "259" : "Congo Brazzaville",
                                "176" : "Cote-dIvoire",
                                "109" : "DR Congo",
                                "184" : "Ethiopia",
				"188" : "Gambia",
                                "110" : "Ghana",
                                "112" : "Kenya",
                                "113" : "Madagascar",
                                "263" : "Malawi (Republic of Malawi)",
                                "114" : "Mali",
                                "115" : "Mauritius",
                                "55"  : "Morocco",
                                "264" : "Mozambique (Republic of Mozambique)",
                                "116" : "Namibia",
				"189" : "Niger",
                                "27"  : "Nigeria",
                                "256" : "Rwanda",
                                "117" : "Senegal",
                                "266" : "Seychelles",
                                "190" : "Sierra Leone",
                                "28"  : "Sudan",
                                "186" : "Tanzania",
                                "118" : "Tunisia",
                                "185" : "Uganda",
				"187" : "Zambia",
				"149" : "Zimbabwe",

			}
		}
	}

	R1 = {
		"name" : "Americas",
		"data" : {
			"country": "United States",
			"1": {
				"01": "United States",
				"1" : {
					"-1": "United States",
					"34": "Alabama",
					"35": "Alaska",
					"36": "Arizona",
					"37": "Arkansas",
					"38": "California",
					"39": "Colorado",
					"40": "Connecticut",
					"41": "Delaware",
					"42": "Florida",
					"43": "Georgia",
					"85": "Public Area",
					"44": "Hawaii",
					"45": "Idaho",
					"46": "Illinois",
					"47": "Indiana",
					"48": "Iowa",
					"49": "Kansas",
					"50": "Kentucky",
					"51": "Louisiana",
					"52": "Maine",
					"53": "Maryland",
					"54": "Massachusetts",
					"55": "Michigan",
					"56": "Minnesota",
					"57": "Mississippi",
					"58": "Missouri",
					"59": "Montana",
					"60": "Nebraska",
					"61": "Nevada",
					"62": "New Hampshire",
					"63": "New Jersey",
					"64": "New Mexico",
					"65": "New York",
					"66": "North Carolina",
					"67": "North Dakota",
					"68": "Ohio",
					"69": "Oklahoma",
					"70": "Oregon",
					"71": "Pennsylvania",
					"72": "Rhode Island",
					"73": "South Carolina",
					"74": "South Dakota",
					"75": "Tennessee",
					"76": "Texas",
					"77": "Utah",
					"78": "Vermont",
					"79": "Virginia",
					"80": "Washington",
					"88": "Washington D.C.",
					"81": "West Virgina",
					"82": "Wisconsin",
					"83": "Wyoming"
				}
			},
			"country": "Canada",
			"2": {
				"134": "Alberta",
				"135": "British Columbia",
				"136": "Manitoba",
				"137": "New Brunswick",
				"138": "Newfoundland",
				"139": "Northwest Territories",
				"140": "Nova Scotia",
				"141": "Nunavut",
				"142": "Ontario",
				"143": "Prince Albert Island",
				"144": "Qubec",
				"145": "Saskatchewan",
				"146": "Yukon"
			}
		}
 	}

	R2 = {
                "name" : "Asia",
                "data" : {
                        "country": "Asia",
                        "2": {
                                "138": "Afghanistan",
                                "139": "Armenia",
				"140": "Azerbaijan",
				"34" : "Bangladesh",
				"141": "Brunei Darussalam",
				"177": "Cambodia",
				"06" : "China",
				"6"  :  {
					"-1": "China",
					"4"  : "Anhui",
					"5"  : "Beijing",
					"90" : "China Internet stations",
					"1"  : "China National Radio",
					"6"  : "Chongqing",
					"7"  : "Fujian",
					"8"  : "Gansu",
					"9"  : "Guangdong",
					"10" : "Guangxi",
					"11" : "Guizhou",
					"12" : "Hainan",
					"13" : "Hebei",
                                        "15" : "Heilongjiang",
                                        "14" : "Henan",
					"2"  : "Hong Kong SAR",
                                        "16" : "Hubei",
                                        "17" : "Hunan",
                                        "19" : "Jiangsu",
                                        "20" : "Jiangxi",
                                        "18" : "Jilin",
                                        "21" : "Liaoning",
                                        "160": "Macau SAR",
					"22" : "Neimenggu",
                                        "23" : "Ningxia",
                                        "24" : "Qinghai",
                                        "84" : "Shaanxi",
                                        "25" : "Shandong",
                                        "27" : "Shanghai",
                                        "26" : "Shanxi",
                                        "28" : "Sichuan",
                                        "159": "Taiwan Region",
                                        "29" : "Tianjin",
					"31" : "Xinjiang",
					"30" : "Xizang",
					"32" : "Yunnan",
					"33" : "Zhejiang",
				},
				"9"  : "India",
				"36" : "Indonesia",
				"8"  : "Japan",
				"179": "Kazakhstan",
				"7"  : "Korea (South)",
				"174": "Kurdistan",
				"142": "Kyrgyzstan",
				"37" : "Laos",
				"40" : "Malaysia",
				"143": "Maldives",
				"257": "Mongolia",
				"258": "Myanmar",
				"98" : "Nepal",
				"38" : "Pakistan",
				"39" : "Philippines",
				"10" : "Singapore",
				"42" : "Sri Lanka",
				"41" : "Thailand",
				"96" : "Turkey",
				"175": "Uzbekistan",
				"11" : "Vietnam"
			}
		}
	}


	R3 = {
                "name" : "Europe",
                "data" : {
                        "country": "Europe",
                        "3": {
                                "17" : "United Kingdom",
				"150": "Albania",
				"72" : "Austria",
				"152": "Belarus",
				"73" : "Belgium",
				"74" : "Bosnia and Herzegovina",
				"75" : "Bulgaria",
				"76" : "Croatia",
				"77" : "Cyprus",
				"78" : "Czech Republic",
				"80" : "Estonia",
				"154": "Faroe Islands",
				"81" : "Finland",
				"299": "For test only",
                                "16" : "France",
                                "173": "Georgia",
				"015": "Germany",
				"15" : {
					"-1" : "Germany",
					"93" : "Baden-Wurttemberg",
					"94" : "Bavaria",
					"95" : "Berlin",
					"96" : "Brandenburg",
					"97" : "Bremen",
					"98" : "Hamburg",
					"99" : "Hessen",
					"100": "Lower Saxony",
					"101": "Mecklenburg-Vorpommern",
					"102": "North Rhine-Westphalia",
					"103": "Rhineland-Palatinate",
					"104": "Saarland",
					"105": "Saxony",
					"106": "Saxony-Anhalt",
					"107": "Schleswig-Holstein",
					"108": "Thuringia"
				},
                                "155": "Gibraltar",
                                "82" : "Greece",
                                "83" : "Hungary",
                                "84" : "Iceland",
                                "33" : "Ireland",
                                "19" : "Italy",
                                "183": "Kosovo",
				"85" : "Latvia",
                                "156": "Liechtenstein",
                                "86" : "Lithuania",
                                "87" : "Luxembourg",
                                "157": "Macedonia",
                                "88" : "Malta",
                                "158": "Moldova",
                                "89" : "Monaco",
                                "159": "Montenegro",
                                "32" : "Netherlands",
                                "160": "Netherlands Antilles",
				"25" : "Norway",
                                "23" : "Poland",
                                "22" : "Portugal",
                                "90" : "Romania",
                                "20" : "Russia",
                                "91" : "Serbia",
                                "92" : "Slovakia",
                                "172": "Slovenia",
                                "18" : "Spain",
                                "24" : "Sweden",
                                "21" : "Switzerland",
				"94" : "Ukraine",
                                "95" : "Vatican"
			}
		}
	}

	R4 = {
                "name" : "MidEast",
                "data" : {
                        "country": "MidEast",
                        "4": {
                                "44" : "Iran",
                                "43" : "Iraq",
				"26" : "Israel",
				"45" : "Jordan",
				"46" : "Kuwait",
				"47" : "Lebanon",
				"180": "Oman",
				"144": "Palestine",
				"145": "Qatar",
				"146": "Saudi Arabia",
				"49" : "Syria",
				"148": "United Arab Emirates"
			}
		}
	}

	R6 = {
                "name" : "Oceania",
                "data" : {
                        "country": "Oceania",
                        "6": {
                                "30" : "Australia",
                                "164": "Bermuda",
                                "165": "Cook Islands",
                                "166": "Fiji",
                                "167": "French Polynesia",
                                "168": "Guam",
                                "169": "Micronesia",
                                "170": "New Caledonia",
                                "31" : "New Zealand",
                                "161": "Northern Mariana",
                                "104": "Others",
                                "171": "Palau",
				"265": "Ppua New Guinea",
				"119": "Samoa",
				"260": "Vanuatu"
                        }
                }
        }

	R7 = {
                "name" : "Not Set",
                "data" : {
                        "country": "Not Set",
                        "-1": {
				"-1"  : "Skytune"
			},
			"7": {
                                "182" : "Not Set"
			}
		}
	}


	global locations
	locations = {
		"R1" : R1,
		"R2" : R2,
		"R3" : R3,
		"R4" : R4,
		"R5" : R5,
		"R6" : R6,
		"R7" : R7
	}

	# locations["R1"]["data"]["2"]["134"]

	#c = str(codes).split(",")
	#string = str(c[0])
	if int(code_1) == -1 or int(code_1) == 7:
 		string = "Not Set"
	else:
		if str(code_3) == "-1":
			string = str(locations["R"+str(code_1)]["data"][str(code_1)][str(code_2)])
		else:
			string = str(locations["R"+str(code_1)]["data"][str(code_1)][str(code_2)][str(code_3)]) + ":" + str(locations["R"+str(code_1)]["data"][str(code_1)][str(code_2)]["-1"])

	return string



def encode_country(cstring = "Not Set"):
	string = "1;2;-1"
	code   = 200
	i = 1

	while i < 8:
		code, string = search_country(str(i), cstring)
		if code == 200:
			break
		i +=1

	return code, string



def search_country(cdict = "3", cstring = "Not Set"):
	ccolon = False
	if ":" in cstring:
		cstring_bits = cstring.split(":")
		ccolon = True

	c        = 0
	l        = "1;2;-1"

	if ccolon:
		key_list = list(locations[str("R"+cdict)]["data"][str(cdict)].keys())
		val_list = list(locations[str("R"+cdict)]["data"][str(cdict)].values())
		try:
			p = val_list.index(str(cstring_bits[1]))
			c = 200
			l = str(cdict) + ";" + str(int(key_list[p]))
			key_list2 = list(locations[str("R"+cdict)]["data"][str(cdict)][str(int(key_list[p]))].keys())
			val_list2 = list(locations[str("R"+cdict)]["data"][str(cdict)][str(int(key_list[p]))].values())
			try:
				p = val_list2.index(str(cstring_bits[0]))
				c = 200
				l = l + ";" + str(int(key_list2[p]))
			except NameError:
				c = 502
			except ValueError:
				c = 404
			except:
				c = 604
		except NameError:
			c = 501
		except ValueError:
			c = 404
		except:
			c = 604
	else:
		key_list = list(locations[str("R"+cdict)]["data"][str(cdict)].keys())
		val_list = list(locations[str("R"+cdict)]["data"][str(cdict)].values())
		try:
			p = val_list.index(str(cstring))
			c = 200
			l = str(cdict) + ";" + str(int(key_list[p])) + ";-1"
		except NameError:
			c = 501
		except ValueError:
			c = 404
		except:
			c = 604

	return int(c), str(l)

def rtl_reset():
	# Reset Tuner Zero
	os.system('usbreset $(lsusb | grep -i "rtl283" | cut -d " " -f6 | head -n1)')
	# Reset Tuner One
	#os.system('usbreset $(lsusb | grep -i "rtl283" | cut -d " " -f6 | head -n2)')

	return

# Bring HDRadio capability to an Internet Radio with ICECAST2, NRSC5 CLI and an RTL-SDR USB dongle
@background
def hdradio(c = "90.3", p = "0", n = "Local HD Radio", port = "3345", pswd = "rdo"):
	os.system('kill -9 $(ps aux | grep -i "nrsc5" | head -n1 | cut -d " " -f10)')

	if isfloat(str(c)) and p.isnumeric():
		rtl_reset()
		proc = subprocess.Popen(f"nrsc5 -q -d 0 {c} {p} -o - | ffmpeg -re -i pipe:0 -codec:a libmp3lame -b:a 192k -f mp3 -content_type audio/mpeg icecast://source:{pswd}@{sip}:{port}/hdradio-{c}-{p} &", shell=True, stdin=None, stdout=None, stderr=None)

		return True
	else:
		logging.info(f"[i] : The given frequency for HD tuning needs to be given as a float and integer, eg 90.3 0")
		return False


# Bring FM to an Internet Radio with ICECAST2, FFMPEG and RTL_FM
@background
def fmradio(f = "90.3", n = "FM Radio", port = "3345", pswd = "rdo"):
	if isfloat(str(f)):
		logging.info(f"[i] : Tuning the local RTL Radio to {f}Mhz FM")
		try:
			rtl_reset()
			proc = subprocess.Popen(f"rtl_fm -d 0 -f {f}M -M wfm -s 180k -E deemp | sox -traw -r180k -es -b16 -c1 -V1 - -t flac - | ffmpeg -re -i pipe:0 -codec:a libmp3lame -b:a 192k -f mp3 -content_type audio/mpeg icecast://source:{pswd}@{sip}:{port}/fmradio-{f} &", shell=True, stdin=None, stdout=None, stderr=None)
			return True
		except:
			return False
	else:
		logging.info(f"[i] : The given frequency for FM tuning needs to be given as a float, eg 90.3")
		return False


# Bring Noaa Weather Radio to an Internet Radio with ICECAST2, FFMPEG and RTL_FM
@background
def wxradio(f = "162.500", n = "WX Radio", port = "3345", pswd = "rdo"):
	if isfloat(str(f)):
		logging.info(f"[i] : Tuning the local RTL Radio to {f}Mhz FM")
		try:
			rtl_reset()
			proc = subprocess.Popen(f"rtl_fm -d 0 -g 50 -f {f}M -M fm -s 115k -E deemp | sox -traw -r 115k -e s -b 16 -c1 -V1 - -t flac - | ffmpeg -re -i pipe:0 -codec:a libmp3lame -b:a 128k -f mp3 -content_type audio/mpeg icecast://source:{pswd}@{sip}:{port}/wxradio &", shell=True, stdin=None, stdout=None, stderr=None)
			return True
		except:
			return False
	else:
		logging.info(f"[i] : The given frequency for WX tuning needs to be given as a float, eg 162.500")
		return False

@background
def play_yt(c = "jfKfPfyJRdk", p = "91", n = "YouTube Radio", port = "3345", pswd = "rdo"):
	logging.info("[i] : Contacting YouTube to obtain HLS stream")
	try:
		# 91 is default and reduces video bandwidth strain (AAC)
		# MP3 is "mp4a.40.34"
		proc = subprocess.Popen(f"yt-dlp -q -f {p} https://www.youtube.com/watch?v={c} -o - | ffmpeg -t 02:00:00 -v quiet -hide_banner -loglevel quiet -nostats -re -i pipe:0 -vn -codec:a libmp3lame -b:a 192k -f mp3 -content_type audio/mpeg icecast://source:{pswd}@{sip}:{port}/ytradio-{c} &", shell=True, stdin=None, stdout=None, stderr=None)

		# AAC WIP
		# 91 and 92 = HE-AAC "mp4a.40.5"
		# 93 = AAC-LC "mp4a.40.2"
		#proc = subprocess.Popen(f"yt-dlp -q -f {p} https://www.youtube.com/watch?v={c} -o - | ffmpeg -t 02:00:00 -v quiet -hide_banner -loglevel quiet -nostats -re -i pipe:0 -vn -codec:a libfdk_aac -profile:a aac_he_v2 -ab 48k -f adts -content_type audio/aac icecast://source:{pswd}@{sip}:{port}/ytradio-{c} &", shell=True, stdin=None, stdout=None, stderr=None)
	except:
		proc = False

	return proc

# Bring YouTube Live streams to an Internet Radio with ICECAST2, FFMPEG and YT-DLP
@background
def ytradio(c = "jfKfPfyJRdk", p = "91", n = "YouTube Radio", port = "3345", pswd = "rdo"):
	dby = TinyDB("stations_yt.db")
	thread_yt = False
	if p.isnumeric():
		url_rdio = "http://"+ str(sip) +":" + str(port) + "/ytradio-" + str(c)
		url_rm3u = "http://"+ str(sip) +":" + str(port) + "/ytradio-" + str(c) + ".m3u"

		# Find if stream already in database
		streams = Query()
		yfound  = dby.get(streams.vid == str(c))
		nfound  = dby.search(streams.vid == "00000000000")[0]
		logging.info(f"[i] : The next available YouTube preset slot is {nfound.doc_id}")
		if yfound == None:
			if int(nfound.doc_id) > 99:
				nid = 99
			else:
				nid = nfound.doc_id

			logging.info(f"[i] : Adding the stream {c} - {n} to YouTube preset slot {nid}")
			dby.update({'vid': str(c), 'aid': str(p), 'sid': str(n)}, doc_ids=[int(nid)])
		else:
			if int(yfound.doc_id) > 99:
				yid = 99
			else:
				yid = yfound.doc_id

			logging.info(f"[i] : The stream {c} - {n} is found at YouTube preset slot {yid}")
			dby.update({'vid': str(c), 'aid': str(p), 'sid': str(n)}, doc_ids=[int(yid)])

		# Update last played stream
		dby.update({'vid': str(c), 'aid': str(p), 'sid': str(n)}, doc_ids=[int(100)])

		try:
			thread_yt = Thread(target=lambda: play_yt(str(c), str(p), str(n), str(port), str(pswd)))
			thread_yt.start()
			return thread_yt
		except:
			return False
	else:
		return False


@background
def bbcradio(c = "m001p1n9", port = "3345", pswd = "rdo"):
	logging.info("[i] Contacting the BBC to obtain DASH stream")
	try:
		proc = os.system(f"yt-dlp -f mf_cloudfront_nonbidi-audio_eng_1=96000-1 https://www.bbc.co.uk/sounds/play/{c} -o - | ffmpeg -v quiet -hide_banner -loglevel quiet -nostats -re -i pipe:0 -vn -codec:a libmp3lame -b:a 192k -f mp3 -content_type audio/mpeg icecast://source:{pswd}@{sip}:{port}/bbcradio-{c} &")
	except:
		proc = False

	return proc


if __name__ == "__main__":
	main()
