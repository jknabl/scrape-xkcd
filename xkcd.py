#!/usr/bin/python
import urllib2
import os
import lxml.html
import string
import re

#checks to see whether a file is .jpg
#or .png. Returns a new filename based
#on type.
def filename_by_type(the_string, dest, count, old_filename):
	if the_string.endswith('.jpg'):
		old_filename = re.sub('.jpg$', '', the_string)
		return "%s/comic-%s-%s.jpg" % (dest, count, old_filename)
	elif the_string.endswith('.png'):
		old_filename = re.sub('.png', '', the_string)
		return "%s/comic-%s-%s.png" % (dest, count, old_filename)

#write image file to filename
def write_image_file(img_url, filename, opener):
	errno = 0
	pic = opener.open(img_url)
	picture = pic.read()
	try:
		f = open(filename, 'wb')
		f.write(picture)
		f.close()
	except:
		errno += 1
		print "Something bad happened. Error # %d\n" % errno
	return None

#open the xkcd url and parse the page. Return a
#new url end, the path of the current image, and the
#image path as an array split on '/'
def open_parse_url(url, url_end):
	page = urllib2.urlopen(url % url_end)
	parsed = lxml.html.document_fromstring(page.read())
	for a in parsed.cssselect('li a'):
		if a.get('rel')=='next':
			url_end = a.get('href')
	for x in parsed.cssselect('#comic img'):
			img_url = x.get('src')
			temp_array = string.split(img_url, '/')
	return [url_end, img_url, temp_array]

#Grab all comics from xkcd.
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
			data = open_parse_url(url, url_end)
			url_end, img_url, temp_array = data[0], data[1], data[2]
			for s in temp_array:
				filename = filename_by_type(s, dest, count, old_filename)
			write_image_file(img_url, filename, opener)
		else:
			count += 1
			invalid = True
	return None

def main():
	pull_all_links("/Users/jknabl/Documents/xkcd-scrape")

if __name__=="__main__":
	main()
