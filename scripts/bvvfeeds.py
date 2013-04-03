#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import sys
try:
	import config
except:
	print "Please copy scripts/config.py.dist to scripts/config.py and adjust it."
	sys.exit(1)

application_root = config.application_root
document_root = config.document_root
homepage = config.homepage

feeds_dir = 'rss'


try:
	feeds = json.load(open(application_root + '/data/gremien.json'))
except:
	feeds = {}
try:
	bezirke = json.load(open(application_root + '/data/bezirke.json'))
except:
	bezirke = {}

link_top = 'http://www.berlin.de/ba-%s/bvv-online/to020.asp?TOLFDNR=%s&options=4'
link_drucksache = 'http://www.berlin.de/ba-%s/bvv-online/vo020.asp?VOLFDNR=%s&options=4'
link_sitzung = 'http://www.berlin.de/ba-%s/bvv-online/to010.asp?SILFDNR=%s&options=4'
link_gremium = 'http://www.berlin.de/ba-%s/bvv-online/si018.asp?GRA=%s'
link_bezirk = 'http://bvvfeeds.kesto.de/#%s'

def parse_date(d):
	try:
		return datetime.datetime.strptime(d, '%d.%m.%Y')
	except:
		return None

extractors = {
	'bezirke': {
		'url': 'http://www.berlin.de/rubrik/politik-und-verwaltung/bezirksaemter/',
		'list_expression': '//div[@class=\'inner\']/ul/li/a',
		'property_map': {
			'fullname': [['./text()', '^(.*)$']],
			'name': [['./@href', '^/ba-(.+)/$']]
		}
	},
	'beschlussbuecher': {
		'url': 'http://www.berlin.de/ba-%s/bvv-online/bb000.asp',
		'list_expression': '//div[@id=\'allrisContent\']/table[@class=\'mainwork\']/tr/td/table/tr/td/table/tr/td/a/b',
		'property_map': {
			'name': [['./text()', '^(.*)$']],
			'id': [['../@href', '^.*=([0-9]+)$']]
		}
	},
	'beschlussbuch': {
		'url': 'http://www.berlin.de/ba-%s/bvv-online/bb022.asp?BBLFDNR=%s',
		'list_expression': '//div[@id=\'allrisContent\']//tr[@class=\'zl11\' or @class=\'zl12\']',
		'property_map': {
#			'date': [['.//td[@class=\'text2\']/text()', '^([0-9]{2}\.[0-9]{2}\.[0-9]{4}).*$']],
			'date': [
				[
					'.//td[@class=\'text2\']/text()',
					'^([0-9]{2}.[0-9]{2}.[0-9]{4}).*$',
					lambda d : datetime.datetime.strptime(d, '%d.%m.%Y')
				]
			],
			'name': [
				['.//td[5]/a/text()', '^(.*)$'],
				['.//td[5]/text()', '^(.*)$']
			],
			'id': [['.//td[5]/a/@href', '^.*SILFDNR=([0-9]+)&.*$']] # silfdnr
		}
	},
	'ausschuesse': {
		'url': 'http://www.berlin.de/ba-%s/bvv-online/au010.asp',
                'list_expression': '//div[@id=\'allrisContent\']//tr[@class=\'zl11\' or @class=\'zl12\']',
		'property_map': {
			'name': [['./td[2]/a/text()', '^(.*)$', lambda n: n.strip()]],
			'id': [['./td[2]/a/@href', '^.*AULFDNR=([0-9]+)&.*$']],
			'text5': [['./td[3]/text()', '^(.*)$']]
		}
	},
	'ausschuss': {
		'url': 'http://www.berlin.de/ba-%s/bvv-online/au020.asp?AULFDNR=%s',
		'list_expression': '//a/h3',
		'property_map': {
			'gra': [['../@href', '^.*GRA=([0-9]+)$']]
		}
	},
	'gremien': {
		'url': 'http://www.berlin.de/ba-%s/bvv-online/si018.asp',
		'list_expression': '//select[@name=\'GRA\']/option',
		'property_map': {
			'name': [['./text()', '^(.*)$', lambda n: n.strip()]],
			'id': [['./@value', '^(.*)$']]
		}
	},
	'gremium': {
		'url': 'http://www.berlin.de/ba-%s/bvv-online/si018.asp?GRA=%s',
		'list_expression': '//tr[@class=\'zk1\'][1]/th',
		'property_map': {
			'name': [['./text()', '^.*Sitzungen des Gremiums (.*) im Zeitraum.*$']]
		}
	},
	'tagesordnung': {
		'url': 'http://www.berlin.de/ba-%s/bvv-online/to010.asp?SILFDNR=%s&options=4',
		'list_expression': '//div[@id=\'allriscontainer\' or @id=\'allrisContent\']//tr[@class=\'zl11\' or @class=\'zl12\']',
		'property_map': {
			'name': [
				['.//td[4]/a/text()', '^(.*)$'],
				['.//td[4]/text()', '^(.*)$']
			],
			'id': [['.//td[1]//a/@href', '^.*TOLFDNR=([0-9]+).*$']], # tolfdnr
			'drucksache_id': [['.//td[6]//a/@href', '^.*VOLFDNR=([0-9]+)&.*$']], # volfdnr
			'drucksache_name': [['.//td[6]//a/text()', '^(.*)$']], # volfdnr
		}
	},
	'drucksache': {
		'url': 'http://www.berlin.de/ba-%s/bvv-online/vo020.asp?VOLFDNR=%s&options=4',
		'list_expression': '//div[@id=\'allrisContent\']/table[1]',
		'property_map': {
			'name': [['.//h1/text()', '^(.*)$']],
			'betreff': [['./tr[2]/td[1]/table/tr[1]/td/table/tr[1]/td[2]/text()', '^(.*)$']],
			'initiator': [['./tr[2]/td[1]/table/tr[1]/td/table/tr[4]/td[2]/text()', '^(.*)$']],
			'drucksache-art': [['./tr[2]/td[1]/table/tr[1]/td/table/tr[6]/td[2]/text()', '^(.*)$']]
			#'content': [['./tr[2]/td[1]/div[2]/text()', '^(.*)$']]
		}
	},
	'drucksachen': {
		'url': 'http://www.berlin.de/ba-%s/bvv-online/vo040.asp',
		'list_expression': '//div[@id=\'allriscontainer\' or @id=\'allrisContent\']//tr[@class=\'zl11\' or @class=\'zl12\']',
		'property_map': {
			'id': [['.//td[1]/form/input[@name=\'VOLFDNR\']/@value', '^(.*)$']],
			'name': [['.//td[2]/a/text()', '^(.*)$']],
			'initiator': [['.//td[4]/text()', '^(.*)$']],
			'date': [['.//td[6]/text()', '^.*([0-9]{2}.[0-9]{2}.[0-9]{4}).*$',  parse_date]],
			'type': [['.//td[7]/text()', '^(.*)$']]
		}
	},
	'sitzungen': {
		# argumente: year_from, month_from, year_to, month_to
		'url': 'http://www.berlin.de/ba-%s/bvv-online/si018.asp?GRA=%s&YYV=%s&MMV=%s&YYB=%s&MMB=%s',
		'list_expression': '//div[@id=\'allriscontainer\' or @id=\'allrisContent\']//tr[@class=\'zl11\' or @class=\'zl12\']',
		'property_map': {
			'date': [
				[
					'./td[1]/text()',
					'^.*([0-9]{2}.[0-9]{2}.[0-9]{4}).*$',
					parse_date
				]
			],
			# TODO: replace time with time_from and time_to
			'time': [
				['./td[2]/text()', '^.*([0-9]{2}:[0-9]{2} - [0-9]{2}:[0-9]{2}).*$'],
				['./td[2]/text()', '^.*([0-9]{2}:[0-9]{2}).*$']
			],
			'name': [
				['.//td[4]/a/text()', '^(.*)$'],
				['.//td[4]/text()', '^(.*)$']
			],
			'id': [['.//td[4]/a/@href', '^.*SILFDNR=([0-9]+)&.*$']] # silfdnr
		}
	}
}

