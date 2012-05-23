#!/usr/bin/python

import lxml.html
import urllib
import re
import time

# TODO:
# - run multiple extractors:
#   - first collect all urls; fetch them; run corresponding extractor (for thoose using the same urls)

def run_extractor(extractor, arguments = ()):
	time.sleep(4)
	doc = lxml.html.fromstring(urllib.urlopen(extractor['url'] % arguments).read())
	entries = []
	nodes = doc.xpath(extractor['list_expression'])
	for node in nodes:
		entry = {}
		for (p,v) in extractor['property_map'].items():
			content = None
			current_try = 0
			while content == None and current_try < len(v):
				xpath_expression = v[current_try][0]
				regexp = v[current_try][1]
				nodeplist = node.xpath(xpath_expression)
				if len(nodeplist) < 1:
					entry[p] = None
				else:
					content = "".join(nodeplist)
					if content != None:
						m = re.search(regexp, content, re.S)
						if m != None:
							content = m.group(1)
						else:
							content = None
					if len(v[current_try]) >= 3:
						content = v[current_try][2](content)
					entry[p] = content
				current_try += 1
		entries.append(entry)
	return entries

