#!/usr/bin/python
# -*- coding: utf-8 -*-

import bvvfeeds
import extractor
import datetime
import PyRSS2Gen
import hashlib
import pickle

def cstr(s):
	if s == None:
		return ""
	return s

def create_feed(bezirk, outfile):
	
	drucksachen = extractor.run_extractor(bvvfeeds.extractors['drucksachen'], (bezirk))

	# replace empty date fields with current date
	date_current = datetime.datetime.today()
	for ds in drucksachen:
		if not ds['date']:
			ds['date'] = date_current
		else:
			ds['date'] = ds['date']

	drucksachen = sorted(drucksachen, key=lambda s : s['date'], reverse=True)
	
	feeditems = []
	for drucksache in drucksachen:
		title = drucksache['name']
		link = "http://www.berlin.de/ba-%s/bvv-online/vo020.asp?VOLFDNR=%s" % (bezirk, drucksache['id'])
		description = "Art: %s<br />Initiator: %s<br />Link: <a href=\"%s\">%s</a>" % (drucksache['type'], drucksache['initiator'], link, link);
		try:
			guid = PyRSS2Gen.Guid(link, isPermaLink=True)
			item = PyRSS2Gen.RSSItem(title = title, link = link, description = description, guid = guid, pubDate = drucksache['date'])
			feeditems.append(item)
		except Exception, e:
			print e
			print drucksache
			continue
	
	rss = PyRSS2Gen.RSS2(
		title = bvvfeeds.bezirke[bezirk] + " - Drucksachen",
		# TODO: anpassen
		link = bvvfeeds.link_bezirk % bezirk,
		description = "Drucksachen " + bvvfeeds.bezirke[bezirk],
		lastBuildDate = datetime.datetime.utcnow(),
		items = feeditems
	)
	
	rss.write_xml(open(outfile, 'w'), 'utf-8')

