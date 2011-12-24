#!/usr/bin/python

import bvvfeeds
import extractor

def test_extractor(name, arguments):
	entries = extractor.run_extractor(bvvfeeds.extractors[name], arguments)
	for entry in entries:
		print entry

#test_extractor('tagesordnung', ('pankow', 2973))
#test_extractor('beschlussbuecher', ('pankow'))
#test_extractor('gremien', ('pankow'))
#test_extractor('beschlussbuch', ('pankow', 17))
#test_extractor('sitzungen', ('pankow', 1, 2010, 1, 2010, 12))
test_extractor('drucksache', ('pankow', 2763))
