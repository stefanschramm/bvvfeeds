#!/usr/bin/python

import bvvfeeds
import os
import shutil

# create document root
if not os.path.exists(bvvfeeds.document_root):
	os.makedirs(bvvfeeds.document_root)

# copy rss dir
if os.path.exists(bvvfeeds.document_root + '/' + bvvfeeds.feeds_dir):
	shutil.rmtree(bvvfeeds.document_root + '/' + bvvfeeds.feeds_dir)
shutil.copytree(bvvfeeds.application_root + '/' + bvvfeeds.feeds_dir, bvvfeeds.document_root + '/' + bvvfeeds.feeds_dir)

# create feed targets in rss dir
for b in bvvfeeds.bezirke:
	if not os.path.exists(bvvfeeds.document_root + '/' + bvvfeeds.feeds_dir + '/' + b):
		os.makedirs(bvvfeeds.document_root + '/' + bvvfeeds.feeds_dir + '/' + b)

# copy static
if os.path.exists(bvvfeeds.document_root + '/' + 'static'):
	shutil.rmtree(bvvfeeds.document_root + '/' + 'static')
shutil.copytree(bvvfeeds.application_root + '/static', bvvfeeds.document_root + '/' + 'static')

# copy some stuff to docroot
shutil.copy(bvvfeeds.application_root + '/static/favicon.ico', bvvfeeds.document_root + '/favicon.ico')
shutil.copy(bvvfeeds.application_root + '/static/robots.txt', bvvfeeds.document_root + '/robots.txt')

