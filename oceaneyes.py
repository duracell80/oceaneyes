#!/usr/bin/python3
import sys, requests, json
#from bs4 import BeautifulSoup
#from requests_html import HTMLSession




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
	r = requests.get(url + "/php/playing.php")
	d = json.loads(str(r.text).replace("'", '"'))

	if d["result"] == "success":
		status = "Playing: " + d["name"]
	else:
		status = "Stopped"
	return  status



def play(ch = 0):
	r = requests.get(url + "/doApi.cgi", params = {"AI":"16", "CI": str(ch - 1)})
	return



def add_current():
	# Get current number of favs first
	r = requests.get(url + "/php/favList.php?PG=0", params = {"PG":"0"})
	c = get_total("fav", r)

	# Set new fav
	r = requests.get(url + "/doApi.cgi", params = {"AI":"8"})
	t = get_total("fav", r)

	# Read currently playing
	current = status()
	station = current.split(": ")

	if t > c:
		code 	= 200
	else:
		code 	= 201

	return code, station[1]

def del_current():
	# Get current number of favs first
	r = requests.get(url + "/php/favList.php?PG=0", params = {"PG":"0"})
	c = get_total("fav", r)

	# Del currently playing
	r = requests.get(url + "/doApi.cgi", params = {"AI":"4"})
	t = get_total("fav", r)

	# Read currently playing
	current = status()
	station = current.split(": ")

	if t < c:
		code    = 200
	else:
		code    = 201

	return code, station[1]


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

def decode_country(codes):
	# 1  = Americas
	# 1  = United States
	# 34 = Alabama


	R1 = {
		"name" : "Americas",
		"data" : {
			"country": "United States",
			"1": {
				"34": "Alabama",
				"35": "Alaska"
			},
                        "country": "Canada",
                        "2": {
				"134": "Alberta",
				"135": "British"
			}
		}
	}

	locations = {
		"R1" : R1
	}

	# locations["R1"]["data"]["2"]["134"]

	c = str(codes).split(",")
	string = str(c[0])

	return codes

def decode_genre(codes):
	string = "TBD"
	return string

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



if __name__ == "__main__":
	main()
