import cv2
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import fake_useragent
from lxml import etree
from time import sleep

# 获取移动位置
def get_move_x():
    template = cv2.imread(kuai_img_path, 0)
    backdrop = cv2.imread(bj_img_path, 0)

    h, w = template.shape[:2]
    res = cv2.matchTemplate(backdrop, template, cv2.TM_CCORR_NORMED)
    # 获取最大值,最小值,图像位置最大值最小值
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val, max_val, min_loc, max_loc)

    # 绘制区域
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(backdrop, top_left, bottom_right, 1, 1)

    return min_loc[0]


url = r'https://www.tianyancha.com/advance/search/e-pc_homesearch'

# chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
bro = webdriver.Chrome()
bro.get(url)
sleep(2)
bro.maximize_window()
sleep(1)


# 选地区
bro.find_element(By.ID,'cascader_area').click()
js_com_box = 'document.getElementsByClassName("cascader-panel")[1].style="height: 700px;"'
bro.execute_script(js_com_box)
sleep(1)
bro.find_element(By.XPATH,'//*[@id="cascader_area"]/div/div[1]/div[1]/ul/li[17]/span').click()
bro.find_element(By.XPATH,'//*[@id="cascader_area"]/div/div[1]/div[2]/ul/li[1]/label/span').click()
bro.find_elements(By.XPATH,'//*[@class="float-left button button-primary"]')[1].click()
# 加大可视区域
js_com_scroll_Top = 'document.documentElement.scrollTop = 700'
bro.execute_script(js_com_scroll_Top)

# 点登陆、注册
js_com_login_link = 'header.loginLink(event)'
# 切换登陆方式
js_com_login_way = 'loginObj.toggleQrcodeAndPwd()'
# 切换帐号密码登陆
js_com_user_pwd = 'loginObj.changeCurrent(1)'
for i in [js_com_login_link,js_com_login_way,js_com_user_pwd]:
    bro.execute_script(i)
    sleep(1)

user = '帐号'
pwd = '密码'
bro.find_element(By.ID,'mobile').send_keys(user)
bro.find_element(By.ID,'password').send_keys(pwd)
js_com_login = 'loginObj.loginByPhone(event)'
bro.execute_script(js_com_login) # 点登陆
sleep(2)
# 删前景
js_com_rm_foreground = "document.getElementsByClassName('gt_cut_fullbg gt_show')[0].remove()"
bro.execute_script(js_com_rm_foreground)

kuai_img_path = r"C:\Users\by-hui\Desktop\1\kuai.png"
bj_img_path = r"C:\Users\by-hui\Desktop\1\bj.png"
# 滑块图
slider_img = bro.find_element(By.XPATH,'//div[@class="gt_slice gt_show"]')
slider_img.screenshot(kuai_img_path)

# 背景
bj = bro.find_element(By.XPATH,'//*[@class="gt_fullbg gt_show"]').screenshot(bj_img_path)

# 滑块处理动做链
slider = bro.find_element(By.XPATH,'//*[@class="gt_slider_knob gt_show"]')
action = ActionChains(bro)
action.move_to_element(slider).perform()
action.click_and_hold().perform()
action.move_by_offset(xoffset=get_move_x(),yoffset=0).perform()
sleep(3)
action.release().perform()


sleep(2)
# 点查找
js_com_find = 'verifyUserStatus(this)'
bro.execute_script(js_com_find)

cookie = bro.get_cookies()
cookie_dt = {}
for i in cookie:  # 整合cookie
    for key in i:
        cookie_dt[key] = i[key]
print(cookie_dt)


# 会员的高级查找功能下爬取
url = 'https://www.tianyancha.com/advance/search/result?eventPrefix=pc_homesearch'
headers = {
    'user-agent':fake_useragent.UserAgent().random, # 随机请求头
    'Referer':'https://www.tianyancha.com/advance/search/e-pc_homesearch',
    # 'cookie':'自己会员的cookie或者上面的cookie_dt',
}
data = {
    'xyz': 'Ix5c38-ndpBcksHHlQp1EP1k',
    'customAreaCodeSet':'00420100V2020',
    'pageNum': '1',
    'pageSize': 20,
    'resultTagList': '地区：湖北省',
}
page_text = requests.post(url=url,headers=headers,data=data,cookies=cookie_dt).text
tree = etree.HTML(page_text)
div_ls = tree.xpath('//*[@class="result-list sv-search-container"]/div')
for div in div_ls:
    name = div.xpath('./div/div[3]/div[1]/a/text()') # 名字
    state = div.xpath('./div/div[3]/div[1]/div/text()') # 状态
    corp = div.xpath('./div/div[3]/div[3]/div[1]/a/text()') # 法人
    money = div.xpath('./div/div[3]/div[3]/div[2]/span/text()') # 注册资本
    date = div.xpath('./div/div[3]/div[3]/div[3]/span/text()') # 日期
    phone = div.xpath('./div/div[3]/div[4]/div[1]/span/text()')[1:2] # 电话
    email = div.xpath('./div/div[3]/div[4]/div[2]/span[2]/text()') # 邮箱
    site = div.xpath('./div/div[3]/div[5]/text()') # 地址
    l = [name,state,corp,money,date,phone,email,site]
    print(l)
