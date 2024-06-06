## -*- coding: utf-8 -*-

import requests
import sys
import json
import codecs
import datetime

########### TOURNAMENT HASH ############

tourhash = "6628ba2468f5760228bba551"
#tourhash = "5f2eb61c0ad5e05d5e217f8c"

########################################

# Writes the entrylist from the jcg with the input tournament hash to "entrylist.txt"
# Writes the html of the tournament page with the input tournament number to "data.txt"
def svoPull():
    r = requests.get("https://dtmwra1jsgyb0.cloudfront.net/stages/" + tourhash + "/matches")
    with codecs.open("data.txt", "w", encoding='utf-8') as out:
        out.write(r.text)

svoPull()
