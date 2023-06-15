#!/usr/bin/python3
import sys, time, socket, requests, urllib.parse, json


global headers, url_placeholder
url_placeholder = "https://streaming.radio.co/s5c5da6a36/listen"
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
			status = "IP Playing: " + d["name"]
		else:
			status = "IP Stopped"
	except Exception as e:
		status = "Unknown"

	return  status


def info_get(chid = "1"):
	chid = str(int(chid)-1)

	t = get_total("fav")

	if int(chid) > t:
		chname = "Bird Song Radio"
		churl  = str(url_placeholder)
		chcountry = "United Kingdom"
		chgenre = "Nature Sounds and Spa Music"
	else:
		station_ids, station_names, station_urls, station_countries, station_genres = list_get()

		chid      = station_ids[int(chid)]
		chname    = station_names[int(chid)]
		churl     = station_urls[int(chid)]
		chcountry = station_countries[int(chid)]
		chgenre   = station_genres[int(chid)]

		genre_bit = chgenre.split(",")
		genre_str = decode_genre(code_1 = int(genre_bit[0]), code_2 = int(genre_bit[1]))

	return chid, chname, churl, chcountry, genre_str


def play(ch = 0):
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
			code = 201
			station = "None"

		return code, station



def add_import(filename = "./import.pls", encode = False):
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

				print("[+] " + str(s) + " of " + str(int((t/3))) + " ...")
				code, station = add(chname, churl, chcountry, chgenre, False)
				added += str(str(code) + "," + str(station) + "," + str(churl) + "\n")
			c+=1
	elif ".json" in filename:
		# Get genres into global scope
		decode_genre(1, 11)

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

			code, chgenre = encode_genre(str(i['genre']))
			print("[+] " + str(s) + " of " + str(int(t)) + " ...")

			#code, station = add(chname, churl, chcountry, chgenre, False)
			added += str(str(code) + "," + str(chname) + "," + str(churl) + "," + str(chgenre) + "," + str(chcountry) + "\n")

			print(added)
			c+=1
	else:
		#lines = open(filename).readlines()
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
		code 	= 201

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
		code    = 201

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

			if format == "plain":
				list += str(int(n)+1) + ":" + name[n] + " [url=" + url[n] + "] [genre=" + str(genre_str)  + "]\n"
			elif format == "csv":
				csv += str(int(n)+1) + "," + name[n] + "," + url[n] + "," + str(genre_str) + "\n"
			elif format == "ssv":
                                ssv += str(int(n)+1) + ";" + name[n] + ";" + url[n] + ";" + str(genre_str) + "\n"
			elif format == "pls":
                                pls += '\nFile' + str(int(n)+1)  + '=' + str(url[n]) + '\nTitle' + str(int(n)+1)  + '=' + str(name[n]) + '\nLength' + str(int(n+1)) + '=-1'
			elif format == "m3u":
                                m3u += '\n#EXTINF:-1, ' + str(name[n]) + ' \n'+ str(url[n])
			elif format == "json":
				#["Radio SoBro","https://streamer.radio.co/s951fc6edc/listen",0,[[1,1,75],[2,24]]]
				#["Station name", "Station URL",int,[[Country Code],[Genre Code]]]

				jsn += '{"channel":"' + str(int(n)+1)  + '","name":"' + str(name[n])  + '","url":"' + str(url[n]) + '","country":"' + str(decode_country(country[n]))  + '","genre":"' + str(genre_str) + '"}'
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
				"89" : "20s 30s 40s and Earlier",
				"1"  : "50s 60s and Oldies",
				"13" : "70s 80s 90s and Classic Hits",
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
				"20" : "EDM, Club, Trance, House & Techno",
				"53" : "European Music",
				"35" : "Folk Music",
				"33" : "Guitar & Piano",
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
		string = "Genre Not Set"
	else:
			string = str(genres["G"+str(code_1)]["data"][str(code_1)][str(code_2)])

	return string

def encode_genre(gstring = "Various"):
	code 	 = 0
	key_list = list(genres["G2"]["data"]["2"].keys())
	val_list = list(genres["G2"]["data"]["2"].values())

	try:
		p = val_list.index(str(gstring))
		c = 200
		g = "2;" + key_list[p]
	except NameError:
  		code = 504
	except ValueError:
		code = 404
		key_list = list(genres["G1"]["data"]["1"].keys())
		val_list = list(genres["G1"]["data"]["1"].values())
		try:
			p = val_list.index(str(gstring))
			c = 200
			g = "1;" + key_list[p]
		except NameError:
			code = 504
		except ValueError:
			code = 404
		except:
			code = 604
	except:
		code = 604

	return int(c), str(g)

def decode_country(codes):
	# /php/get_CG.php
	# 1  = Americas
	# 1  = United States
	# 34 = Alabama


	R1 = {
		"name" : "Americas",
		"data" : {
			"country": "United States",
			"1": {
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
                "name" : "Europe",
                "data" : {
                        "country": "Europe",
                        "3": {
                                "17" : "United Kingdom",
				"150": "Albania"
			}
		}
	}



	locations = {
		"R1" : R1,
		"R2" : R2
	}

	# locations["R1"]["data"]["2"]["134"]

	#c = str(codes).split(",")
	#string = str(c[0])

	return codes



if __name__ == "__main__":
	main()
