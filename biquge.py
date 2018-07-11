# -*- coding:utf-8 -*-
import requests,re
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def get_page_index():
    url = 'http://www.biquge.com.tw/0_213/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.encode('iso-8859-1').decode('gbk')
        return None
    except RequestException:
        return None

def get_url(html):
    pattern = re.compile('<dd><a href="(.*?)">', re.S)
    results = re.findall(pattern, html)
    for result in results[:-10]:
        url =  'http://www.biquge.com.tw' + result
        response = requests.get(url)
        html = response.text.encode('iso-8859-1').decode('gbk')
        soup = BeautifulSoup(html, 'lxml')
        titles = soup.select('.bookname h1')
        neirongs = soup.select('#content')
        title = titles[0].text
        neirong = neirongs[0].text
        with open('/Users/zmh/Desktop/content.txt', 'a', encoding='utf-8') as f:
            f.write(title + '\n')
            f.write(neirong)
            f.close()

def main():
    html = get_page_index()
    get_url(html)

if __name__ == '__main__':
    main()