#!../bin/python
import os, sys, argparse

from pyradios import RadioBrowser

rb = RadioBrowser()
#help(RadioBrowser)

def main():
	global args

	parser = argparse.ArgumentParser()
	parser.add_argument('--keyword', type=str)
	parser.add_argument('--exact', type=str)
	parser.add_argument('--type', type=str)
	args = parser.parse_args()

	if str(args.exact).lower() == "false":
        	result = rb.search(name=str(args.keyword), name_exact=False)
	else:
        	result = rb.search(name=str(args.keyword), name_exact=True)

	playlist(result, args.type)




def playlist(list, type = "m3u"):
	m3u     = "#EXTM3U"
	pls     = "[playlist]"

	if type.lower() == "m3u":
		for idx, item in enumerate(list):
			m3u += '\n#EXTINF:-1, ' + str(item["name"]) + ' \n'+ str(item["url_resolved"])

		file_out = "export_rb.m3u"
		with open(file_out, "w") as o:
			o.write(m3u)
		print("[i] Search results written to export_rb.m3u")
		return m3u
	elif type.lower() == "pls":
		pls += f"NumberOfEntries={len(list)}"

		for idx, item in enumerate(list):
			pls += '\nFile' + str(int(idx)+1)  + '=' + str(item["url_resolved"]) + '\nTitle' + str(int(idx)+1)  + '=' + str(item["name"]) + '\nLength' + str(int(idx+1)) + '=-1'

		file_out = "export_rb.pls"
		with open(file_out, "w") as o:
			o.write(pls)
		print("[i] Search results written to export_rb.pls")
		return pls
	else:
		return pls


main()
