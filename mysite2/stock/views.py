from django.shortcuts import render
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

def get_data(symbol):
    url = 'http://finance.naver.com/item/sise.nhn?code={}'.format(symbol)
    with urlopen(url) as doc:
        soup = BeautifulSoup(doc, "lxml", from_encoding="euc-kr")
        cur_price = soup.find('strong', id='_nowVal')  # ① # jindo.$Date
        cur_rate = soup.find('strong', id='_rate')  # ②
        stock = soup.find('title')  # ③
        stock_name = stock.text.split(':')[0].strip()  # ④
        return cur_price.text, cur_rate.text.strip(), stock_name

def get_data2(x, date) :
    url = 'https://finance.naver.com/item/sise_day.nhn?code={}'.format(x)
    with urlopen(url) as doc:
        soup = BeautifulSoup(doc, "lxml", from_encoding="euc-kr")
        tables = soup.select('table')
        table = tables[0]

        # 테이블 html 정보를 문자열로 변경하기
        table_html = str(table)

        # 판다스의 read_html 로 테이블 정보 읽기
        table_df_list = pd.read_html(table_html)

        # 데이터프레임 선택하기
        table_df = table_df_list[0]
        dates = '' #빈 문자열
        dates = date[:4] + '.' + date[4:6] + '.' + date[6:8]
        answer = table_df[table_df['날짜'] == dates]['종가']
    return answer


def main_view(request):
    querydict = request.GET.copy()
    mylist = querydict.lists()  # ⑤
    rows = []
    total = 0

    for x in mylist:
        cur_price, cur_rate, stock_name = get_data(x[0])  # ⑥
        price = cur_price.replace(',', '')
        stock_count = format(int(x[1][0]), ',')  # ⑦
        sum = int(price) * int(x[1][0])
        stock_sum = format(sum, ',')

        # QueryDict('a=1&a=2&c=3')
        # <QueryDict: {'a': ['1', '2'],

        if len(x[1]) == 2 :
            before_date_price = get_data2(x[0], x[1][1])
            rows.append([stock_name, x[0], cur_price, stock_count, cur_rate,
                stock_sum, x[1][1]])  # ⑧

            total = total + int(price) * int(x[1][0])  -  (int(before_date_price) * int(x[1][0]) )# ⑨

        else :

            rows.append([stock_name, x[0], cur_price, stock_count, cur_rate,
                         stock_sum])
            total = total + int(price) * int(x[1][0])  # ⑨

        # 이전 날짜 종가와 비교 현 종가 차이




    total_amount = format(total, ',')
    values = {'rows' : rows, 'total' : total_amount}  # ⑩
    return render(request, 'index.html', values)  # ⑪

# Create your views here.
