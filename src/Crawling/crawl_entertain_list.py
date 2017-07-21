#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import os
import codecs
import requests # On Ubuntu, $ sudo pip3 install requests
from bs4 import BeautifulSoup # On Ubuntu, $ sudo pip3 install BeautifulSoup4
from crawl_naver_lib import *
from calendar import monthrange

# CSV format
# "date","newspaper","regular/breaking","section","subsection","artical id","title","url"

def crawl_list(date, sid):
	base_url = 'http://entertain.naver.com/now'
	page = 0
	num_items = 0
	num_errors = 0


	while True: # for all pages
		page += 1
		fn = get_raw_html_name_entlist(date, sid, page)
		if not os.path.exists(fn): # the page has NOT been crawled.
			print ("Download: " + fn, file=sys.stderr)
			time.sleep(3)
			status = -1
			while status != 200:
				if status >= 0:
					time.sleep(1)
				# ref: http://dgkim5360.tistory.com/entry/python-requests
				params = {
						'sid':sid,
						'date':date,
						'page':str(page)}
				res = requests.get(base_url, params)
				status = res.status_code
			f = codecs.open(fn, 'w', 'utf-8-sig')
			print(res.text, file=f)
			#f.write(res.text)
			f.close()
			refine_raw_html(fn)

		# Parse the list page and get the list
		f = open(fn)
		soup = BeautifulSoup(f, 'html.parser') 
		f.close()
		ul = soup.find('ul', { "class" : "news_lst news_lst2"})
		item_list = []
		for li in ul.find_all('li'):
			item_list.append(li)

		if len(item_list) == 1 and item_list[0].find('a') == None:
			break # this is the last page

		for item in item_list:
			num_items += 1
			try:
				div = item.find('div', {"class": "tit_area"})
				link = div.find('a', {"class": "tit"})
				url = 'http://entertain.naver.com' + link['href']
				if len(link.contents) == 0:
					title = '[Untitled]'
				else:
					title = link.contents[0].strip()
				oid, aid = get_oid_aid(url)
				# Print as a csv format
				print ('"%s","%s","%s","%s","%s","%s"' % (date, oid, sid, aid, title.replace('"', '""'), url))
			except:
				print ('ERROR at %s' % (get_raw_html_name_entlist(date, sid, page)))
				print ('==================================================')
				print (item)
				print ('==================================================')
				num_errors += 1


	return num_items, num_errors, page




if __name__ == '__main__':

	if len(sys.argv) != 3:
		print ('usage: python3 crawl_naver_list.py [year] [month]')
		sys.exit()

	total_items = 0
	total_errors = 0
	total_pages = 0
	year = int(sys.argv[1])
	month = int(sys.argv[2])
	sid = '106'
	days = range(1,monthrange(year, month)[1] + 1)
	#days = [14]
	for day in days:
		date = '%04d-%02d-%02d' % (year, month, day)
		num_items, num_errors, pages = crawl_list(date, sid)
		total_items += num_items
		total_errors += num_errors
		total_pages += pages

	print ('%04d-%02d' % (year, month), file=sys.stderr)
	print ("total_items: %d" % (total_items), file=sys.stderr)
	print ("total_errors: %d" % (total_errors), file=sys.stderr)
	print ("total_pages: %d" % (total_pages), file=sys.stderr)
