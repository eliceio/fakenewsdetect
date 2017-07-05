#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import os
import codecs
import requests # On Ubuntu, $ sudo pip3 install requests
from bs4 import BeautifulSoup # On Ubuntu, $ sudo pip3 install BeautifulSoup4
from crawl_naver_lib import *

# CSV format
# "date","newspaper","regular/breaking","section","subsection","artical id","title","url"

def main():
	base_url = 'http://news.naver.com/main/officeList.nhn'


	fn = 'raw_html/officeList.html'
	if not os.path.exists(fn): # the page has NOT been crawled.
		status = -1
		while status != 200:
			if status >= 0:
				time.sleep(1)
			# ref: http://dgkim5360.tistory.com/entry/python-requests
			params = {}
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
	div = soup.find('div', { "id" : "groupOfficeList"})
	item_list = div.find_all('li')

	for item in item_list:
		office = item.a.contents[0].strip()
		oid, aid = get_oid_aid(item.a['href'])
		print ("'" + oid + "':'" + office + "',")





if __name__ == '__main__':
	main()
