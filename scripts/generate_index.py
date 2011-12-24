#!/usr/bin/python
## -*- coding: utf-8 -*-

import bvvfeeds
import codecs

from mako.template import Template

tpl = Template(filename=bvvfeeds.application_root + '/templates/index.htm', default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
content = tpl.render(b=bvvfeeds)

f = open(bvvfeeds.document_root + '/index.htm', 'w')
f.write(content)
f.close()

