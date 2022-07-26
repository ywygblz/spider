# -*- coding: utf-8 -*-
# @Time    : 2022/6/7 23:24
# @Author  : By_hui
# @File    : 飞卢小说工具.py
# @Software: PyCharm

import os
import re
import threading
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import requests
import ttkbootstrap as ttk
from lxml import etree

import copy
from xpinyin import Pinyin

headers = {
    'Cookie': 'host4chongzhi=b.faloo.com; KeenFire=UMID=8871100&UserID=z854316885&Pwd=0a96584cda9ee0937db1927322c905ed&Identity=web44720.1292013002&PhotoID=0&NickName=%e9%87%8e%e5%8c%ba%e5%93%88%e5%a3%ab%e5%a5%87; UU12345678=uuc=131662919429424811823720392; curr_url=https%3A//b.faloo.com/author/1.html',
    'Referer': 'https://author.faloo.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}

timeout = 10


# 文件列表排序
def get_file_ls():
    files = os.listdir()
    p = Pinyin()
    data_1 = [p.get_pinyin(i) for i in files]
    data_2 = copy.deepcopy(data_1)
    data_2.sort()
    new_file_index = [data_1.index(i) for i in data_2]
    new_file_ls = [files[i] for i in new_file_index]

    return new_file_ls


def try_except(func):
    def test(self, *args, **kwargs):
        try:
            func(self)
        except Exception as E:
            messagebox.showerror('错误', str(E))

    return test


def get_book_info():
    url = 'https://author.faloo.com/OpusList2020.aspx'
    page = requests.get(url=url, headers=headers, timeout=timeout)
    page_text = page.text

    try:
        assert '您还没有登录请先登录' not in page_text
    except:
        messagebox.showerror('错误', f'cookie 失效 登陆失败!!!\n{page_text}')
        return

    tree = etree.HTML(page_text)
    div_ls = tree.xpath('//div[@class="mo_opus"]')
    # tag_text = ['收藏', 'V收藏', '鲜花', '打赏(月)', '人气', '今天催更', '昨天催更']

    data_ls = []
    for div in div_ls:
        ID = div.xpath('./div[1]/div/div[2]/span/span/text()')[0].replace('[', '').replace(']', '')
        name = div.xpath('./div[1]/div/div[2]/a[1]/text()')[0]

        data_ls.append([ID, name])

    return data_ls


# 分卷 1 作品正文  2作品相关
def subsection(book_id, NV_Type, NV_Name, NV_Info, NV_OrderBy):
    url_2 = f'https://author.faloo.com/ajax.aspx?act=17&id={book_id}'
    data = {
        'NV_Type': NV_Type,
        'NV_Name': NV_Name,
        'NV_Info': NV_Info,
        'NV_OrderBy': NV_OrderBy,
    }

    path_json = requests.post(url=url_2, headers=headers, data=data, timeout=timeout).json()
    info = path_json['ReturnString']
    return info


# 章节内容
def get_article(save_path_dir, book_name, book_ID, article_ID, delete_judeg=False):
    url = f'https://author.faloo.com/Ajax.aspx?act=7&id={book_ID}&n={article_ID}'

    page = requests.get(url=url, headers=headers, timeout=timeout)
    try:
        page_json = page.json()["Data"]
    except:
        messagebox.showerror('错误', page.text)
        raise
        # return
    NN_Name = page_json['NN_Name']  # 章节
    NN_Content = page_json['NN_Content']  # 内容
    # print(NN_Name, NN_Content)
    if delete_judeg == False:
        book_name = ''.join(re.findall('[\u4E00-\u9FA5A-Za-z0-9_.]+', book_name))
        NN_Name = ''.join(re.findall('[\u4E00-\u9FA5A-Za-z0-9_.]+', NN_Name))
        path = os.path.join(save_path_dir, f'{book_ID}-{book_name}-{str(article_ID).zfill(6)}-{NN_Name}.txt')
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(NN_Name + '\n\n')
            fp.write(NN_Content)

    else:
        delete_data_dt = {}
        delete_data_dt['publicTime'] = page_json['publicTime']
        delete_data_dt['startDate'] = page_json['startDate']
        delete_data_dt['startHour'] = page_json['startHour']
        delete_data_dt['StartMinute'] = page_json['StartMinute']
        delete_data_dt['StartSecond'] = page_json['StartSecond']

        return NN_Name, NN_Content, delete_data_dt


# 文章，章节id
def get_index(book_ID):
    url = f'https://author.faloo.com/ajax.aspx?act=43&id={book_ID}'
    page_json = requests.get(url=url, headers=headers, timeout=timeout).json()["Data"]
    type_index_dt = {}

    delete_partID_chapterID_dt = {}
    for i in page_json:
        NV_Name = i['NV_Name']  # 草稿箱 回收站 作品相关 正文
        NodeList = i['NodeList']
        index_dt = {}
        NV_OrderBy = i['NV_OrderBy']
        delete_partID_chapterID_dt[NV_OrderBy] = []
        if NodeList:
            for j in NodeList:
                NN_Name = j['NN_Name']
                NovelNodeID = j['NovelNodeID']
                delete_partID_chapterID_dt[NV_OrderBy].append(NovelNodeID)
                index_dt[NN_Name] = NovelNodeID
        else:
            ...
        type_index_dt[NV_Name] = index_dt

    return type_index_dt, delete_partID_chapterID_dt


# 删除
def delete_article(book_ID, article_ID):
    save_path_dir, book_name = '', ''
    NN_Name, NN_Content, delete_data_dt = get_article(save_path_dir, book_name, book_ID, article_ID, delete_judeg=True)
    url = f'https://author.faloo.com/ajax.aspx?act=8&id={book_ID}&n={article_ID}'
    print(NN_Name, NN_Content)

    data = {
        'volumeSelected': '-10',
        'nodeName': NN_Name.replace('\ufffd', '').encode('gbk'),
        'nodeContent': NN_Content.replace('\ufffd', '').encode('gbk'),
    }

    data.update(delete_data_dt)

    page_json = requests.post(url=url, headers=headers, data=data, timeout=timeout).json()
    info = f'已删除：id：{book_ID}，章节id：{article_ID}'

    return info


# 合并txt文件
def merge_txt(name='当前合并'):
    file_name = f'{name}.txt'
    with open(file_name, 'w', encoding='utf-8', newline='') as fp:

        file_ls = os.listdir()
        for i in file_ls:
            if '.txt' in i and file_name not in i:
                with open(i, 'r', encoding='utf-8') as r_fp:
                    text = r_fp.read()
                    fp.write(text.replace('\n\n\n', '\n'))
                    fp.write('\n\n')
                print(f'已完成{i}文件合并!!!')
    messagebox.showinfo('提示', f'已完成所有文件合并!!!,文件为：{file_name}')
    return f'已完成所有文件合并!!!,文件为：{file_name}'


class Fiction_tool_gui:

    def __init__(self):

        self.book_index = None
        self.cookie = None
        self.book_name_section_ls = None
        self.book_id_name_ls = None
        self.path = None
        w, h = 1024, 769
        # win = tk.Tk()
        # style = ttk.Style(theme='sandstone').master
        # ['cyborg', 'journal', 'darkly', 'flatly', 'solar', 'minty', 'litera',
        #  'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero', 'sandstone', 'default']

        win = ttk.Window()
        ttk.Style(theme='litera')
        win.title('飞卢工具')
        win.geometry(f'{w}x{h}+20+20')

        self.font = ('宋体', 12)
        self.win = win
        self.EN_var_ls = []
        self.TE_var_ls = []
        self.table_var_ls = []

    def load_text(self):
        x = 80
        text_dt = {'cookie:': [x, 30], '保存位置:': [x, 70], '用户数据:': [x, 110],
                   '输出信息:': [80, 500], '章节信息:': [550, 110], '最小编号:': [700, 110],
                   '删除间隔:': [840, 110], '采集编号:': [700, 70]
                   }
        for i in text_dt:
            tk.Label(self.win, text=i, font=self.font).place(x=text_dt[i][0], y=text_dt[i][1], anchor='center')
        ...

    def load_box(self):
        x, width, height = 120, 300, 25  # 最小编号              删除间隔
        box_dt = {
            'cookie': [x, 30, width, height],
            '保存位置': [x, 70, width, height],
            '1': [740, 70, 30, height],  # start_num
            '5': [780, 70, 30, height],  # end_num
            '300': [740, 110, 50, height],
            '3': [880, 110, 30, height],

        }
        for i in box_dt:
            EN = tk.Entry(self.win, textvariable=tk.StringVar(value=i), justify='left')
            EN.place(x=box_dt[i][0], y=box_dt[i][1], anchor='w', width=box_dt[i][2], height=box_dt[i][3])
            self.EN_var_ls.append(EN)

    def load_return(self):
        # text_dt = {'输出信息:': [60, 580]}
        TE = tk.Text(self.win, undo=True, autoseparators=False)
        TE.place(x=40, y=520, width=930, height=220)
        self.TE_var_ls.append(TE)

    def load_table(self):

        begin_column = [
            # 首列 和宽
            {'id': 100, '书名': 250},
            {'书名': 120, '类型': 30, '章节': 170, '章节编号': 30}
        ]
        table_xy_ls = [
            # x,y,长，宽
            [40, 130, 450, 350],
            [520, 130, 450, 350]
        ]

        Scrollbar_xy_ls = [
            [495, 130],
            [975, 130],
        ]

        for table_xy, begin_dt, Scrollbar_xy in zip(table_xy_ls, begin_column, Scrollbar_xy_ls):
            yscroll = tk.Scrollbar(self.win, orient=tk.VERTICAL)  # 竖直滚动条
            table = ttk.Treeview(self.win, show='headings', columns=[key for key in begin_dt],
                                 yscrollcommand=yscroll.set)

            for key in begin_dt:
                if begin_dt[key] == 0:
                    table.column(key, anchor='w')
                else:
                    table.column(key, width=begin_dt[key], anchor='center')
                table.heading(key, text=key)

            yscroll.config(command=table.yview)
            yscroll.place(x=Scrollbar_xy[0], y=Scrollbar_xy[1], height=350, width=20, anchor='nw')
            table.place(x=table_xy[0], y=table_xy[1], width=table_xy[2], height=table_xy[3], anchor='nw')

            self.table_var_ls.append(table)

        # 表1事件
        self.table_var_ls[0].bind('<ButtonRelease-1>', self.table_user_info_click_1)
        self.table_var_ls[1].bind('<ButtonRelease-1>', self.table_user_info_click_2)

    # 用户信息表 鼠标 事件
    def table_user_info_click_1(self, event):
        table_user_var = self.table_var_ls[0]
        item_num_ls = table_user_var.selection()  # 选中的行

        data_ls = []
        for item_num in item_num_ls:
            table_data_ls = table_user_var.item(item_num, 'values')  # 选中的值
            data_ls.append(table_data_ls)

        self.book_id_name_ls = data_ls

        book_text = [f'id:{i[0]},书名:{i[1]}' for i in data_ls]
        put_info = f'----当前已选择: ' + '、'.join(book_text) + '----'
        self.journal_output(put_info)

    def table_user_info_click_2(self, event):
        table_user_var = self.table_var_ls[1]
        item_num_ls = table_user_var.selection()  # 选中的行

        data_ls = []
        for item_num in item_num_ls:
            table_data_ls = table_user_var.item(item_num, 'values')  # 选中的值
            data_ls.append(table_data_ls)

        self.book_name_section_ls = data_ls

        book_text = [f'书名:{i[0]},类型:{i[1]},章节:{i[2]},章节ID{i[3]}' for i in data_ls]
        put_info = f'----当前已选择: ' + '、'.join(book_text) + '----'
        self.journal_output(put_info)
        ...

    def load_button(self):
        tk.Button(self.win, text='获取书藉信息', command=self.button_func_1).place(x=450, y=30, width=80, anchor='w')
        tk.Button(self.win, text='获取章节信息', command=self.button_func_2).place(x=550, y=30, width=80, anchor='w')
        tk.Button(self.win, text='批量采集文章', command=lambda: self.thread_it(self.button_func_3)).place(x=650, y=30,
                                                                                                     width=80,
                                                                                                     anchor='w')
        tk.Button(self.win, text='删除文章', command=lambda: self.thread_it(self.button_func_4)).place(x=850, y=30,
                                                                                                   width=80, anchor='w')
        tk.Button(self.win, text='选择文件夹', command=self.button_func_5).place(x=450, y=70, width=80, anchor='w')
        tk.Button(self.win, text='章节管理', command=self.button_func_6).place(x=750, y=30, width=80, anchor='w')
        tk.Button(self.win, text='暂停删除', command=self.button_func_7).place(x=850, y=70, width=80, anchor='w')
        tk.Button(self.win, text='下载合并', command=merge_txt).place(x=550, y=70, width=80, anchor='w')

    # @try_except
    def button_func_1(self):
        print('获取书藉信息')

        user_data_var = self.table_var_ls[0]
        cookie_var = self.EN_var_ls[0]

        headers['Cookie'] = cookie_var.get()

        data_ls = get_book_info()

        if data_ls is not None:
            messagebox.showinfo('提示', '成功登陆!!!')
        else:
            return

        # 清表格
        for table_var in self.table_var_ls:
            for item in table_var.get_children():
                table_var.delete(item)
        for i in data_ls:
            num = data_ls.index(i)
            user_data_var.insert('', num, values=i)

        ...

    @try_except
    def button_func_2(self):
        print('获取章节信息')

        book_id_name_ls = self.book_id_name_ls
        if not book_id_name_ls:
            messagebox.showwarning('警告', '请先选择一个书名信息')
            return

        book_id, book_name = book_id_name_ls[0]
        self.button_3_book_name_id = book_id, book_name
        self.button_3_book_id = book_id
        # try:
        # chapter_info = [[i, i * 3] for i in range(50)]
        type_index_dt, self.delete_partID_chapterID_dt = get_index(book_id)

        chapter_info = []

        for i in type_index_dt:
            if i in ['自动保存的章节', '草稿箱', '回收站', '作品相关']:
                continue
            # print(i)
            type_ = i
            section_name_dt = type_index_dt[i]
            # print(section_name_dt)
            for item in section_name_dt.items():
                # print(item)
                section_name, section_ID = item[0], item[1]
                # print(section_name ,section_ID)
                chapter_info.append([book_name, type_, section_name, section_ID])

        # chapter_info = [[i,type_index_dt[i].keys()] for i in type_index_dt]
        chapter_data_var = self.table_var_ls[1]
        self.chapter_info = chapter_info
        # 清表格

        for item in chapter_data_var.get_children():
            chapter_data_var.delete(item)
        for i in chapter_info:
            num = chapter_info.index(i)
            # print(i)
            chapter_data_var.insert('', num, values=i)
        put_info = f'正在获取书名为：{book_name} 的章节信息'
        self.journal_output(put_info)
        ...

    @try_except
    def button_func_3(self):
        try:
            book_id, book_name = self.button_3_book_name_id
        except:
            messagebox.showwarning('警告', '请先获取章节信息')
            return

        EN_var_1 = self.EN_var_ls[-2]
        EN_var_2 = self.EN_var_ls[-1]
        EN_var_3 = self.EN_var_ls[-3]
        EN_var_4 = self.EN_var_ls[-4]
        title_num = EN_var_1.get()
        wait_time = EN_var_2.get()
        start_num = int(EN_var_4.get())
        end_num = int(EN_var_3.get())
        print(title_num, wait_time, start_num, end_num)

        section_id_dt = {i[-1]: i for i in self.chapter_info}
        # print(section_id_dt)
        section_id_ls = [i[-1] for i in section_id_dt.values()]
        for article_id in range(start_num, end_num + 1):
            if article_id not in section_id_ls:
                continue

            book_name, type_, section_name, section_id = section_id_dt[article_id]
            get_article('./', book_name, self.button_3_book_id, section_id)
            put_info = f'已下载{book_name}，{section_name}...'
            self.journal_output(put_info)
            time.sleep(int(wait_time))

        put_info = merge_txt(f'0_A-{book_id}-{book_name}章节编号{start_num}-{end_num}汇总')
        self.journal_output(put_info)

        # messagebox.showwarning('警告', put_info)
        # print(self.delete_partID_chapterID_dt.keys())
        # for key in self.delete_partID_chapterID_dt.keys():
        #     if key >= int(title_num):
        #         article_id_ls = self.delete_partID_chapterID_dt[key]
        #         for article_id in article_id_ls:
        #             # print(article_id)
        #             book_name, type_, section_name, section_id = section_id_dt[article_id]
        #             get_article('./', book_name, self.button_3_book_id, section_id)
        #             put_info = f'已下载{book_name}，{section_name}...'
        #             self.journal_output(put_info)
        #             time.sleep(int(wait_time))
        #
        # put_info = merge_txt(f'0_A-{book_id}-{book_name}大于{title_num}汇总')
        # self.journal_output(put_info)
        # messagebox.showwarning('警告', put_info)
        ...

    @try_except
    def button_func_4(self):
        self.suspend = False
        try:
            book_id = self.button_3_book_id
        except:
            messagebox.showwarning('警告', '请先获取章节信息')
            return
        EN_var_1 = self.EN_var_ls[-2]
        EN_var_2 = self.EN_var_ls[-1]
        title_num = EN_var_1.get()
        wait_time = EN_var_2.get()
        num = 1
        for key in self.delete_partID_chapterID_dt.keys():

            if key >= int(title_num):
                article_id_ls = self.delete_partID_chapterID_dt[key]
                for article_id in article_id_ls:
                    put_info = delete_article(book_id, article_id)
                    if num == 1:
                        messagebox.showinfo('消息', '开始删除')
                    if self.suspend == True:
                        return
                    self.journal_output(put_info)
                    num = 2
                    time.sleep(int(wait_time))
        messagebox.showwarning('警告', f'已删除编号大于等于{title_num}的章节')
        ...

    def button_func_5(self):
        print('打开文件夹')
        get_path = filedialog.askdirectory()  # 使用askdirectory函数选择文件夹
        path_EN_var = self.EN_var_ls[1]
        path_EN_var.delete(0, tk.END)
        path_EN_var.insert(0, get_path)
        self.path = get_path

        put_info = f'已选择目录:{get_path}'
        if self.path == '':
            messagebox.showwarning('警告', '当前未选择，已设为当前目录')
            os.chdir('./')
            return
        os.chdir(get_path)
        self.journal_output(put_info)
        ...

    # 暂停删除
    def button_func_7(self):
        self.suspend = True
        messagebox.showwarning('警告', '暂停已删除')

    def button_func_6(self):
        print('章节管理')
        win2 = tk.Tk()
        win2.geometry("400x400")
        win2.title('章节管理')
        cbb = ttk.Combobox(win2, textvariable=tk.StringVar())
        cbb.place(x=80, y=30, width=200)
        cbb['value'] = ['作品正文', '作品相关']
        cbb.current(0)

        tk.Label(win2, text='分卷类型:').place(x=20, y=30)
        tk.Label(win2, text='分卷序号:').place(x=20, y=60)
        tk.Label(win2, text='卷标题：').place(x=20, y=90)
        tk.Label(win2, text='卷简介:').place(x=20, y=120)

        e1 = tk.Entry(win2, textvariable=tk.StringVar())
        e1.place(x=80, y=60, width=250)
        e1.insert('insert', '300')

        e2 = tk.Entry(win2, textvariable=tk.StringVar())
        e2.place(x=80, y=90, width=250)

        t1 = tk.Text(win2)
        t1.place(x=80, y=120, width=250, height=200)

        tk.Button(win2, text='添加新卷', command=lambda: self.thread_it(self.win2_Button_1, cbb, e1, e2, t1)).place(x=300,
                                                                                                                y=25)
        win2.mainloop()

    @try_except
    def win2_Button_1(self, cbb, e1, e2, t1):

        type_ = cbb.get()
        type_num = e1.get()
        title = e2.get()
        text = t1.get(1.0, tk.END)
        # print(type_,type_num,title,text)
        type_dt = {'作品正文': '1', '作品相关': '2'}
        try:
            put_info = subsection(self.button_3_book_id, type_dt[type_], title, text, type_num)
            messagebox.showwarning('警告', put_info)
            self.journal_output(put_info)

        except:
            messagebox.showerror('错误', '请先获取章节信息')

        ...

    # 日志输出
    def journal_output(self, text):
        log = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ':' + text + '\n'
        Te_var = self.TE_var_ls[0]
        Te_var.see("end")  # 移到下面
        Te_var.insert("end", log)

        ...

    def thread_it(self, func, *args):
        '''将函数打包进线程'''
        # 创建
        t = threading.Thread(target=func, args=args)
        # 守护 !!!
        # t.setDaemon(False)
        # 启动
        t.start()

    def run(self):
        self.win.mainloop()


def start():
    start = Fiction_tool_gui()
    start.load_text()
    start.load_box()
    start.load_table()
    start.load_return()
    start.load_button()
    start.run()


if __name__ == '__main__':
    start()
    ...
