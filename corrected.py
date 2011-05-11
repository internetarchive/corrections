#!/usr/bin/env python
from urllib2 import urlopen, HTTPError
from urlparse import urlparse
from httplib import HTTPConnection

import sys
import subprocess
import os
import string
import StringIO
import json
import cgi
import cgitb
import re
import io
import appauth

cgitb.enable()

import abbyyhtml
import abbyygethtml

def s3save(url,data):
    auth="LOW %s:%s"%(appauth.key,appauth.secret)
    c=HTTPConnection("s3.us.archive.org")
    c.request("PUT",url,data,{"Authorization":auth})
    r=c.getresponse()

olid=sys.argv[1]
bookid=sys.argv[2]
text=open(sys.argv[3]).read().decode('utf-8')
style_start=re.search("(?i)<style[^>]*>",text)
style_end=re.search("(?i)</style[^>]*>",text)
body_start=re.search("(?i)<body[^>]*>",text)
body_end=re.search("(?i)</body[^>]*>",text)
body=False
style=False
if ((body_start) and (body_end)):
    if ((style_start) and (style_end)):
        style=text[style_start.end():style_end.start()]
        body=text[body_start.end():body_end.start()]
    else:
        body=text

newdoc=abbyygethtml.remakehtml(olid,body,style)
newdata=newdoc.encode('utf-8')
save_path="http://s3.us.archive.org/%s/%s_corrected.html"%(bookid,bookid)
save_path="http://s3.us.archive.org/abbyyhtml/%s_corrected.html"%bookid
s3save(save_path,newdata)
print "<html>\n<head>\n<title>All saved</title>\n</head>\n<body>\n<p>Your edits were saved.</p>\n</body>\n"

