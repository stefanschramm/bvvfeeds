#!/usr/bin/python

import feed
import bvvfeeds
import traceback

for bezirk,gremien in bvvfeeds.feeds.items():
	for gremium,g in gremien.items():
		outfile = bvvfeeds.document_root + '/' + bvvfeeds.feeds_dir + '/' + bezirk + '/' + gremium + '.xml'
		try:
			feed.create_feed(bezirk, g[0], g[1], outfile)
		except Exception as inst:
			print "Error while creating " + outfile + ":"
			print traceback.print_exc(inst)
