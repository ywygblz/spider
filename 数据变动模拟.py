import random,time

path = r"D:\0_BY_HUI_object\接单\NO5--5175\挂机数据目录\test.txt"
i = 0
while True:
    i+=1

    # int_num = random.randint(0, 100)
    float_num_1 = random.randint(-10000, 10000) / 1000
    float_num_2 = random.randint(-10000, 10000) / 1000
    with open(path,'a+',encoding='utf-8') as fp:
        text = f'\n20220610{str(i).zfill(4)}        2022:06:10 15:39:09        {float_num_1}        {float_num_2}'
        fp.write(text)
    print(f'已插入:{text}')
    time.sleep(5)
