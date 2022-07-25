import hashlib
import os
import re

from django.shortcuts import render, HttpResponse, redirect
from django.http import StreamingHttpResponse
from .models import User_info

from .tool_func import *


# Create your views here.

# 文件信息
def get_file_ls():
    file_path = 'file_catalogue'
    file_ls = os.listdir(file_path)
    file_info_ls = []
    for file in file_ls:
        file_abs = os.path.join(file_path, file)
        if 1024 < os.path.getsize(file_abs) < 1024 * 1024:
            file_size = str(round(os.path.getsize(file_abs) / 1024, 2)) + 'KB'
        elif os.path.getsize(file_abs) < 1024:
            file_size = str(os.path.getsize(file_abs)) + '字节'
        else:
            file_size = str(round(os.path.getsize(file_abs) / 1024 / 1024, 2)) + 'MB'
        file_type = os.path.splitext(file_abs)[1][1:]

        file_info_ls.append([file, file_size, file_type])

    return file_info_ls


# 密码加密
def password_md5(password: str):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


# print(get_file_ls())
# 登陆
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        try:
            judge_password = User_info.objects.filter(user=username).get().password
            password = password_md5(password)
        except:
            return render(request, 'login.html', {'login_info': '用户名不存在，请重注册!!!'})
        if password != judge_password:
            return render(request, 'login.html', {'login_info': '用户名或密码不正确，请重新尝试!!!'})
        else:
            request.session['info'] = {'user': username, 'password': password}
            return redirect('/home/', {'name': username})

    return render(request, 'login.html')


file_info_ls = []

download_judge = False


# 登陆下载验证
def login_download_judge(func):
    def judge(request, *args, **kwargs):
        global download_judge
        try:
            userinfo = request.session['info']
            username = userinfo['user']
            password = userinfo['password']
        except:
            download_judge = True
            return func(request, *args, **kwargs)

        judge_password = User_info.objects.filter(user=username).get().password
        # password = password_md5(password)
        if password != judge_password:
            download_judge = True
        else:
            download_judge = False

        return func(request, *args, **kwargs)

    return judge


# 登陆验证
def login_judge(func):
    def judge(request, *args, **kwargs):
        try:
            userinfo = request.session['info']
            username = userinfo['user']
            password = userinfo['password']
        except:
            return redirect('/login/')
        judge_password = User_info.objects.filter(user=username).get().password
        # print(password , judge_password)
        if password != judge_password:
            return redirect('/login/')
        return func(request, *args, **kwargs)

    return judge


# 文件加密
def encrypt(file, judge):
    fp = open(file, 'rb')
    if not judge:
        data_ls = fp.read()
        data_ls = data_ls[::-1]
        with open('temp', 'wb') as f:
            f.write(data_ls)
        return fp
    else:
        return fp


# 主页
def home(request):
    global file_info_ls
    file_info_ls = get_file_ls()
    html_text = ''
    for file_info in file_info_ls:
        index = file_info_ls.index(file_info)
        html_text += f'''
        <tr style="height: 40px;">
            <td>{index + 1}</td>
            <td class='file_name'>{file_info[0]}</td>
            <td>{file_info[1]}</td>
            <td>{file_info[2]}</td>
            <td>
                <div>
                    <button class="file_download" style="height:30px;width: 60px;user-select: none;font-size:16px;" onclick="download({index})" >下载</button>
                    <span>  <span>
                    <button class="file_delete" style="height:30px;width: 60px;user-select: none; font-size:16px;" onclick="delete({index})" >删除</button>
                </div>
            </td>
        </tr>
        '''
    user_info = request.session.get('info')
    if user_info is not None:
        name = user_info['user']
    else:
        name = '登陆'

    load_data = {'all_text': html_text, 'name': name}
    return render(request, 'home.html', load_data)


# 下载文件
@login_download_judge
def download(request):
    file_index = request.GET.get('filename')
    filename = file_info_ls[int(file_index)]
    file_path = f'file_catalogue/{filename[0]}'
    # print(download_judge)
    f = open(file_path, 'rb')
    temp = open('temp', 'wb')
    if not download_judge:
        data_ls = f.read()
        # temp.write(data_ls[::-1])
        data_ls = b_decrypt(data_ls)
        temp.write(data_ls)
    else:
        data_ls = f.read()
        temp.write(data_ls)
    temp.close()

    response = StreamingHttpResponse(open('temp', 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)

    return response


# 文件类型
file_type = [".doc", ".docx", ".docm", ".dotx", ".dotm", ".xls", ".xlsx", ".xlsm", ".xltx", ".xltm", ".xlsb", ".xlam",
             ".PPT", ".PPTx", ".PPTm", ".pPSx", ".pPSm", ".potx", ".potm", ".ppam", ".bmp", ".tif", ".tiff", ".cpx",
             ".dwg", ".eps", ".gif", ".ico", ".jiff", ".jpeg", ".jpg", ".pdf", ".pm5", '.jpeg', '.png']


# 上传文件
@login_judge
def upload_file(request):
    if request.method == "POST":
        # 获取上传的文件,如果没有文件,则默认为None;
        File = request.FILES.get("myfile", None)
        if File is not None:
            file_len = sum([len(i) for i in File.chunks()])
            print(file_len, '长度')
            if file_len > 10 * 1024 * 1024:
                return render(request, 'load_file.html', {'state': '文件大于10MB'})
            elif '.' + File.name.split('.')[-1] not in file_type:
                return render(request, 'load_file.html', {'state': '文件不属于office文档或图片文件'})
            # 打开特定的文件进行二进制的写操作;
            file_path = os.path.join('file_catalogue', File.name)
            with open(file_path, 'wb+') as f:
                # 分块写入文件;
                for chunk in File.chunks():
                    # chunk = chunk[::-1]
                    chunk = b_encrypt(chunk)
                    f.write(chunk)

        return render(request, 'load_file.html', {'state': '上传成功'})

    else:
        return render(request, 'load_file.html')


# 注册
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user_judge = re.findall('^[\u4E00-\u9FA5A-Za-z\d]{8,36}$', username)
        password_judge = re.findall('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,36}$', password)
        if user_judge == [] and password_judge != []:
            register_user = '请输入有效的中文、英文字母、数字,且帐号位数在8-16位内'
            register_password = ''
        elif user_judge != [] and password_judge == []:
            register_user = ''
            register_password = '密码必须包含大小写字母和数字的组合，不能使用特殊字符,且密码位数在8-36位内'
        elif user_judge == [] and password_judge == []:
            register_user = '请输入有效的中文、英文字母、数字,且帐号位数在8-16位内'
            register_password = '密码必须包含大小写字母和数字的组合，不能使用特殊字符,且密码位数在8-36位内'
        else:
            try:
                judge_sql_user = User_info.objects.filter(user=user_judge[0]).get().user
                print(judge_sql_user)
                return render(request, 'register.html', {'successfully': '此帐号已注册'})
            except:
                password = password_md5(password_judge[0])
                User_info.objects.create(user=user_judge[0], password=password)
                return render(request, 'register.html', {'successfully': '注册成功'})
        # Aadfjadsfljl54kjfd

        print(user_judge, register_password)
        load_dt = {'register_user': register_user, 'register_password': register_password}
        return render(request, 'register.html', load_dt)

    return render(request, 'register.html')


# 注销
def logout(request):
    request.session['info'] = None
    return render(request, 'login.html')
