import time
import re
import streamlit as st
import os
import pandas as pd


def get_data(data_file):
    data_all_ls = []
    data_ls_show = []
    periods_ls = []
    with open(data_file, 'r', encoding='utf-8') as fp_1:
        data_ls = fp_1.readlines()
        for i in data_ls:
            data = re.findall('\S{1,}',i)
            if data == []:
                continue
            data_ls_show.append([float(data[-2]),float(data[-1])])
            periods_ls.append(data[0])
            data_all_ls.append(data)

    return data_all_ls,data_ls_show,periods_ls

def start(x,data_file,web_file):
    i = 0
    while True:
        data_all_ls, data_ls_show, periods_ls = get_data(data_file)
        current_time = data_all_ls[-1][1] +'-'+ data_all_ls[-1][2]
        text = f'''
data_ls_show = {data_ls_show}
# index = {periods_ls}
import streamlit as st
import pandas as pd
\'\'\'
# {title}
###### 当前数据：期数：{data_all_ls[-1][0]} 时间：{current_time.replace(':','-')} {data_name[0]}：{data_all_ls[-1][3]} {data_name[1]}：{data_all_ls[-1][4]}
\'\'\'
all_dp = pd.DataFrame({data_all_ls},columns={title_index},index=range(1,{len(data_all_ls)+1}))
# st.set_page_config(page_title='富达模拟盈亏数据图')
chart_data = pd.DataFrame(
    data_ls_show,
    # index=index,
    columns={data_name}
    )
st.line_chart(chart_data,height=400,width=500)
st.dataframe(all_dp,height=400,width=700)
# st.balloons() # 放气球
        '''
        with open(web_file,'w',encoding='utf-8') as fp_2:
            fp_2.write(text)

        time.sleep(x)


if __name__ == '__main__':

    title = '富达模拟盈亏数据图'
    data_name = ['数据1', '数据2']
    title_index = ['期数', '日期', '时间'] + data_name
    web_file = 'web_file.py'

    # data_dir = r'D:\0_BY_HUI_object\接单\NO5--5175\挂机数据目录'
    # file_ls = os.listdir(data_dir)
    # newest_file = file_ls[-1]
    # file_path = os.path.join(data_dir,newest_file)
    # 与上面4行2选1
    file_path = r'D:\0_BY_HUI_object\接单\NO5--5175\挂机数据目录\test.txt'
    x = 5  # 刷新时间
    print(f'当前目录cmd下运行：streamlit run {web_file}')
    start(x,file_path,web_file)

