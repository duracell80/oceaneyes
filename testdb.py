#!../bin/python3
import os, sys

from tinydb import TinyDB, Query

dby = TinyDB("stations_yt.db")



streams = Query()
#result  = dby.get(streams.vid == str("jfKfPfyJRdk"))
row  = dby.search(streams.vid == "00000000000")[0]
print(row.doc_id)

sys.exit()
