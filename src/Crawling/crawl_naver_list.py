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

def crawl_list(date, sid1, sid2, mid='shm'):
	base_url = 'http://news.naver.com/main/list.nhn'
	page = 0
	num_items = 0


	while True: # for all pages
		page += 1
		fn = get_raw_html_name_list(date, sid1, sid2, mid, page)
		if not os.path.exists(fn): # the page has NOT been crawled.
			print ("Download: " + fn)
			time.sleep(3)
			status = -1
			while status != 200:
				if status >= 0:
					time.sleep(1)
				# ref: http://dgkim5360.tistory.com/entry/python-requests
				params = {
						'sid1':sid1,
						'sid2':sid2,
						'mid':mid,
						'mode':'LS2D',
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
		div = soup.find('div', { "class" : "list_body newsflash_body"})
		item_list = []
		for ul in div.find_all('ul'):
			item_list.extend(ul.find_all('li'))

		for item in item_list:
			num_items += 1
			dt = item.find('dt', {"class": None})
			url = dt.a['href']
			title = dt.a.contents[0].strip()
			oid, aid = get_oid_aid(url)
			# Print as a csv format
			print ('"%s","%s","%s","%s","%s","%s","%s","%s"' % (date, oid, mid, sid1, sid2, aid, title.replace('"', '""'), url))

		# check whether this is the last page or not
		paging = soup.find('div', {"class":"paging"})
		if paging.find('a', {"class":"next"}) != None:
			continue
		max_page = 0
		page_links = paging.find_all('a')
		for a in page_links:
			cl = a.get("class")
			if (cl != None) and ((cl == 'pre') or (cl[0] == 'pre')):
				continue
			p = int(a.contents[0].strip())
			if max_page < p:
				max_page = p

		this_page = paging.find('strong')
		if not this_page == None:
			p = int(this_page.contents[0].strip())
			if max_page < p:
				max_page = p

		if max_page == page:
			break # this is the last page
		else:
			continue # this is not the last page
	#print (num_items)




if __name__ == '__main__':

	if len(sys.argv) != 4:
		print ('usage: python3 crawl_naver_list.py [year] [month] [sid1]')
		sys.exit()

	year = int(sys.argv[1])
	month = int(sys.argv[2])
	sid1 = sys.argv[3]
	days = range(1,monthrange(year, month)[1] + 1)
	for day in days:
		for sid2 in get_sid2_list(sid1):
			date = '%04d%02d%02d' % (year, month, day)
			crawl_list(date, sid1, sid2)
