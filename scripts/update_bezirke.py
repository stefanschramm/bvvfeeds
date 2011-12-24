#!/usr/bin/python
## -*- coding: utf-8 -*-

import bvvfeeds
import extractor
import re
import json

bezirke_collection = {}
bezirke = extractor.run_extractor(bvvfeeds.extractors['bezirke'], ())

def fix_fullname(b):
	return b.replace(" - ", "-")

for bezirk in bezirke:
	bezirke_collection[bezirk['name']] = fix_fullname(bezirk['fullname'])

f = open(bvvfeeds.application_root + '/data/bezirke.json', 'w')
f.write(json.dumps(bezirke_collection, indent=4, ensure_ascii=False).encode('utf-8'))
f.close()

