# -*- coding: utf-8 -*-
# @Time    : 2022/4/30 14:20
# @Author  : By_hui
# @File    : 1-京东-数据.py
# @Software: PyCharm
import math
import re
import time
import requests
import fake_useragent
from lxml import etree

# 请求头
headers = {
    'user-agent': fake_useragent.UserAgent().random,
}

# 获取一个商店所有商品id和标题
def get_shop_goods_id_title(shop_id:str):

    id_title_dt = {}
    # 商家id
    # shop_id = '1000004123'

    # 主页url
    home_url = f'https://mall.jd.com/index-{shop_id}.html'
    var_text_1 = requests.get(url=home_url, headers=headers).text

    global shop_name
    shop_name = etree.HTML(var_text_1).xpath('/html/head/title/text()')[0]

    print('-' * 20 + shop_name + '-' * 20 )

    pageInstance_appId = etree.HTML(var_text_1).xpath('//*[@id="pageInstance_appId"]/@value')[0]
    # 所有商品页
    all_goods_url = f'https://mall.jd.com/view_search-{pageInstance_appId}-0-99-1-24-1.html'
    var_text_2 = requests.get(url=all_goods_url, headers=headers).text

    # 获取 params 参数
    pageInstanceId = re.findall('value="(\d+)" id="pageInstance_id"',var_text_2)[0]
    moduleInstanceId = re.findall('m_render_instance_id="(\d+)" m_render', var_text_2)[0]
    templateId = re.findall('m_render_template_id="(\d+)" m_render_instance', var_text_2)[0]
    layoutInstanceId = re.findall('layout_instance_id="(\d+)" m_render_prototype', var_text_2)[0]
    prototypeId  = re.findall('m_render_prototype_id="(\d+)" m_render_template',var_text_2)[0]

    # 商品信息url --- 方法1
    good_info_url_1 = 'https://module-jshop.jd.com/module/getModuleHtml.html'
    params_1 = {
        'orderBy': 5,  # 排序
        'direction': 1,  # 编码
        'pageNo': 1,  # 页码
        # 'categoryId': 0,
        'pageSize': 24,
        # 'pagePrototypeId': 8,
        'pageInstanceId': pageInstanceId,
        'moduleInstanceId': moduleInstanceId,
        'prototypeId': prototypeId,
        'templateId': templateId,
        'appId': pageInstance_appId,
        'layoutInstanceId': layoutInstanceId,
        # 'origin': 0,
        'shopId': shop_id,
        'venderId': shop_id,

    }

    # 商品信息url --- 方法2
    good_info_url_2 = 'https://module-jshop.jd.com/module/allGoods/goods.html'
    params_2 = {
        'appId': pageInstance_appId,
        'pageInstanceId': pageInstanceId,
        'pageNo': 1,
        'direction': 1,
        'instanceId': moduleInstanceId,
        'modulePrototypeId': prototypeId,
        'moduleTemplateId': templateId,
    }

    page_num = 0 # 初始页码
    page_max = 1 # 初始页码最大值
    goods_num = 0 # 商品数量
    data_len = 0 # 数据长度
    while True:
        page_num += 1

        params_1['pageNo'] = page_num
        params_2['pageNo'] = page_num

        headers_module = {
            'user-agent': fake_useragent.UserAgent().random,
            'referer':'https://mall.jd.com/',
        }

        print('-' * 20 + f'开始第{page_num}页' + '-' * 20)

        if data_len == 0:
            module_text = requests.get(url=good_info_url_1, headers=headers_module, params=params_1).text
            id_ls = re.findall("jdprice='(\d+)'",module_text)
            title_ls = re.findall('html" target="_blank">((?!<).*?)</a>', module_text)

            if title_ls == []:
                data_len = 20
                page_num = 0 # 页码重置
                print('正在使用第二种方法......')
        else:
            module_text = requests.get(url=good_info_url_2, headers=headers_module, params=params_2).text
            # print(module_text)
            id_ls = re.findall("jdprice='(\d+)'", module_text)
            title_ls = re.findall('html" target="_blank" title="(.*?)">', module_text)



        for i, j in zip(id_ls,title_ls):
            goods_num += 1
            print(goods_num,i,j)

        if page_num == 1:
            # 商品总数
            all_goods_num = ''.join(re.findall('J_resCount">(\d+)</span>件商品|共(\d+)条记录', module_text)[0])
            # 最大页码
            page_max = int(math.ceil(int(all_goods_num)/len(id_ls)))

        id_title_dt.update(dict(zip(id_ls, title_ls))) # 更新数据

        if page_num == page_max:
            print('-' * 20 + f'结束!共{page_max}页,{len(id_title_dt)}条数据!!!' + '-' * 20)
            break
        else:
            time.sleep(2)

    return id_title_dt


