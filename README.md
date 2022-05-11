# 爬虫
基于python开发的爬虫
交流学习 

学习交流qq：1874369378

# 免责声明：此代码仅学习使用，请勿用于商业用途，如拿去非法使用与本人无关！

# 目录

1. [spider -- 京东](https://github.com/ywygblz/spider/blob/main/README.md#%E4%B8%80spider----京东)
2. [spider -- 天眼查滑动验证码](https://github.com/ywygblz/spider/blob/main/README.md#%E4%BA%8Cspider----天眼查滑动验证码)
3. [spider -- 链家二手房源爬取存入mysql数据库](#%E4%B8%89spider----链家二手房源爬取存入mysql数据库)


# [一、spider -- 京东](https://github.com/ywygblz/spider/tree/main/1-%E4%BA%AC%E4%B8%9C)

### 1、通过商家id爬取商品数据及评论

> 运行main()开始爬取

> 传入evaluat_switch=False，可开启爬取评论

### 2、通过关键字爬取商品数据及评论

>  运行run_search_goods()开始爬取

> 获取id后可值传入get_goods_evaluat(productId: str)函数获取评论

![爬虫图片](https://github.com/ywygblz/spider/blob/main/1-%E4%BA%AC%E4%B8%9C/images/%E4%BA%AC%E4%B8%9C%E7%88%AC%E8%99%AB%E5%9B%BE%E4%BE%8B.png)

# [二、spider -- 天眼查滑动验证码](https://github.com/ywygblz/spider/tree/main/2-%E5%A4%A9%E7%9C%BC%E6%9F%A5%E6%BB%91%E5%8A%A8%E9%AA%8C%E8%AF%81%E7%A0%81)

## 基于自动化测试功具selenium及cv2中的模版对比实现滑动验证码破解

## 需要提前安装selenium自动化测试环境及chromedriver 下载

### 实现效果

![实现效果](https://github.com/ywygblz/spider/blob/main/2-%E5%A4%A9%E7%9C%BC%E6%9F%A5%E6%BB%91%E5%8A%A8%E9%AA%8C%E8%AF%81%E7%A0%81/%E6%BB%91%E5%8A%A8%E9%AA%8C%E8%AF%81%E7%A0%81%E7%A0%B4%E8%A7%A3_.gif)

# [三、spider -- 链家二手房源爬取存入mysql数据库](/3-%E9%93%BE%E5%AE%B6/)

## 1.以 湖北武汉 为例，先拿到所有区的名字和url

如下图（只显示部分）
![到所有区的名字和url](/3-%E9%93%BE%E5%AE%B6/%E6%AD%A6%E6%B1%89%E6%89%80%E6%9C%89%E5%8C%BA%E5%90%8D%E7%A7%B0%E5%92%8Curl.png)

## 2.新建数据表
```MySql
/*
['104108454851', '中建文华星城-文化大道', '113.03平米', '158万元', '13978元/平', '3室2厅', '南北', '简装', '高楼层(共34层)', '2016年建', '板塔结合']
*/
create table lianjia_wh_used_2(
id int primary key not null auto_increment,
url_id varchar(15) not null,
region varchar(5) not null,
name varchar(20) not null,
area varchar(10),
money varchar(7),
price varchar(10),
trait_1 varchar(10),
trait_2 varchar(10),
trait_3 varchar(10),
trait_4 varchar(10),
trait_5 varchar(10),
trait_6 varchar(10),
trait_7 varchar(10)
);
```


## 3.运行get_data_ls方法即可
```Python
url_prefix = 'https://wh.lianjia.com/ershoufang/baibuting/'
district = '江岸'
get_data_ls(url_prefix=url_prefix, district=district)
```

## 4.数据分析
房源数据（10万条中的部分）
!['房源数据'](/3-%E9%93%BE%E5%AE%B6/%E6%88%BF%E6%BA%90%E6%95%B0%E6%8D%AE.png)

### [1.直方图(点击查看)](https://ywygblz.github.io/spider/3-链家/数据图/1-直方图.html)<br>
[![](3-链家/数据图/1-直方图.png)](https://ywygblz.github.io/spider/3-链家/数据图/1-直方图.html)<br>
### [2.直方图(点击查看)](https://ywygblz.github.io/spider/3-链家/数据图/2-圆饼图.html)<br>
[![](3-链家/数据图/2-圆饼图.png)](https://ywygblz.github.io/spider/3-链家/数据图/2-圆饼图.html)<br>
### [3.折线图(点击查看)](https://ywygblz.github.io/spider/3-链家/数据图/3-折线图.html)<br>
[![](3-链家/数据图/3-折线图.png)](https://ywygblz.github.io/spider/3-链家/数据图/3-折线图.html)<br>
### [4.词云图(点击查看)](https://ywygblz.github.io/spider/3-链家/数据图/4-词云图.html)<br>
[![](3-链家/数据图/4-词云图.png)](https://ywygblz.github.io/spider/3-链家/数据图/4-词云图.html)<br>
### [5.武汉市地图(点击查看)](https://ywygblz.github.io/spider/3-链家/数据图/5-武汉市地图.html)<br>
[![](3-链家/数据图/5-武汉市地图.png)](https://ywygblz.github.io/spider/3-链家/数据图/5-武汉市地图.html)<br>
### [6.大屏展示图(点击查看)](https://ywygblz.github.io/spider/3-链家/数据图/6-大屏展示图.html)<br>
[![](3-链家/数据图/6-大屏展示图.png)](https://ywygblz.github.io/spider/3-链家/数据图/6-大屏展示图.html)<br>
