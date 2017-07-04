#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import os
import codecs
import requests # On Ubuntu, $ sudo pip3 install requests
from bs4 import BeautifulSoup # On Ubuntu, $ sudo pip3 install BeautifulSoup4


oid_name = {
	'032':'경향신문',
	'005':'국민일보',
# TODO: contain all newpapers
}

mid_code = {	
	'속보':'sec',
	'일반':'shm'
}
mid_name = {	
	'sec':'속보',
	'shm':'일반'
}

sid1_name = {
	'100': '정치',
	'101': '경제',
	'102': '사회',
	'103': '생활/문화',
	'104': '세계',
	'105': 'IT/과학',
}

sid1_sid2 = {
	'100': ['264', '265', '268', '266', '267', '269'],
	'101': ['259', '268', '261', '771', '260', '262', '310', '264'],
	'102': ['249', '250', '251', '254', '252', '59b', '255', '256', '276', '257'],
	'103': [],
	'104': [],
	'105': [],
}

sid2_name = {
	#정치
	'264':'청와대',
	'265':'국회/정당',
	'268':'북한',
	'266':'행정',
	'267':'국방/외교' ,
	'269':'정치일반',
	#경제
	'259':'금융',
	'268':'증권',
	'261':'산업/재계',
	'771':'중기/벤처',
	'260':'부동산',
	'262':'글로벌경제',
	'310':'생활경제',
	'264':'경제 일반',
	#사회
	#생활/문화
	#TODO
	#세계
	#TODO
	#IT/과학
	#TODO
}

def refine_raw_html(fn):
	# '&#' corrupt the html parser
	f = open(fn)
	refined = ''
	detected = False
	for line in f:
		if not '&#' in line:
			refined += line
			continue
		mode = 0
		last_idx = -1
		i = 0
		while i < len(line):
			if mode == 0:
				if line[i] == '&':
					mode = 1
					last_idx = i
			elif mode == 1:
				if line[i] == '#':
					mode = 2
				else:
					mode = 0
			elif mode == 2:
				if line[i] in ['0','1','2','3','4','5','6','7','8','9']:
					pass
				elif line[i] == ';':
					mode = 0
				else:
					# detected
					line = line[:last_idx] + line[last_idx + 2:]
					i = last_idx - 1
					detected = True
			i = i + 1
		refined += line
	f.close()
	if not detected:
		return
	f = open(fn, 'w')
	f.write(refined)
	f.close()

def raw_html_name(date, sid1, sid2, mid, page):
	return 'raw_html/list.%s.%s.%s.%s.%d.html' % (date, sid1, sid2, mid, page)

def get_oid_aid(url):
	params = url.split('?')[1].split('&')
	oid = 'None'
	aid = 'None'
	for param in params:
		if param.startswith('oid'):
			oid = param[4:]
		elif param.startswith('aid'):
			aid = param[4:]
	return oid, aid
def crawl_list(date, sid1, sid2, mid='shm'):
	base_url = 'http://news.naver.com/main/list.nhn'
	page = 0
	num_items = 0


	while True: # for all pages
		page += 1
		fn = raw_html_name(date, sid1, sid2, mid, page)
		if not os.path.exists(fn): # the page has NOT been crawled.
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

		f = open(fn)
		soup = BeautifulSoup(''.join(f.readlines()), 'html.parser') 
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
	sid1 = '100' # 정치
	for day in range(1,31):
		for sid2 in sid1_sid2[sid1]:
			crawl_list('201606%02d' % day, '100', sid2)
