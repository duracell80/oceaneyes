#!/usr/bin/python3
import sys, time, socket, requests, urllib.parse, json


global headers, url_placeholder, name_placeholder
url_placeholder 	= "https://streaming.radio.co/s5c5da6a36/listen"
name_placeholder	= "Bird Song radio"

headers = {
	"User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"Accept-Encoding": "gzip,deflate",
	"Upgrade-Insecure-Requests": "1",
	"Connection": "keep-alive"
}



def main():
	return


def init(ipaddr = "192.168.1.100"):
	global url, ip
	ip  = str(ipaddr)
	url = "http://" + ipaddr

	settings = {
		"ipaddress" : ip,
		"language"  : "English"
        }

	stations = {
		"ch0":  {
			"name"    : "BBC World Service",
			"url"     : "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
			"country" : "United Kingdom",
			"genre"   : "Public Radio"
		},
		"ch1":  {
			"name"    : "WPLN - Nashville (NPR)",
			"url"     : "https://wpln.streamguys1.com/wplnfm.mp3",
			"country" : "United States, Tennessee",
			"genre"   : "Public Radio"
                }
	}
	return settings, stations


def is_online():
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

def is_streamable(churl = "https://streaming.radio.co/s5c5da6a36/listen", chpreview = False):
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
		return False
	else:
		try:
			import vlc
			chid, chname, churl, country_str, genre_str = info_get(str(int(chid)))

			print("[i] Playing " + str(chname) + " locally ...")

			vlc_ins = vlc.Instance('--input-repeat=-1', '-q')
			vlc_pla = vlc_ins.media_player_new()
			vlc_med = vlc_ins.media_new(str(churl))

			vlc_pla.set_media(vlc_med); vlc_pla.play()
			vlc_pla.audio_set_mute(False);
			time.sleep(chduration)

			did_play = str(vlc_pla.is_playing()); time.sleep(1); vlc_pla.stop()


			result = False
			if str(vlc_pla.get_state()) == "State.Stopped":
				if did_play == "1":
					result = True
				else:
					vlc_pla.stop()

		except ModuleNotFoundError:
			return False

	return result


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


def status():
	status = "Unknown"
	try:
		r = requests.get(url + "/php/playing.php")
		d = json.loads(str(r.text).replace("'", '"'))

		if d["result"] == "success":
			status = "IPRadio Playing: " + d["name"]
		else:
			status = "IPRadio Stopped"
	except Exception as e:
		status = "Unknown"

	return  status


def info_get(chid = "1"):
	chid = str(int(chid)-1)

	t = get_total("fav")

	if int(chid) > t:
		chname = str(name_placeholder)
		churl  = str(url_placeholder)
		chcountry = "United Kingdom"
		chgenre = "Nature Sounds & Spa Music"
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
	r = requests.get(url + "/doApi.cgi", params = {"AI":"16", "CI": str(ch - 1)})
	return


def delete(chid = "100"):
	#/delCh.cgi?CI=46
	chid = str(int(chid)-1)
	r = requests.get(url + "/delCh.cgi", params = {"CI":chid})
	return


def add(chname = "Local Streaming", churl = "http://192.168.1.200:1234/stream.mp3", chcountry = "-1", chgenre = "-1", chplay = False):
	t = 0
	c = get_total("fav")

	if c > 99:
		code = 403
		station = "Presets Full"
		return code, station
	else:
		f = {'EX': '0', 'chName': str(chname), 'chUrl': str(churl), 'chCountry': str(chcountry), 'chGenre': str(chgenre)}
		r = requests.post(url + "/addCh.cgi", data=f)

		time.sleep(8)
		t = get_total("fav")

		if t > c:
			code = 200
			station = str(chname)
		else:
			code = 500
			station = "None"

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

	current = status()
	if "stopped" in current.lower():
		station = "none"
	else:
		# Set new fav
		r = requests.get(url + "/doApi.cgi", params = {"AI":"8"})
		t = get_total("fav")

		# Read currently playing
		current = status()
		currspl = current.split(": ")
		station = currspl[1]

	if t > c:
		code 	= 200
	else:
		code 	= 500

	return code, station

