import os

pip_list = [
    #    'hm3u8dl-cli',
    # 'pygame',
    'requests',
    'pyinstaller',
    'tqdm',
    #    'pprintjson',
    'urllib3',
    'selenium',
    'pycryptodome',  # 解密
    'playsound',  # 音乐播放
    'pyautogui',  # 自动化
    'pillow',  # 图像识别
    'plyer',  # 通知
    'pyexecjs2',  # py解析使用js
    'opencv-python',
    'rich'  # 输出彩色字体
]
os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U')  # 清华源更新pip
os.system('pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple')  # 设置默认下载地址为清华源
for i in pip_list:
    print(f'\033[1;32;40m安装\t\t{i} 中。。。\033[0m')
    os.system(f'pip install {i}')
print(f'\033[1;32;40m完成！\t\t共{len(pip_list)}个\033[0m')
print('-----目前安装的有-----\n')
os.system('pip list')
input()