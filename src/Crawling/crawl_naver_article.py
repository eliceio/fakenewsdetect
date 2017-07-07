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

def crawl_article(date, oid, mid, sid1, sid2, aid, title, url):
	base_url = 'http://news.naver.com/main/read.nhn'

	fn = get_raw_html_name_article(date, oid, mid, sid1, sid2, aid)
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
					'oid':oid,
					'aid':aid}
			res = requests.get(base_url, params)
			status = res.status_code
		f = codecs.open(fn, 'w', 'utf-8-sig')
		print(res.text, file=f)
		#f.write(res.text)
		f.close()
		refine_raw_html(fn)

	print ("====================================================================")
	print (fn)
	print ("====================================================================")
	# Parse the list page and get the list
	f = open(fn)
	soup = BeautifulSoup(f, 'html.parser') 
	f.close()
	body = soup.find('div', {"id":"articleBodyContents"})
	print ("1st:" + str(body))
	if body == None:
		body = soup.find('div', {"id":"articeBody"})
		print ("2nd:" +str(body))

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

	print (article)
	# Save to file
	fn = get_text_name_article(date, oid, mid, sid1, sid2, aid)
	f = codecs.open(fn, 'w', 'utf-8-sig')
	print(title, file=f)
	print(url, file=f)
	print(article, file=f)
	f.close()



def filter_and_crawl(csv_fn, filtering):
	f = open(csv_fn)
	csvreader = csv.reader(f)
	stat_oid = {}
	stat_sid1 = {}
	stat_sid2 = {}
	num = 0
	num_filtered = 0
	for row in csvreader:
		date, oid, mid, sid1, sid2, aid, title, url = row
		num += 1

		# for stats
		if not oid in stat_oid:
			stat_oid[oid] = 0
		if not sid1 in stat_sid1:
			stat_sid1[sid1] = 0
		if not sid2 in stat_sid2:
			stat_sid2[sid2] = 0
		stat_oid[oid] += 1
		stat_sid1[sid1] += 1
		stat_sid2[sid2] += 1

		# filtering
		if 'oid' in filtering and not oid in filtering['oid']:
			continue
		if 'mid' in filtering and not mid in filtering['mid']:
			continue
		if 'sid1' in filtering and not sid1 in filtering['sid1']:
			continue
		if 'sid2' in filtering and not sid1 in filtering['sid2']:
			continue
		num_filtered += 1
		#print (row)
		crawl_article(date, oid, mid, sid1, sid2, aid, title, url)
		if num_filtered % 100 == 0:
			print ("Crawl %d articles" % (num_filtered))

	return
	# show stats
	print ("Total articles: " + str(num))
	print ("Crawled articles: " + str(num_filtered))
	print ("Articles for each office")
	if 'oid' in filtering:
		oid_list = filtering['oid']
	else:
		oid_list = list(oid_name.keys())
	for oid in filtering['oid']:
		num_articles = 0
		if oid in stat_oid:
			num_articles = stat_oid[oid]
		print ("%s: %d" % (oid_name[oid], num_articles))
	print ()
	
	print ("Articles for each section")
	if 'sid1' in filtering:
		sid1_list = filtering['sid1']
	else:
		sid1_list = list(sid1_name.keys())
	for sid1 in sid1_list:
		num_articles = 0
		if sid1 in stat_sid1:
			num_articles = stat_sid1[sid1]
		print ("%s %d" % (sid1_name[sid1], num_articles))

	print ("Articles for each subsection")
	if 'sid2' in filtering:
		sid2_list = filtering['sid2']
	elif 'sid1' in filtering:
		sid2_list = []
		for sid1 in filtering['sid1']:
			sid2_list.extend(sid1_sid2[sid1])
	else:
		sid2_list = list(sid2_name.keys())
	for sid2 in sid2_list:
		num_articles = 0
		if sid2 in stat_sid2:
			num_articles = stat_sid2[sid2]
		print ("%s: %d" % (sid2_name[sid2], num_articles))


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print ('usage: python3 crawl_naver_article.py [csv file]')
		print ('please set the filtering information in the source code')
		sys.exit()

	filtering = {}
	filtering['oid'] = ['020', '028', '119', '047'] # 동아일보, 한겨레, 오마이뉴스, 데일리안
	#filtering['mid'] = []
	filtering['sid1'] = ['100']
	#filtering['sid2'] = []
	#filtering['aid'] = []

	csv_fn = sys.argv[1]

	filter_and_crawl(csv_fn, filtering)