def del_current():
	# Get current number of favs first
	t = 0
	c = get_total("fav")

	current = status()
	if "stopped" in current.lower():
		station = "none"
	else:
		# Del currently playing
		r = requests.get(url + "/doApi.cgi", params = {"AI":"4"})
		t = get_total("fav")

		# Read currently playing
		current = status()
		currspl = current.split(": ")
		station = currspl[1]

	if t < c:
		code    = 200
	else:
		code    = 500

	return code, station

def move(f = "2", t = "1"):
	#/moveCh.cgi?CI=49&DI=48&EX=0
	# offset by 1 so -1 off values supplied in method
	f = int(int(f)-1)
	t = int(int(f)-1)

	c = get_total("fav")

	if f > 99 or t > 99 or t > c or f > c or f < 0 or t < 0:
		string = "500, Cannot move - presets out of range"
		return string
	else:
		r = requests.post(url + "/moveCh.cgi?EX=0&CI="+ str(int(f)) +"&DI="+ str(int(t)))

		string = "200, Moved preset " + str(int(f)+1) + " to " + str(int(t)+1)
		return string


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


def get_list(format = "plain"):
	id, name, url, country, genre = list_get()

	n = 0

	list	= ""
	pls_1 	= "[playlist]"
	pls_2 	= "NumberOfEntries=0"
	pls	= str(pls_1)
	m3u 	= "#EXTM3U"
	jsn	= ""
	jsn_1	= '{"stations":['
	jsn_2	= ']}'
	csv	= "" # comma
	ssv	= "" # semicolon

	while n < int(len(name)):
		if name is not None:
			genre_bit = genre[n].split(",")
			genre_str = decode_genre(code_1 = int(genre_bit[0]), code_2 = int(genre_bit[1]))

			country_bits  = country[n].split(",")
			#print(country_bits[0] + ":" + country_bits[1] + ":" + country_bits[2]  + " - " + str(name[n]))

			if format == "plain":
				list += str(int(n)+1) + ":" + name[n] + " [url=" + url[n] + "] [genre=" + str(genre_str)  + "] [country=" + str(decode_country(country_bits[0], country_bits[1], country_bits[2])) + "\n"
			elif format == "csv":
				csv += str(int(n)+1) + "," + name[n] + "," + url[n] + "," + str(genre_str).replace(",", ";") + "," + str(decode_country(country_bits[0], country_bits[1], country_bits[2])).replace(",", ";") +  "\n"
			elif format == "ssv":
                                ssv += str(int(n)+1) + ";" + name[n] + ";" + url[n] + ";" + str(genre_str) + ";" + str(decode_country(country_bits[0], country_bits[1], country_bits[2])) + "\n"
			elif format == "pls":
                                pls += '\nFile' + str(int(n)+1)  + '=' + str(url[n]) + '\nTitle' + str(int(n)+1)  + '=' + str(name[n]) + '\nLength' + str(int(n+1)) + '=-1'
			elif format == "m3u":
                                m3u += '\n#EXTINF:-1, ' + str(name[n]) + ' \n'+ str(url[n])
			elif format == "json":
				jsn += '{"channel":"' + str(int(n)+1)  + '","name":"' + str(name[n])  + '","url":"' + str(url[n]) + '","country":"' + str(decode_country(country_bits[0], country_bits[1], country_bits[2]))  + '","genre":"' + str(genre_str).replace("and", "&") + '"}'
				if int(int(n)+1) != int(len(name)):
					jsn += ','
			else:
				print("Error: Format not supplied (plain, pls, m3u, csv, ssv)")
			n+=1

	if format == "plain":
		list = list
	elif format == "csv":
		list = csv
	elif format == "ssv":
		list = ssv
	elif format == "pls":
		pls += "\n" + str(pls_2).replace("0", str(int(len(name))))
		list = pls
	elif format == "m3u":
		list = m3u
	elif format == "json":
		list = str(jsn_1) + str(jsn) + str(jsn_2)
	else:
		list = "Birdsong," + str(url_placeholder)

	return list





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

if __name__ == "__main__":
	main()
