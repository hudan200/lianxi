import requests,json,re
from requests.exceptions import RequestException

def get_one_page(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
    }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_page(html):
    pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)</a>.*?name">(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
                        'index': item[0],
                        'image': item[1],
                        'title': item[2],
                        'actor': item[3].strip()[3:],
                        'time': item[4].strip()[5:],
                        'score': item[5] + item[6]
                                  }

def save_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main():
    for i in range(10):
        html = get_one_page(i*10)
        for item in parse_page(html):
            print(item)
            save_file(item)

if __name__ == '__main__':
    main()