# 商品评论获取 一次一个
def get_goods_evaluat(productId: str):
    id_evaluat_dt = {}  # 保存评价信息

    url = 'https://club.jd.com/comment/skuProductPageComments.action'
    headers = {
        'user-agent': fake_useragent.UserAgent().random,  # 随机UA
    }
    params = {
        'productId': productId,
        'score': 0,  # 0全部评价 1差评，2中评 3好评 4晒图  5追评  7视频晒单
        'sortType': 5,
        'page': 0,  # 页码
        'pageSize': 10,  # 10个评论
    }

    # 请求数据
    try:
        page_json = requests.get(url=url, headers=headers, params=params).json()
    except:
        page_json = requests.get(url=url, headers=headers, params=params).text
        print(page_json)
        page_json = {}
        print('ip 可能被封!!!')

    # 评论内容
    comment_ls = []
    for i in page_json['comments']:
        goods_id = i['id']
        guid = i['guid']
        content = i['content']

        comment_ls.append([goods_id, guid, content])

    # 评论数
    data = page_json["productCommentSummary"]
    goods_id = str(data['productId'])
    CommentCount = data['commentCountStr']  # 总评价数
    GoodCount = data['goodCountStr']  # 好评数
    AfterCount = data['afterCountStr']  # 追评
    GoodRateShow = str(data['goodRateShow']) + '%'  # 好评度
    GeneralCount = data['poorCountStr']  # 差评

    id_evaluat_dt[goods_id] = [CommentCount, GoodCount, AfterCount, GoodRateShow, GeneralCount, comment_ls]  # 加入字典

    return id_evaluat_dt


# 获取商品价格一次多个
def get_goods_price(skuids: list):

    id_price_dt = {}

    once_num = 20 # 一次20个
    id_len = len(skuids)
    couple = int(math.ceil(int(id_len/once_num))) # 分成几段

    all_id_ls = []

    if id_len > once_num:
        for i in range(couple):
            all_id_ls.append(skuids[0+once_num*i:20+once_num*i])
    else:
        all_id_ls = [skuids]


    url = 'https://f-mall.jd.com/prices/mgets'
    headers = {
        'user-agent': fake_useragent.UserAgent().random,
    }

    for id_ls in all_id_ls:

        params = {
            'skuids': ','.join(['J_' + i for i in id_ls]),
        }

        # 请求数据
        page_json = requests.get(url=url, headers=headers, params=params).json()
        # print(page_json)
        # page_json = [{'p': '103.00', 'op': '497.00', 'm': '994.00', 'cbf': 0, 'id': 'J_10022383735844', 'tpp': '97.00', 'up': '2'}, {'p': '258.00', 'op': '258.00', 'm': '1150.00', 'cbf': 0, 'id': 'J_10043609106706'}]

        for price_dt, id in zip(page_json, id_ls):
            price = price_dt['p']  # 现价

            if 'tpp' in price_dt:
                price_vip = price_dt['tpp']  # 会员价
            else:
                price_vip = price
            price_max = price_dt['m']  # 最高价

            id_price_dt[id] = [price, price_vip, price_max]

    # print(id_price_dt)
    return id_price_dt

# evaluat_switch == Ture 开启评论爬取
def main(evaluat_switch=False):
    # 商家id
    # shop_id = '10739135'
    shop_id = input('请输入商家id：')
    id_title_dt = get_shop_goods_id_title(shop_id=shop_id)
    # 取出所有id
    id_ls = list(id_title_dt.keys())
    # 获取商品价格
    id_price_dt = get_goods_price(id_ls)

    price_text_ls = ['现价', '会员价', '最高价']
    evaluat_text_ls = ['总评价数', '好评数', '追评', '好评度', '差评', '评论内容']

    print('-' * 20 + shop_name + '-' * 20)

    # 商品评论获取
    for ID in id_ls:
        if evaluat_switch == False:
            id_evaluat_dt = dict(zip(evaluat_text_ls,list(range(len(evaluat_text_ls)))))
        else:
            id_evaluat_dt = get_goods_evaluat(ID)

        # time.sleep(3) # 注意减速易封ip

        print(f'''

            序号:{id_ls.index(ID)}      id:{ID},    url: https://item.jd.com/{ID}.html
            标题:{id_title_dt[ID]}
            价格:{[f'{text}:{price}' for text, price in zip(price_text_ls, id_price_dt[ID])]}

            ''')

        # 有评论------------------------------------------------------------------------------------
        # print(f'''
        #
        #     序号:{id_ls.index(ID)}      id:{ID},    url: https://item.jd.com/{ID}.html
        #     标题:{id_title_dt[ID]}
        #     价格:{[f'{text}:{price}' for text, price in zip(price_text_ls, id_price_dt[ID])]}
        #     评论:{[f'{text}:{evaluat}' for text, evaluat in zip(evaluat_text_ls, id_evaluat_dt[ID])]}
        #
        #     ''')

