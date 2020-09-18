import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import pandas as pd
from urllib import parse
import time
from multiprocessing import Pool, Process
def crawling_news(category):
    total = pd.DataFrame()
    base_url = "https://news.naver.com/main/list.nhn?"
    para = {'mode': ['LS2D'],
            'mid': ['shm'],
            'sid2': ['259'],
            'sid1': ['101'],
            'date': ['20200915'],
            'page': ['2']}
    para['sid2'] = category
    # 일주일 동안 데이터 수집
    for day in range(6, 13):
        para['date'] = str(date(2020, 9, day)).replace("-", "")
        para['page'] = 1000
        r = requests.get("https://news.naver.com/main/list.nhn?", params=para)
        # print (r.url)
        bs = BeautifulSoup(r.text)
        # 마지막 페이지 번호를 가져온다.
        b = bs.find('div', id='main_content')
        last_page = bs.find('div', class_='paging').find("strong").text
        # print("===========")
        # print (last_page)
        # print("===========")
        for page in range(1, int(last_page) + 1):
            # print (page)
            para['page'] = page
            r = requests.get("https://news.naver.com/main/list.nhn?", params=para)
            bs = BeautifulSoup(r.text)
            for x in bs.find({"div": "list_body newsflash_body"}).findAll("dl", class_=""):
                total = total.append(pd.DataFrame([[x.select("a")[-1].text.strip(), x.select("a")[-1]['href'],
                                                    x.find({"span": "lede"}).text,
                                                    x.find("span", class_="writing").text,
                                                    str(date(2020, 9, day))]],
                                                  columns=['title', 'url', 'content', 'company', 'date']))
    return total
if __name__ == "__main__":
    pool = Pool(4)
    start = time.time()
    result = pool.map(crawling_news, ['259', '258', '310', '263'] )
    print (time.time() - start)