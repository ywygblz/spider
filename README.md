# 爬虫
基于python开发的爬虫

# 免责声明：此代码仅学习使用，请勿用于商业用途，如拿去非法使用与本人无关！

# 目录

1. [spider -- 京东](https://github.com/ywygblz/spider/blob/main/README.md#%E4%B8%80spider----京东)
2. [spider -- 天眼查滑动验证码](https://github.com/ywygblz/spider/blob/main/README.md#%E4%B8%80spider----天眼查滑动验证码)


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
