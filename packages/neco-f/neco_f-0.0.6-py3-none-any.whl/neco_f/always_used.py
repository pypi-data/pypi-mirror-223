import json
from neco_f.internet import download


def format_str(data: str):
    # 去除字符串中的 ' / , \ , " , ? , * , < , > , | , : ,空格'
    return data.replace('/', '').replace('\\', '').replace('"', '').replace('?', '').replace('*', '') \
        .replace('<', '').replace('>', '').replace('|', '').replace(':', '').replace(' ', '')


# 输入选集
def set_episode():
    while 1:
        try:
            input_ = input('从第几集开始下载？ (如果下载整部的话请直接回车 >>> ')
            if input_.replace(' ', '') == '' or input_ == '0':
                return 0
            return int(input_) - 1
        except ValueError:
            print('请输入数字！！！')


# 让用户输入数字 如果输入空白则返回0
def input_int(data: str):
    while 1:
        try:
            input_ = input(data)
            if input_.replace(' ', '') == '':
                return 0
            return int(input_)
        except ValueError:
            print('请输入数字！！！')


# 播放音乐
def play_mp3(path: str, thread: bool = False):
    from playsound import playsound
    from threading import Thread
    if thread:
        path = f'{path}'.replace('\\', '/')  # 不知道为什么只能用左斜杠
        Thread(target=playsound, args=[path]).start()
    else:
        playsound(path)


# windows 弹窗
def notice(title='test', message='test', icon=None, time_=3, music_path=''):
    from plyer import notification
    if len(music_path) != 0:
        play_mp3(music_path, 1)
    # time.sleep(0.1)
    notification.notify(
        title=title,
        message=message,
        app_icon=icon,
        timeout=time_)


# 打包时要加 --hidden-import plyer.platforms.win.notification


# 创建文件夹
def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    if isExists := os.path.exists(path):
        # print(' 创建过了')
        return False
    os.makedirs(path)
    print(f'{path} 创建成功')
    return True


# 获取文件夹大小
def getdirsize(dir):
    import os
    return sum(sum(os.path.getsize(os.path.join(root, name)) for name in files) for root, dirs, files in os.walk(dir))


# 请求超时重试
def request_timeout_retry(url: str, headers: dict = None, out_time: int = 2, retry_cnt: int = 3):
    '''
    :param url: 地址
    :param data: 请求头
    :param out_time: 超时时间
    :param retry_cnt: 重试次数
    '''
    import requests
    for i in range(retry_cnt):
        try:
            resp = requests.get(url, headers=headers, timeout=out_time)
            return resp
        except requests.exceptions.RequestException:
            pass
    print(f'{url} 访问超时！')
    return False


# pyqt5 界面居中
# def pyqt_in_canter(QWidget_class):
#     from PyQt5.QtWidgets import QDesktopWidget
#     center_pointer = QDesktopWidget().availableGeometry().center()
#     x = center_pointer.x()
#     y = center_pointer.y()
#     # w.move(x, y)
#     # w.move(x - 150, y - 150)
#     # print(w.frameGeometry())
#     # print(w.frameGeometry().getRect())
#     # print(type(w.frameGeometry().getRect()))
#     old_x, old_y, width, height = QWidget_class.frameGeometry().getRect()
#     QWidget_class.move(int(x - width / 2), int(y - height / 2))


def pyinstaller(py_path, icon_path: str = False, have_notice: bool = False, mode: str = '-F', finish_open=False):
    """
    :param py_path: py文件路径，必填
    :param icon_path: 图标路径,非必填
    :param have_notice: 代码中是否含有notice，非必填
    :param mode: 打包模式 默认-F。-D 打包多个文件,-w 无命令行
    :return:
    """
    import os
    command = f'pyinstaller {mode}'
    if icon_path:
        command += f' -i {icon_path}'
    command += f' {py_path}'
    if have_notice:
        command += ' --hidden-import plyer.platforms.win.notification'
    os.system(command)
    # notice('pyinstaller', '打包完成！！')
    if finish_open:
        dist_path = '\\'.join(py_path.split('\\')[:-1]) + r'\dist'
        os.startfile(dist_path)


def get_path(desktop=False, temp=False):
    import os
    if desktop:
        return os.path.join(os.path.expanduser("~"), 'Desktop')
    if temp:
        return os.getenv('TEMP')


def pretty_str(data: str, sign: str = '-', num: int = 20):
    return f'{sign * num}{data}{sign * num}'


def thread_join(threads):
    [i.start() for i in threads]
    [i.join() for i in threads]


# 获取硬盘信息
def get_ssd_info(path, show_mode='gb'):
    import shutil
    total, used, free = shutil.disk_usage(path)
    # bite/1024 kb/1024 mb/1024 gb
    if show_mode == 'gb' or show_mode == 'GB':
        sizi = 1024 ** 3
    if show_mode == 'mb' or show_mode == 'MB':
        sizi = 1024 ** 2
    all_size = round(total / sizi, 2)
    used_size = round(used / sizi, 2)
    free_size = round(free / sizi, 2)
    return all_size, used_size, free_size


# 美化json
def pretty_json(data):
    if isinstance(data, dict):
        return json.dumps(data, indent=4, ensure_ascii=False)
    elif isinstance(data, str):
        try:
            data_dict = json.loads(data.replace("'", '"'))
            return json.dumps(data_dict, indent=4, ensure_ascii=False)
        except json.JSONDecodeError as e:
            return f"Error: {e.msg}"
    else:
        return "Error: input data is not a dictionary or a string"


# 编写bat脚本，删除旧程序，运行新程序
def WriteRestartCmd(rename: str, exe_name: str = 'updata.exe', icon=None,
                    download_url: str = ''):  # sourcery skip: ensure-file-closed, use-fstring-for-concatenation
    """
    :param exe_name: 下载的新版软件名字,默认为 updata.exe
    :param icon: 图标
    :param rename: 新软件要改的名字，同时是通知弹窗的标题
    :param download_url: 软件下载url
    打包要加 --hidden-import plyer.platforms.win.notification
    """
    import os
    import subprocess
    import sys

    if os.path.isfile("upgrade.bat"):  # 新程序启动时，删除旧程序制造的脚本
        os.remove("upgrade.bat")

    if len(download_url) != 0:
        download(download_url, f'./{exe_name}')

    if not os.path.isfile(exe_name):
        return

    notice(rename, '发现新版，将会自动重启软件并更新！！', icon=icon, time_=2)

    b = open("upgrade.bat", 'w')
    TempList = "@echo off\n"
    TempList += '@echo 请不要按任何键！\n'
    TempList += 'echo createobject("scripting.filesystemobject").deletefile(wscript.scriptfullname) >%temp%\VBScriptWait.vbs& echo ' \
                f'wscript.sleep {6000} >>%temp%\VBScriptWait.vbs& start /wait %temp%\VBScriptWait.vbs\n'
    TempList += "del " + os.path.realpath(sys.argv[0]) + "\n"  # 删除当前文件
    if rename != '':
        TempList += f'rename {exe_name} {rename}\n'  # 改名
        exe_name = rename
    TempList += "start " + exe_name  # 启动新程序
    b.write(TempList)
    b.close()
    subprocess.Popen("upgrade.bat")
    sys.exit()  # 进行升级，退出此程序