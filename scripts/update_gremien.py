#!/usr/bin/python
## -*- coding: utf-8 -*-

import bvvfeeds
import extractor
import re
import json

pretty_replacements = [
	["Ä", "ae"],
	["Ö", "oe"],
	["Ü", "ue"],
	["ä", "ae"],
	["ö", "oe"],
	["ü", "ue"],
	["ß", "ss"],
	["\"", ""],
	["\\", ""],
	["ausschuss fuer ", ""],
	["ausschuss f. ", ""],
	["ausschuss zur ", ""],
	["sausschuss", ""],
	["ausschuss", ""],
	[" und ", "_"],
	[" u. ", "_"],
	[", ", "_"],
	["/", "_"],
	[" ", "_"],
	["-", ""],
	["+", ""],
	["___", "_"],
	["__", "_"],
	["vorstand_der_bvv", "vorstand"],
	["vorstand_bvv", "vorstand"],
	["vorstand_pankow_von_berlin", "vorstand"]
]

# individual fixes
pretty_replacements_map = {
	'sozial': 'soziales',
	'schul': 'schule',
	'geschaeftsordnungsauschuss': 'geschaeftsordnung',
	'haushalt._personal_verwaltung': 'haushalt_personal_verwaltung',
	'haupt': 'hauptausschuss',
	'ag_haushaltsplanerarbeitung_des_kinder_jugendhilfees': 'ag_haushaltsplanerarbeitung_des_kjha',
	'ag_kinder_jugendhilfeplanung_des_kinder_jugendhilfees': 'ag_kinder_jugendhilfeplanung_des_kjha',
	'vorstand_steglitzzehlendorf': 'vorstand',
	'buergerdienste_ordnungs_allg._verwaltungsangelegnheiten': 'buergerdienste_ordnung_verwaltungsangelegnheiten',
	'zeitweiliger_geschaeftsordnung': 'zeitweilige_geschaeftsordnung',
	'temporaerer_transparente_moderne_oeffentlichkeitsarbeit': 'transparente_moderne_oeffentlichkeitsarbeit'
}


def pretty_name(g):
	g = g.encode('utf-8')
	g = g.lower()
	for k, v in pretty_replacements:
		g = g.replace(k, v)
	if pretty_replacements_map.has_key(g):
		return pretty_replacements_map[g]
	return g

gremien_collection = {}

for b in bvvfeeds.bezirke:
	print b
	gremien_collection[b] = {}
	gremien = extractor.run_extractor(bvvfeeds.extractors['gremien'], (b))
	for gremium in gremien:
		if re.search("inaktiv", gremium['name']):
			continue
		if gremium['name'].strip() == "":
			continue
		gremium_detail = extractor.run_extractor(bvvfeeds.extractors['gremium'], (b, gremium['id']))
		name = gremium_detail[0]['name']
		if re.search("^(BVV|Bezirksverordnetenversammlung).*", name):
			name = 'BVV'
		pname = pretty_name(name)
		if gremien_collection[b].has_key(pname):
			# gleichnamiges Gremium bereits in Liste
			if int(gremien_collection[b][pname][0]) < int(gremium['id']):
				# verwende das mit der hoeheren ID
				gremien_collection[b][pname] = [gremium['id'], name]
		else:
			gremien_collection[b][pname] = [gremium['id'], name]

f = open(bvvfeeds.application_root + '/data/gremien.json', 'w')
f.write(json.dumps(gremien_collection, indent=4, ensure_ascii=False).encode('utf-8'))
f.close()