# 搜索爬虫
def search_goods(key,page_num=1):

    url = 'https://search.jd.com/Search?'

    headers = {
        'user-agent':fake_useragent.UserAgent().random,
        'cookie':'__jdu=1644919025313704760977; shshshfpa=ae080e7a-325d-150d-cb01-96f50d7ae0a9-1644919026; shshshfpb=kLSF1wK6giaG05VBKhmZImA; rkv=1.0; qrsc=3; __jdv=122270672|direct|-|none|-|1650892764169; TrackID=1bha6YZiAC0fjlVB2MvxL_EMpG4Gnvk9Rhs6ZvvJX94Ih158BHQnKqyqW_lFX1wU_uQ-a2B-DjUT13wovjQKamwvRAGFMbPydBSX3ExnlMQWtV528pkpmSAqU2c0T9nKs; pinId=qUWBY6CQOHPmOjznu3dbNLV9-x-f3wj7; pin=jd_494a0abca1f30; unick=%E6%B2%A1%E9%92%B1%E8%AE%A4%E5%91%BDsix; ceshi3.com=103; _tp=znKc1VSrW8C6dLj%2FU6fkYDvKpWuSg%2F2AWIyki%2F5TH%2BA%3D; _pst=jd_494a0abca1f30; user-key=1b41c47b-3750-48cf-bdb7-3e7004af61d1; cn=7; ipLoc-djd=1-72-55653-0; areaId=1; PCSYCityID=CN_420000_420100_0; mt_xid=V2_52007VwMVV1hQUlIeSh1eBWUFE1dbX1NSGU8pWA1nA0EHVFBOWE1BEUAAY1ATTg1YUAkDQR8IVWAEGgdbXFRTL0oYXwZ7AhdOXl5DWR1CHFgOZQciUG1YYl0bSRxUAGcGEVFtWFReGw%3D%3D; __jdc=122270672; shshshfp=eeb237fdf161fdd8d45583959685946f; joyya=1651164848.1651164853.21.1q7s5i2; ip_cityCode=1381; __jda=122270672.1644919025313704760977.1644919025.1651320751.1651326569.35; wlfstk_smdl=zefjltksdlprtunvtq8tl9rk0q6ggctg; thor=C249DDCD2AC63AB8341576E29300D9B9A2F27A02EE257C6A80AA57841E3AA790D2162966132B1145E2F7E7BD9BC25BA8CC65AD02776D96FDCBC468DF9F6900B0717E8EAF7C8447BDC69CCEA6A0C9AA91DFDED44577DECF59ECDA7E84AD25AE48866F423D3DB89883179727E3FDF74EC418025AFF2046CD5076C0F91B60842568359E8B6BED78452347977F375DF446380A851C6DA593DA92CBCD5C490D0D77AD; __jdb=122270672.6.1644919025313704760977|35.1651326569; shshshsID=2a3b7517b58176da10140c365ac40828_3_1651326619422; 3AB9D23F7A4B3C9B=HYXSMYTQYQHTHTMHJDIFFBUVOOSMDMSEZLMR7VVPXRV5HC3RTVGYBS75LEVMK5EZJGSWD6KTDAPVF4LGKSB55LA5QM',
    }

    params = {

        'keyword': key,
        'qrst': 1,
        'wq': key,
        'stock': 1,
        'page': page_num,

    }
    # 请求源码
    page_text = requests.get(url=url, headers=headers, params=params).text
    # with open(r'C:\Users\by-hui\Desktop\1\1.html','r',encoding='utf-8') as fp:
    #     # fp.write(page_text)
    #     page_text = fp.read()
    # print(page_text)
    tree = etree.HTML(page_text)
    li_ls = tree.xpath('//*[@id="J_goodsList"]/ul/li')
    for li in li_ls:
        goods_id = li.xpath('./@data-sku')[0] # 商品id
        goods_title = li.xpath('./div/div[3]/a/em/text()') # 商品标题
        goods_price = li.xpath('./div/div[2]/strong/i/text()') # 高品价格
        goods_shop = li.xpath('./div/div[5]/span/a/text()') # 所在商家
        print(goods_id,goods_title,goods_price,goods_shop)

def run_search_goods():
    key = input('请输入关键字：')
    page_num = int(input('爬取的页数：'))

    for i in range(1,page_num+1):
        print('-'*30+f'开始第{i}页'+'-'*30)
        search_goods(key=key,page_num=i)
        time.sleep(3)

    print('-'*30+'完毕!!!'+'-'*30)
    ...


if __name__ == '__main__':
    run_search_goods()
