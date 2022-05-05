# -*- coding: utf-8 -*-
# @Time    : 2022/5/4 14:00
# @Author  : By_hui
# @File    : lianjia_new_data_get.py
# @Software: PyCharm

import requests
import fake_useragent
from lxml import etree
from time import sleep
import math
import pymysql

# 连接数据库
by_hui = pymysql.connect(host='127.0.0.1',user='root',password='root',database='by_hui')
cursor = by_hui.cursor() # 游标

headers = {
    'user-agent':fake_useragent.UserAgent().random,
}
# 武汉所有区url
all_url_dt = {
            '江岸': {'百步亭': 'https://wh.lianjia.com/ershoufang/baibuting/', '大智路': 'https://wh.lianjia.com/ershoufang/dazhilu/',
                    '堤角': 'https://wh.lianjia.com/ershoufang/dijiao/', '二七': 'https://wh.lianjia.com/ershoufang/erqi2/',
                    '后湖': 'https://wh.lianjia.com/ershoufang/houhu/',
                    '黄埔永清': 'https://wh.lianjia.com/ershoufang/huangpuyongqing/',
                    '三阳路': 'https://wh.lianjia.com/ershoufang/sanyanglu/', '育才花桥': 'https://wh.lianjia.com/ershoufang/yucaihuaqiao/'},
            '江汉': {'长港路': 'https://wh.lianjia.com/ershoufang/changganglu/', '常青路': 'https://wh.lianjia.com/ershoufang/changqinglu/',
                    '前进江汉': 'https://wh.lianjia.com/ershoufang/qianjinjianghan/', '台北香港路': 'https://wh.lianjia.com/ershoufang/taibeixiangganglu/',
                    '唐家墩': 'https://wh.lianjia.com/ershoufang/tangjiadun/', '塔子湖': 'https://wh.lianjia.com/ershoufang/tazihu/',
                    '新华路万达': 'https://wh.lianjia.com/ershoufang/xinhualuwanda/', '杨汊湖': 'https://wh.lianjia.com/ershoufang/yangchahu/'},
            '硚口': {'宝丰崇仁': 'https://wh.lianjia.com/ershoufang/baofengchongren/', 'CBD西北湖': 'https://wh.lianjia.com/ershoufang/cbdxibeihu/',
                    '长丰常码头': 'https://wh.lianjia.com/ershoufang/changfengchangmatou/', '古田': 'https://wh.lianjia.com/ershoufang/gutian/',
                    '汉正街': 'https://wh.lianjia.com/ershoufang/hanzhengjie/', '集贤': 'https://wh.lianjia.com/ershoufang/jixian2/',
                    '武广万松园': 'https://wh.lianjia.com/ershoufang/wuguangwansongyuan/', '宗关': 'https://wh.lianjia.com/ershoufang/zongguan/'},
            '东西湖': {
                    '常青花园': 'https://wh.lianjia.com/ershoufang/changqinghuayuan/', '东西湖其它': 'https://wh.lianjia.com/ershoufang/dongxihuqita/',
                    '将军路': 'https://wh.lianjia.com/ershoufang/jiangjunlu/', '金银湖': 'https://wh.lianjia.com/ershoufang/jinyinhu/',
                    '吴家山': 'https://wh.lianjia.com/ershoufang/wujiashan/'},
            '武昌': {
                    '楚河汉街': 'https://wh.lianjia.com/ershoufang/chuhehanjie/',  '积玉桥': 'https://wh.lianjia.com/ershoufang/jiyuqiao/',
                    '首义': 'https://wh.lianjia.com/ershoufang/shouyi/',
                    '水果湖': 'https://wh.lianjia.com/ershoufang/shuiguohu/',
                    '武昌火车站': 'https://wh.lianjia.com/ershoufang/wuchanghuochezhan/', '中北路': 'https://wh.lianjia.com/ershoufang/zhongbeilu/'},
            '青山': {'青山': 'https://wh.lianjia.com/ershoufang/qingshan1/'},
            '洪山': {'白沙洲': 'https://wh.lianjia.com/ershoufang/baishazhou/', '东湖东亭': 'https://wh.lianjia.com/ershoufang/donghudongting/',
                    '虎泉杨家湾': 'https://wh.lianjia.com/ershoufang/huquanyangjiawan/', '街道口': 'https://wh.lianjia.com/ershoufang/jiedaokou/',
                    '老南湖': 'https://wh.lianjia.com/ershoufang/laonanhu/', '珞狮南路': 'https://wh.lianjia.com/ershoufang/luoshinanlu/',
                    '南湖沃尔玛': 'https://wh.lianjia.com/ershoufang/nanhuwoerma/',
                    '沙湖': 'https://wh.lianjia.com/ershoufang/shahu/', '团结大道': 'https://wh.lianjia.com/ershoufang/tuanjiedadao/',
                    '新南湖': 'https://wh.lianjia.com/ershoufang/xinnanhu/', '徐东': 'https://wh.lianjia.com/ershoufang/xudong/',
                    '杨园': 'https://wh.lianjia.com/ershoufang/yangyuan/', '中南丁字桥': 'https://wh.lianjia.com/ershoufang/zhongnandingziqiao/',
                    '卓刀泉': 'https://wh.lianjia.com/ershoufang/zhuodaoquan/'},
            '汉阳': {'七里庙': 'https://wh.lianjia.com/ershoufang/qilimiao/', '四新': 'https://wh.lianjia.com/ershoufang/sixin/',
                    '钟家村': 'https://wh.lianjia.com/ershoufang/zhongjiacun/'},
            '东湖高新': {'光谷东': 'https://wh.lianjia.com/ershoufang/guanggudong/', '光谷广场': 'https://wh.lianjia.com/ershoufang/guangguguangchang/',
                    '关山大道': 'https://wh.lianjia.com/ershoufang/guanshandadao/', '关西长职': 'https://wh.lianjia.com/ershoufang/guanxichangzhi/',
                    '洪山其它': 'https://wh.lianjia.com/ershoufang/hongshanqita/', '华科大': 'https://wh.lianjia.com/ershoufang/huakeda/',
                    '民族大道': 'https://wh.lianjia.com/ershoufang/minzudadao/', '三环南': 'https://wh.lianjia.com/ershoufang/sanhuannan/'},
            '江夏': {'藏龙岛': 'https://wh.lianjia.com/ershoufang/canglongdao/', '光谷南': 'https://wh.lianjia.com/ershoufang/guanggunan/',
                    '黄家湖': 'https://wh.lianjia.com/ershoufang/huangjiahu1/', '江夏其它': 'https://wh.lianjia.com/ershoufang/jiangxiaqita/',
                    '金融港': 'https://wh.lianjia.com/ershoufang/jinronggang/', '庙山': 'https://wh.lianjia.com/ershoufang/miaoshan/',
                    '文化大道': 'https://wh.lianjia.com/ershoufang/wenhuadadao/', '纸坊': 'https://wh.lianjia.com/ershoufang/zhifang/'},
            '蔡甸': {'蔡甸城区': 'https://wh.lianjia.com/ershoufang/caidianchengqu/', '后官湖': 'https://wh.lianjia.com/ershoufang/houguanhu/',
                    '中法生态城': 'https://wh.lianjia.com/ershoufang/zhongfashengtaicheng/'},
            '黄陂': {'汉口北': 'https://wh.lianjia.com/ershoufang/hankoubei/', '横店街': 'https://wh.lianjia.com/ershoufang/hengdianjie/',
                    '黄陂其它': 'https://wh.lianjia.com/ershoufang/huangbeiqita/', '盘龙城': 'https://wh.lianjia.com/ershoufang/panlongcheng/',
                    '前川': 'https://wh.lianjia.com/ershoufang/qianchuan/', '武湖': 'https://wh.lianjia.com/ershoufang/wuhu/'},
            '新洲': {'新洲其它': 'https://wh.lianjia.com/ershoufang/xinzhouqita/', '阳逻': 'https://wh.lianjia.com/ershoufang/yangluo/'},
            '沌口开发区': {'沌口': 'https://wh.lianjia.com/ershoufang/dunkou/', '王家湾': 'https://wh.lianjia.com/ershoufang/wangjiawan/'},
            '汉南': {'蔡甸其它': 'https://wh.lianjia.com/ershoufang/caidianqita/', '汉南其它': 'https://wh.lianjia.com/ershoufang/hannanqita/'}}


