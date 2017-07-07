#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Libraries for crawling naver news

oid_name = {
	'032':'경향신문',
	'005':'국민일보',
	'020':'동아일보',
	'021':'문화일보',
	'081':'서울신문',
	'022':'세계일보',
	'023':'조선일보',
	'025':'중앙일보',
	'028':'한겨레',
	'469':'한국일보',
	'421':'뉴스1',
	'003':'뉴시스',
	'001':'연합뉴스',
	'422':'연합뉴스TV',
	'449':'채널A',
	'215':'한국경제TV',
	'437':'JTBC',
	'056':'KBS 뉴스',
	'214':'MBC 뉴스',
	'057':'MBN',
	'374':'SBS CNBC',
	'055':'SBS 뉴스',
	'448':'TV조선',
	'052':'YTN',
	'009':'매일경제',
	'008':'머니투데이',
	'011':'서울경제',
	'277':'아시아경제',
	'018':'이데일리',
	'366':'조선비즈',
	'014':'파이낸셜뉴스',
	'015':'한국경제',
	'016':'헤럴드경제',
	'079':'노컷뉴스',
	'119':'데일리안',
	'006':'미디어오늘',
	'047':'오마이뉴스',
	'002':'프레시안',
	'138':'디지털데일리',
	'029':'디지털타임스',
	'293':'블로터',
	'031':'아이뉴스24',
	'030':'전자신문',
	'092':'ZDNet Korea',
	'356':'게임메카',
	'216':'골닷컴',
	'435':'골프다이제스트',
	'447':'뉴스엔',
	'347':'데일리e스포츠',
	'439':'디스이즈게임',
	'433':'디스패치',
	'425':'마니아리포트',
	'117':'마이데일리',
	'409':'몬스터짐',
	'343':'베스트일레븐',
	'108':'스타뉴스',
	'144':'스포츠경향',
	'382':'스포츠동아',
	'468':'스포츠서울',
	'396':'스포츠월드',
	'076':'스포츠조선',
	'472':'스포츠타임스',
	'139':'스포탈코리아',
	'477':'스포티비뉴스',
	'465':'아이즈 ize',
	'415':'앳스타일',
	'311':'엑스포츠뉴스',
	'529':'엠스플뉴스',
	'275':'엠파이트',
	'445':'윈터뉴스 코리아',
	'442':'인벤',
	'413':'인터풋볼',
	'241':'일간스포츠',
	'065':'점프볼',
	'111':'조이뉴스24',
	'481':'테니스코리아',
	'312':'텐아시아',
	'440':'티비데일리',
	'236':'포모스',
	'411':'포포투',
	'436':'풋볼리스트',
	'112':'헤럴드POP',
	'404':'enews24',
	'470':'JTBC GOLF',
	'515':'KBO',
	'438':'KBS 연예',
	'408':'MBC연예',
	'410':'MK스포츠',
	'427':'OBS TV',
	'109':'OSEN',
	'416':'SBS funE',
	'213':'TV리포트',
	'444':'뉴스위크 한국판',
	'145':'레이디경향',
	'024':'매경이코노미',
	'417':'머니S',
	'308':'시사IN',
	'262':'신동아',
	'140':'씨네21',
	'094':'월간 산',
	'243':'이코노미스트',
	'007':'일다',
	'033':'주간경향',
	'037':'주간동아',
	'053':'주간조선',
	'353':'중앙SUNDAY',
	'036':'한겨레21',
	'050':'한경비즈니스',
	'127':'기자협회보',
	'310':'여성신문',
	'123':'조세일보',
	'152':'참세상',
	'040':'코리아타임스',
	'044':'코리아헤럴드',
	'296':'코메디닷컴',
	'346':'헬스조선',
	'087':'강원일보',
	'088':'매일신문',
	'082':'부산일보',
	'045':'로이터',
	'348':'신화사 연합뉴스',
	'412':'포토친구',
	'077':'AP연합뉴스',
	'091':'EPA연합뉴스',
	'298':'정책브리핑',
	'441':'코리아넷',
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
	'103': ['241', '239', '240', '237', '238', '376', '242', '243', '244', '248', '245'],
	'104': ['231', '232', '233', '234', '322'],
	'105': ['731', '226', '227', '230', '732', '283', '229', '228'],
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
	'249':'사건사고',
	'250':'교육',
	'251':'노동',
	'254':'언론',
	'252':'환경',
	'59b':'인권/복지',
	'255':'식품/의료',
	'256':'지역',
	'276':'인물',
	'257':'사회 일반',
	#생활/문화
	'241':'건강정보',
	'239':'자동차/시승기',
	'240':'도로/교통',
	'237':'여행/레저',
	'238':'음식/맛집',
	'376':'패션/뷰티',
	'242':'공연/전시',
	'243':'책',
	'244':'종교',
	'248':'날씨',
	'245':'생활문화 일반',
	#세계
	'231':'아시아/호주',
	'232':'미국/중남미',
	'233':'유럽',
	'234':'중동/아프리카',
	'322':'세계 일반',
	#IT/과학
	'731':'모바일',
	'226':'인터넷/SNS',
	'227':'통신/뉴미디어',
	'230':'IT 일반',
	'732':'보안/해킹',
	'283':'컴퓨터',
	'229':'게임/리뷰',
	'228':'과학 일반'
}

def get_oid_name(oid):
	global oid_name
	return oid_name[oid]

def get_mid_code(name):
	global mid_code
	return mid_code[name]

def get_mid_name(mid):
	global mid_name
	return mid_name[mid]

def get_sid1_name(sid1):
	global sid1_name
	return sid_name[sid1]

def get_sid2_list(sid1):
	global sid1_sid2
	return sid1_sid2[sid1]

def get_sid2_name(sid2):
	global sid2_name
	return sid2_name[sid2]

def get_oid_aid(url):
	'''
	Get oid and aid from the url
	'''
	params = url.split('?')[1].split('&')
	oid = 'None'
	aid = 'None'
	for param in params:
		if param.startswith('oid'):
			oid = param[4:]
		elif param.startswith('aid'):
			aid = param[4:]
	return oid, aid


def refine_raw_html(fn):
	'''
	'&#' messes up the html parser.
	This function removes '&#' from a html file.

	@fn: the html file name
	'''
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

def get_raw_html_name_list(date, sid1, sid2, mid, page):
	'''
	Return the raw html file name of list pages
	'''
	return 'raw_html/list.%s.%s.%s.%s.%d.html' % (date, sid1, sid2, mid, page)

def get_raw_html_name_article(date, oid, mid, sid1, sid2, aid):
	'''
	Return the raw html file name of article pages
	'''
	return 'raw_html/article.%s.%s.%s.%s.%s.%s.html' % (date, oid, mid, sid1, sid2, aid)

def get_text_name_article(date, oid, mid, sid1, sid2, aid):
	'''
	Return the raw html file name of article pages
	'''
	return 'article/%s.%s.%s.%s.%s.%s.txt' % (date, oid, mid, sid1, sid2, aid)
