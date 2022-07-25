import os
import re
import requests
from lxml import etree

key = '宫崎骏'
start_num = 20

url = f'https://search.douban.com/book/subject_search?search_text={key}&start={start_num}'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

page_text = requests.get(url=url,headers=headers).text

# with open('page.html', 'r', encoding='utf-8') as fp:
#     page_text = fp.read()

cryptograph_text = etree.HTML(page_text).xpath('/html/body/script[6]/text()')[0]
cryptograph = re.findall('"(.*?)"', cryptograph_text)[0]
one_line = f"let text = '{cryptograph}'"


# print(one_line)


def get_data(one_line):
    with open('豆瓣逆向--.js', 'r', encoding='gbk') as f:
        text_ls = f.readlines()
        text_ls[0] = one_line
        # print(text_ls)
    with open('豆瓣逆向--2.js', 'w', encoding='utf-8') as f:
        for i in text_ls:
            f.write(i)

    os.system('node 豆瓣逆向--2.js > arr.txt')
    data = open('arr.txt', 'r', encoding='utf-8').read()
    data = f'let arr = {data}'

    with open('规范化--.js', 'r', encoding='utf-8') as f:
        text_ls = f.readlines()
        text_ls[0] = data
        # print(text_ls)
    with open('规范化--2.js', 'w', encoding='utf-8') as f:
        for i in text_ls:
            f.write(i)
    os.system('node 规范化--2.js > new_arr.txt')
    with open('new_arr.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        text = re.sub('null', '"null"', text)
    books = eval(text)
    return books


data = get_data(one_line)
key_word = data["text"]
total = data["total"]  # 书藉数量
count = data["count"]  # 本次数量
items = data["items"]
print(key_word,total,count)
for item in items:
    Id = item["id"]
    title = item["title"]
    url = item["url"]
    # cover_url = item["cover_url"]  # 图url
    abstract = item["abstract"]  # 收藏
    print(Id, title, url, abstract)
# print(data)
