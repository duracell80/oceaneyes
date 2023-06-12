#!/usr/bin/python3
import sys, time, requests, urllib.parse, json


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


def init(ip = "192.168.1.100"):
	global url; url = "http://" + ip

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



def get_total(thing = "fav", r = ""):
	if thing == "fav":
		s = str(r.text).split("\n")
		i = len(s)
		c = s[i-2].split(":")
		f = c[2].split(",")
		t = int(f[0])

	return t



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
		status = "Offline"

	return  status



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
	r = requests.get(url + "/php/favList.php?PG=0", params = {"PG":"0"})
	c = get_total("fav", r)

	if c > 99:
		code = 403
		station = "Presets Full"
		return code, station
	else:
		f = {'EX': '0', 'chName': str(chname), 'chUrl': str(churl), 'chCountry': str(chcountry), 'chGenre': str(chgenre)}
		r = requests.post(url + "/addCh.cgi", data=f)

		time.sleep(8)
		s = requests.get(url + "/php/favList.php?PG=0", params = {"PG":"0"})
		t = get_total("fav", s)

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
	else:
		lines = open(filename).readlines()
		added = "None"

	return added



def add_current():
	# Get current number of favs first
	t = 0
	r = requests.get(url + "/php/favList.php?PG=0", params = {"PG":"0"})
	c = get_total("fav", r)

	current = status()
	if "stopped" in current.lower():
		station = "none"
	else:
		# Set new fav
		r = requests.get(url + "/doApi.cgi", params = {"AI":"8"})
		t = get_total("fav", r)

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
	r = requests.get(url + "/php/favList.php?PG=0", params = {"PG":"0"})
	c = get_total("fav", r)

	current = status()
	if "stopped" in current.lower():
		station = "none"
	else:
		# Del currently playing
		r = requests.get(url + "/doApi.cgi", params = {"AI":"4"})
		t = get_total("fav", r)

		# Read currently playing
		current = status()
		currspl = current.split(": ")
		station = currspl[1]

	if t < c:
		code    = 200
	else:
		code    = 201

	return code, station


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

	r = requests.get(url + "/php/favList.php?PG=0")
	s = str(r.text).split("\n")
	f = str(s[int(len(s)-2)]).split(":")
	n = (str(f[2])).split(",")


	data_size = int(n[0])			# Total of favourites
	data_page = round(data_size/10)		# Pages of favourites

	#if int(data_size) < int(data_page * 10):
	#	data_page = data_page -1 	# Correct page number

	i = 0
	while i < data_page:
		c = 0
		r = requests.get(url + "/php/favList.php?PG=" + str(i))
		s = str(r.text).split("\n")

		while c < int(len(s)):
			if c >= 2 and c < int(len(s)-2):
				if s[c] is not None:
					data_item = str(s[c]).replace("myFavChannelList.push", "").split('"')
					data_name = str(html_decode(str(data_item[1])))
					data_cbit = str(html_decode(str(data_item[4]))).replace("]", "").replace(");", "").split("[")
					data_cont = str(data_cbit[2][:-1])
					data_genr = str(data_cbit[3])


					data_url  = str(data_item[3]).replace("****** Channel URL is maintained by Skytune", url_placeholder)
					# URL's maintained by Skytune are masked, play birdsong instead

					station_countries.append(data_cont)
					station_genres.append(data_genr)
					station_names.append(data_name)
					station_urls.append(data_url)
			c+=1
		i+=1

	return station_names, station_urls, station_countries, station_genres


def list(format = "plain"):
	name, url, country, genre = list_get()

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
			if format == "plain":
				list += name[n] + " [" + url[n] + "]\n"
			elif format == "csv":
				csv += name[n] + "," + url[n] + "\n"
			elif format == "ssv":
                                ssv += name[n] + ";" + url[n] + "\n"
			elif format == "pls":
                                pls += '\nFile' + str(int(n)+1)  + '=' + str(url[n]) + '\nTitle' + str(int(n)+1)  + '=' + str(name[n]) + '\nLength' + str(int(n+1)) + '=-1'
			elif format == "m3u":
                                m3u += '\n#EXTINF:-1, ' + str(name[n])  + '\n'+ str(url[n])
			elif format == "json":
				#["Radio SoBro","https://streamer.radio.co/s951fc6edc/listen",0,[[1,1,75],[2,24]]]
				#["Station name", "Station URL",int,[[Country Code],[Genre Code]]]

				jsn += '{"channel":"' + str(int(n)+1)  + '","name":"' + str(name[n])  + '","url":"' + str(url[n]) + '","country":"' + str(decode_country(country[n]))  + '","genre":"' + str(genre[n]) + '"}'
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

def decode_genre(codes):
	string = "TBD"
	return string



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