def get_data_ls(url_prefix,district):

    page_num = 1 # 当前页码
    page_max = page_num # 总页码
    property_num = 0 # 房源数
    default_page = page_num # 初始页码

    while True:

        print('-'*30 + f'准备开始{district}第{page_num}页' + '-'*30)
        sleep(3)
        url = f'{url_prefix}pg{page_num}/'
        page_text = requests.get(url=url,headers=headers).text
        # print(page_text)
        tree = etree.HTML(page_text)
        li_ls = tree.xpath('//*[@class="sellListContent"]/li')

        if li_ls == []:
            li_ls = tree.xpath('//*[@class="sellListContent LOGCLICKDATA LOGVIEWDATA"]/li')

        # 第一次获取总页码数
        if page_num == default_page:
            try:
                sum_num = tree.xpath('//h2[@class="total fl"]/span/text()')[0].replace(' ','') # 总房数
                page_max = int(math.ceil(int(sum_num)/30)) # 总页数
            except:
                page_max = default_page

        for li in li_ls:
            title = li.xpath('./div/div[2]/div/a/text()')  # 位置
            # if title == []: # 清除广告信息
            #     continue
            url_id = li.xpath('./a/@data-housecode | @data-lj_action_housedel_id')[0]
            title = '-'.join(title).replace(' ', '')
            price = li.xpath('./div/div[6]/div[2]/@data-price')[0] + '平/元'  # 平/元
            money = li.xpath('./div/div[6]/div[1]/span/text()')[0] + '万元' # 钱 万
            message = [i.replace(' ','') for i in li.xpath('./div/div[3]/div/text()')[0].split('|')]  # 信息
            data_ls = [url_id,title,price,money] + message # ['104107228878', '温馨苑AB区-百步亭', '15937平/元', '136万元', '2室2厅', '85.34平米', '南', '精装', '中楼层(共7层)', '2005年建', '板楼']
            property_num += 1  # 数据量

            print(data_ls)

            # 100条保存一次
            if property_num % 100 == 0:
                save_judge = True
            else:
                save_judge = False
            # 写入数据库
            write_sql(data_ls=data_ls, district=district, save_judge=save_judge)

        if page_num == page_max:
            print(f'完毕!!!,{district}共有{property_num}套房源')


            break

        page_num += 1 # 翻页


