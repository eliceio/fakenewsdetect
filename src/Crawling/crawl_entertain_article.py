#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import os
import codecs
import requests # On Ubuntu, $ sudo pip3 install requests
from bs4 import BeautifulSoup # On Ubuntu, $ sudo pip3 install BeautifulSoup4
import bs4
from crawl_naver_lib import *
import csv

#test
# CSV format
# "date","newspaper","regular/breaking","section","subsection","artical id","title","url"

def crawl_article(date, oid, sid, aid, title, url):
	base_url = 'http://entertain.naver.com/now/read'

	fn = get_raw_html_name_entarticle(date, oid, sid, aid)
	if not os.path.exists(fn): # the page has NOT been crawled.
		print ("Download: " + fn)
		time.sleep(3)
		status = -1
		while status != 200:
			if status >= 0:
				time.sleep(1)
			# ref: http://dgkim5360.tistory.com/entry/python-requests
			params = {'oid':oid,
					'aid':aid}
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
	body = soup.find('div', {"id":"articleBody"})
	if body == None:
		body = soup.find('div', {"id":"articeBody"})
	if body == None:
		print ("======================================")
		print ("ERROR: UNEXPECTED HTML CODE")
		print ("ERROR: PLEASE REPORT THE FOLLOWING CODE TO holypsycho@gmail.com")
		print ('       crawl_article("%s", "%s", "%s", "%s", "title", "%s")' % (date, oid, sid, aid, url))
		print ("ERROR: Crawling continues, but you have to run again")
		print ("ERROR: after the unexpected html code is treated.")
		print ("======================================")
		return

	def get_text_from_tag(tag):
		if type(tag) == bs4.element.Comment:
			return ''
		append_newline = False
		text = ''
		if tag.name == 'br':
			text += '\n'
		elif tag.name == 'span' and tag.get('class') == ['end_photo_org']:
			text += '[사진] '
			append_newline = True
		if hasattr(tag, 'string') and tag.string != None:
			text += tag.string
			return text

		for child in tag.children:
			text += get_text_from_tag(child)
		if append_newline:
			text += '\n'
		return text

	article = ''
	for child in body.contents:
		if type(child) == bs4.element.Comment:
			continue
		if child.name == 'script':
			# exclude the scripts
			continue
		text = get_text_from_tag(child)
		if len(text) == 0:
			continue
		article += text
	article = article.strip()

	# Save to file
	fn = get_text_name_entarticle(date, oid, sid, aid)
	f = codecs.open(fn, 'w', 'utf-8-sig')
	print(title, file=f)
	print(url, file=f)
	print(article, file=f)
	f.close()



def filter_and_crawl(csv_fn, filtering):
	f = open(csv_fn)
	csvreader = csv.reader(f)
	stat_oid = {}
	num = 0
	num_filtered = 0
	for row in csvreader:
		date, oid, sid, aid, title, url = row
		num += 1

		# for stats
		if not oid in stat_oid:
			stat_oid[oid] = 0
		stat_oid[oid] += 1

		# filtering
		if 'oid' in filtering and not oid in filtering['oid']:
			continue
		num_filtered += 1
		#print (row)
		crawl_article(date, oid, sid, aid, title, url)
		if num_filtered % 100 == 0:
			print ("Crawl %d articles" % (num_filtered))

	# show stats
	print ("Total_articles: " + str(num))
	print ("Crawled_articles: " + str(num_filtered))
	print ("Articles for each office")
	if 'oid' in filtering:
		oid_list = filtering['oid']
	else:
		oid_list = list(oid_name.keys())
	for oid in oid_list:
		num_articles = 0
		if oid in stat_oid:
			num_articles = stat_oid[oid]
		print ('"%s" %d' % (oid_name[oid], num_articles))
	print ()
	


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print ('usage: python3 crawl_naver_article.py [csv file]')
		print ('please set the filtering information in the source code')
		sys.exit()

	filtering = {}
	filtering['oid'] = ['433', '001', '109', '076', '009', '119'] # 디스패치, 연합뉴스, OSEN, 스포츠조선, 매일경제, 데일리안

	csv_fn = sys.argv[1]

	filter_and_crawl(csv_fn, filtering)
