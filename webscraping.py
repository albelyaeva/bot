import argparse
from values import *
from bs4 import BeautifulSoup
import requests
import json


KEY = 'AIzaSyDlF0CxkOWuPLn7d7L5fC9ZMQicHlVmBwY'
CX = '012341715563579400739:gepdcsp-wnm'


def scrapping(words):
    s = requests.Session()
    
    # get query words
    q = '+'.join(words)

    # create url
    url = 'https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&num={num}&q='.format(key=KEY, cx=CX,
                                                                                             num=NUM) + q
    # send request
    req = s.get(url, timeout=60000)

    # to json
    objects = json.loads(req.content)

    # get search queries
    items = objects['items']

    output = {}
    i = 1

    for item in items:
        result = {}

        # page link
        link = item['link']
        get_html = requests.get(link)

        #  use BeautifulSoup
        bs = BeautifulSoup(get_html.content, 'html.parser')

        # get h1 head
        if bs.h1:
            result['head'] = bs.h1.get_text()
        else:
            result['head'] = 'head'

        # title of the page
        if item['title']:
            result['title'] = item['title']
        else:
            result['title'] = 'title'

        # find page image
        img_find = bs.find(itemprop="image")
        if img_find['content']:
            result['img'] = img_find['content']
        elif bs.findAll('img'):
            image_tags = bs.findAll('img')
            print(image_tags)
            result['img'] = image_tags[0].get('src')
        else:
            result['img'] = None

        # find description
        meta_list = bs.find_all("meta")
        for meta in meta_list:
            if 'name' in meta.attrs:
                name = meta.attrs['name']
                if name in ATTRIBUTES:
                    result[name.lower()] = meta.attrs['content']
        output[i] = str(result)
        i += 1

    # output data
    with open('output.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(output, ensure_ascii=False))


parser = argparse.ArgumentParser(description='Key words')
parser.add_argument('-i', '--item', action='store', dest='alist',
                    type=str, nargs='*', default=['item1', 'item2', 'item3'],
                    help="Examples: -i item1 item2, -i item3")
args = parser.parse_args()

scrapping(args.alist)