def write_sql(data_ls:list,district:str,save_judge=False):
    # 读数据
    # cursor.execute('select * from lianjia_wh_used where id < 100')
    # data = cursor.fetchall() # 读数据
    # print(data)
    # cursor.execute('')
    # l = ['104108461629', '江岸', '海赋江城天韵-百步亭', '88.68平米', '225万元', '25373元/平', '2室2厅', '南', '精装', '低楼层(共34层)', '2016年建', '板塔结合']
    data_ls.insert(1,district) # 加入区
    while len(data_ls) < 13:
        data_ls.append('null') # 没有13位的补齐位数
    com = "insert into lianjia_wh_used_2 values(0,'" + "','".join(data_ls) + "');"


    # 出错回滚
    try:
        cursor.execute(com) # 写入数据
    except Exception as E:
        print('出错:',E,'\ncom')

    if save_judge == True:
        by_hui.commit() # 保存

if __name__ == '__main__':

    for district in all_url_dt:
        for key in all_url_dt[district]:
            print(district,key,all_url_dt[district][key])

    district = '黄陂'
    key = '前川'
    url_prefix = all_url_dt[district][key]

    try:
        get_data_ls(url_prefix=url_prefix, district=district)
    except Exception as E:
        print('ip可能被封了')

    by_hui.commit()
    by_hui.close()
    ...