#!/usr/bin/python3
import sys, requests, json
#from bs4 import BeautifulSoup
#from requests_html import HTMLSession




global headers
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
	station_names = []
	station_urls  = []

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
					data_url  = str(data_item[3]).replace("****** Channel URL is maintained by Skytune", "https://streaming.radio.co/s5c5da6a36/listen")
					# URL's maintained by Skytune are masked, play birdsong instead

					station_names.append(data_name)
					station_urls.append(data_url)
			c+=1
		i+=1


	return station_names, station_urls


def list(format = "plain"):
	name, url = list_get()

	n = 0
	pls_1 	= "[playlist]"
	pls_2 	= "NumberOfEntries=0"
	pls	= str(pls_1)
	m3u 	= "#EXTM3U"

	while n < int(len(name)):
		if name is not None:
			if format == "plain":
				print(name[n] + " : " + url[n])
				n+=1
			elif format == "csv":
                        	print(name[n] + "," + url[n])
                        	n+=1
			elif format == "pls":
                                pls += '\nFile' + str(int(n)+1)  + '="' + str(url[n]) + '"\nTitle' + str(int(n)+1)  + '=' + str(name[n])
                                n+=1
			else:
				print("Format not supplied (plain, pls, m3u, csv)")
	if format == "pls":
		pls += "\n" + str(pls_2).replace("0", str(int(len(name))))
		print(pls)





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
