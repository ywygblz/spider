import os
import time

import requests

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
    'referer': 'https://music.163.com/song?id=208891',
}

'''
var params = {
    csrf_token: "",
    cursor: arguments[2],
    offset: "0",
    orderType: "1",
    pageNo: arguments[3],
    pageSize: arguments[4],
    rid: arguments[5],
    threadId: arguments[6],
}, 
'''

cursor = round(time.time() * 1000)

song_id = 1346104327

pageNo = '1'
pageSize = '20'
rid = f'R_SO_4_{song_id}'
threadId = rid
s = os.popen(f'node jiami.js {cursor} {pageNo} {pageSize} {rid} {threadId}').readlines()
data = {
    'params': s[1].replace("  params: '", '').replace("',\n", ''),
    'encSecKey': s[2].replace("  encSecKey: '", '').replace("'\n", ''),
}
json_data = requests.post(url=url, headers=headers, data=data).json()
for key in ['hotComments', 'comments']:
    if key == 'hotComments':
        continue
    totalCount = json_data['data']['totalCount']  # 总评论数
    print('*' * 20, f'总评价数：{totalCount}', '*' * 20)
    print(['热门评价', '最新评价'][['hotComments', 'comments'].index(key)], '-' * 30)
    for item in json_data['data'][key]:
        num = json_data['data'][key].index(item) + 1
        userId = item['user']['userId']  # 用户ud
        nickname = item['user']['nickname']  # 用户昵称
        commentId = item['commentId']  # 评论id
        content = item['content']  # 评论内容
        likedCount = item['likedCount']
        timestamp = item['time']  # 时间戳
        time_array = time.localtime(timestamp / 1000)
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_array)
        info = f'{num} 用户名id：{userId} 用户名：{nickname}\n评论id：{commentId} 点赞数：{likedCount} 时间：{time_str}\n评论内容：{content}'
        print(info)
