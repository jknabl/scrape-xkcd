#!/usr/bin/env python
import urllib2
import os
import lxml.html
import string
import re
def pull_all_links(dest):
	invalid = False
	url = "http://www.xkcd.com%s"
	opener = urllib2.build_opener()
	url_end = "/1/"
	count = 0
	old_filename = ""
	filename = ""
	while not invalid:
		if not (url_end == "#"):
			count += 1
			page = urllib2.urlopen(url % url_end)
			parsed = lxml.html.document_fromstring(page.read())
			for a in parsed.cssselect('li a'):
				if a.get('rel')=="next":
					url_end = a.get('href')
			for x in parsed.cssselect('#comic img'):
				img_url = x.get('src')
				#grab old filename, produce new one				
				temp_array = string.split(img_url, '/')
				for s in temp_array:
					if s.endswith('.jpg'):
						old_filename = re.sub('.jpg$', '', s)
						filename = "%s/comic-%s-%s.jpg" % (dest, count, old_filename)
					elif s.endswith('.png'):
						old_filename = re.sub('.png$', '', s)
						filename = "%s/comic-%s-%s.png" % (dest, count, old_filename)
				pic = opener.open(img_url)
				picture = pic.read()
				print "FILENAME IS %s" % filename
				fout = open(filename, "wb")
				fout.write(picture)
				fout.close()
				print "Got image at %s.\n Wrote new file %s.\n" % (img_url, filename)
		else:
			invalid = True
	return None

def main():
	pull_all_links("/Users/jknabl/Documents/xkcd-scrape")

if __name__=="__main__":
	main()
