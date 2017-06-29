import requests
import time
import random
import sys
import datetime
import codecs
import os
from bs4 import BeautifulSoup


def get_page_for_bigkinds(target_url, startdate, enddate, pagestartnumber):
    global cur_session, headers

    payload = {'keyword': '',
               # 'popKeyword': '',
               'realKeyword': '',
               "keywordType": "N",
               # "fieldRadio": "_search",
               "search_field": "_search",
               "byline": "",
               # "methodRadio": "0",
               "search_method": "0",
               'fromDate': startdate,
               'toDate': enddate,
               "provider_code": "01100101",
               "provider_name": "경향신문",
               # "main_provider": "01100101",
               "category_code": "",
               "category_name": "",
               "larm_incident_category_path": "",
               "larm_incident_category_nm": "",
               "news_id": "",
               "listPage": pagestartnumber,
               "listCount": 10,
               "orderByOption": "asc"
               }

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "Getting web page\t", startdate, enddate, pagestartnumber)

    # check the web page is in HDD or not
    # wait
    time.sleep(random.randint(1, 5))

    try:
        req = requests.Request('POST', target_url, headers=headers, data=payload)
        prepared = cur_session.prepare_request(req)
        response_one = cur_session.send(prepared)
        if 200 == response_one.status_code:
            # response_one.encoding = 'euc-kr'
            return response_one.text
        else:
            return False
    except:
        print("Unexpected error:", sys.exc_info()[0])
        time.sleep(600 + random.random() * 60)
        cur_session = requests.Session()
        cur_session.get(url=target_url, headers=headers)
        return get_page_for_bigkinds(target_url, startdate, enddate, pagestartnumber)


def write_file(content, filename, path='./html/'):
    with codecs.open(path + filename + '.html', "w", "utf-8-sig") as f_htmlFile:
        print(content, file=f_htmlFile)


def main():
    global cur_session, headers, start_year, end_year

    cur_date = datetime.datetime(start_year, 1, 1, 18, 0)

    cur_session = requests.Session()
    cur_session.get(url=main_url, headers=headers)

    cur_year = cur_date.year
    f_result_txt = codecs.open("Article_List_Output_Khan_%d.txt" % cur_year, "w", "utf-8")
    try:
        while cur_date.year <= end_year:
            print(cur_date.strftime('Download the article at %Y-%m-%d'))

            # Check the existence of directory
            dir_name = root_dirpath + cur_date.strftime('%Y%m')
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            # Download list page in cur_date
            page_id = 1
            while True:
                cur_date_str = cur_date.strftime('%Y%m%d')
                article_list_page = get_page_for_bigkinds(main_url, cur_date_str, cur_date_str, page_id)
                write_file(article_list_page, cur_date.strftime('%Y%m%d_' + str(page_id)), path='./%s/' % dir_name)

                # analyze the result
                try:
                    soup = BeautifulSoup(article_list_page, 'html.parser')
                    article_html_list = soup.find("div", {"class": "list"})
                    article_html_list = article_html_list.find_all("div")

                    if len(article_html_list) > 1:
                        for article in article_html_list:
                            try:
                                article_meta = article.find("dt").find("a")
                                print("\t".join(
                                    (article_meta.contents[0].strip(), article_meta['href'].strip(), cur_date_str)),
                                      file=f_result_txt)
                            except:
                                pass
                        page_id += 1
                    else:
                        break
                except:
                    pass

            cur_date += datetime.timedelta(days=1)
            # cur_date += datetime.timedelta(days=3660)

            if cur_date.year != cur_year and cur_date.year <= end_year:
                # Year is changed
                f_result_txt.close()
                cur_year = cur_date.year
                f_result_txt = codecs.open("Article_List_Output_Khan_%d.txt" % cur_year, "w")
    except:
        print('Something wrong!')
        print(sys.exc_info())

    f_result_txt.close()


'''
    Program Start
'''
if __name__ == "__main__":
    try:
        start_year = int(sys.argv[1])
        end_year = int(sys.argv[2])
    except (IndexError, TypeError):
        print("Run debug mode: start and end year: 1990")
        start_year = 1990
        end_year = 1990

    root_dirpath = "./khan_list/"
    if not os.path.exists(root_dirpath):
        os.makedirs(root_dirpath)
    cur_session = None

    main_url = "http://www.bigkinds.or.kr/search/totalSearchList.do"
    headers = {'Host': "www.bigkinds.or.kr",
               'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
               'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               'Accept-Language': "en-US,en;q=0.8,ko-KR;q=0.5,ko;q=0.3",
               'Accept-Encoding': 'gzip, deflate',
               'DNT': "1",
               "Referer": "http://www.bigkinds.or.kr/search/totalSearchList.do",
               'Connection': 'keep-alive',
               "Upgrade-Insecure-Requests": "1"
               }

    main()
