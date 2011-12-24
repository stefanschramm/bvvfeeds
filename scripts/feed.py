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

def list_tops(bezirk, sitzung):
	tops = extractor.run_extractor(bvvfeeds.extractors['tagesordnung'], (bezirk, sitzung['id']))
	abstract = ''
	for top in tops:
		if top['name'] == None:
			continue
		try:
			abstract += '<ul>' + format_top(bezirk, top) + '</ul>'
		except Exception, e:
			print e
			print sitzung
			print top
			continue
	return abstract

def format_top(bezirk, top):
	abstract = '<li>'
	if top['id'] != None:
		abstract += '<a href="' + (bvvfeeds.link_top % (bezirk, top['id'])) + '">' + top['name'] + ' (' + top['id'] + ')</a>'
	else:
		# (should not happen)
		abstract += top['name']
	if top['drucksache_id'] != None:
		abstract += ' (<a href="' + (bvvfeeds.link_drucksache % (bezirk, top['drucksache_id'])) + '">Drucksache ' + top['drucksache_name'] + '</a>)'
	abstract += "</li>"
	return abstract


def create_feed(bezirk, gremium, gremium_name, outfile):
	
	# fetch complete previous year
	year_current = datetime.datetime.now().year
	year_prev = year_current - 1 
	month = datetime.datetime.now().month
	sitzungen = extractor.run_extractor(bvvfeeds.extractors['sitzungen'], (bezirk, gremium, year_prev, month, year_current, month))
	sitzungen = sorted(sitzungen, key=lambda s : s['date'], reverse=True)
	
	feeditems = []
	for sitzung in sitzungen:
		if (sitzung['date'] == None or sitzung['name'] == None):
			print "Skipping Sitzung:" + str(sitzung)
			continue
		if (sitzung['id'] == None):
			title = sitzung['date'].strftime('%Y-%m-%d') + ': ' + sitzung['name']
			link = bvvfeeds.link_gremium % (bezirk,gremium)
			description = '(Tagesordnung nicht verfügbar.)'
		else:
			title = sitzung['date'].strftime('%Y-%m-%d') + ': ' + sitzung['name'] + " (" + str(sitzung['id']) + ")"
			link = bvvfeeds.link_sitzung % (bezirk,sitzung['id'])
			description = list_tops(bezirk, sitzung)
		try:
			guid = PyRSS2Gen.Guid(hashlib.md5(pickle.dumps((title,link,description))).hexdigest(), isPermaLink=False)
			item = PyRSS2Gen.RSSItem(title = title, link = link, description = description, guid = guid, pubDate = sitzung['date'])
			feeditems.append(item)
		except Exception, e:
			print e
			print sitzung
			continue
	
	rss = PyRSS2Gen.RSS2(
		title = bvvfeeds.bezirke[bezirk] + " - " + gremium_name,
		link = bvvfeeds.link_bezirk % bezirk,
		description = "Sitzungen " + gremium_name + " " + bvvfeeds.bezirke[bezirk],
		lastBuildDate = datetime.datetime.utcnow(),
		items = feeditems
	)
	
	rss.write_xml(open(outfile, 'w'), 'utf-8')

