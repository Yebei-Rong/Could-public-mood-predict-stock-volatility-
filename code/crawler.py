# coding:utf-8

import requests
from bs4 import BeautifulSoup #解析网页库
import re
import pymysql

STOCK_LIST = [
              '000002',
              '000063',
              '000069',
              '000166',
              '000333',
              '000538',
              '000568',
              '000651',
              '000725',
              '000776',
              '000858',
              '000895',
              '001979',
              '002024',
              '002027',
              '002142',
              '002252',
              '002304',
              '002352',
              '002415',
              '002450',
              '002558',
              '002594',
              '002736',
              '300059',
              '600009',
              '600010',
              '600011',
              '600015',
              '600016',
              '600018',
              '600019',
              '600023',
              '600025',
              '600028',
              '600030',
              '600036',
              '600048',
              '600050',
              '600104',
              '600115',
              '600276',
              '600309',
              '600340',
              '600518',
              '600519',
              '600585',
              '600606',
              '600690',
              '600703',
              '600795',
              '600837',
              '600887',
              '600893',
              '600900',
              '600919',
              '600958',
              '600999',
              '601006',
              '601009',
              '601018',
              '601088',
              '601111',
              '601166',
              '601169',
              '601186',
              '601211',
              '601225',
              '601229',
              '601238',
              '601288',
              '601318',
              '601328',
              '601336',
              '601360',
              '601390',
              '601398',
              '601601',
              '601618',
              '601628',
              '601633',
              '601668',
              '601669',
              '601766',
              '601800',
              '601818',
              '601857',
              '601881',
              '601899',
              '601933',
              '601985',
              '601988',
              '601989',
              '601998',
              '603288',
              '603993',
              '601727',
              '600000',
              '601688']


def get_page_num(stock_id_list):

    stock_page_dict = {}

    for stock_id in stock_id_list:

        page = 1
        # 爬取的基本url形式
        stock_url = 'http://guba.eastmoney.com/list,{0}_{1}.html'.format(stock_id, page)
        # 获取网页源代码内容
        wbdata = requests.get(stock_url).content
        # 利用lxml解析网页
        soup = BeautifulSoup(wbdata, 'lxml')
        # pager info
        pager = soup.select("div#articlelistnew > div.pager > span")
        # list,股票代码_|总评论数|每页帖子数|
        data_pager = pager[0]['data-pager']
        # 总评论数
        i1 = data_pager.index('|')
        i2 = data_pager.index('|', i1+1)
        total_po = int(data_pager[i1+1:i2])
        # 总页数
        page_num = (total_po // 80) + 1

        stock_page_dict[stock_id] = page_num

    return stock_page_dict


# 获取各股的讨论内容，写入DB
def insert_post(stock_id, pages, cursor, conn):

    cnt = 0

    for i in range(1, pages + 1):
        po_url = 'http://guba.eastmoney.com/list,{0}_{1}.html'.format(stock_id, i)
        wbdata = requests.get(po_url).content
        soup = BeautifulSoup(wbdata, 'lxml')
        review_html = soup.select("div#articlelistnew > div.normal_post > span.l3 > a")
        review_date_html = soup.select("div#articlelistnew > div.normal_post > span.l6")

        for r, rd in zip(review_html, review_date_html):
            review = r['title']
            review = review.replace('\\', '')
            review = review.replace("'", '')

            review_date = rd.get_text()

            # print(review, review_date)

            cursor.execute("INSERT IGNORE INTO guba (stock_id, review, review_date) VALUES ('{0}', N'{1}', '{2}');".format(stock_id, review, review_date))
            conn.commit()
            cnt += 1

        if cnt % 1000 == 0:
            print('{0} records inserted'.format(cnt))


if __name__ == '__main__':

    # 获取目标股票代码（中证100指数)
    path = '/Users/rongyebei/Desktop/毕设/project/code'

    # stock_list = get_stock_list(path)

    # stock_page_dict = get_page_num(stock_list)

    conn = pymysql.connect(host='localhost', port=3306, user='root', password='password', db='stock')

    cursor = conn.cursor()

    '''
    crawler
    '''

    print('DB connected successfully')

    for stock_id in STOCK_LIST:
        # page = stock_page_dict[stock_id]
        print(stock_id)
        insert_post(stock_id, 400, cursor, conn)

    cursor.close()
    conn.close()

