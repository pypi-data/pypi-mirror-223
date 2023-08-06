from setuptools import setup, find_packages

setup(
    name='neco_f',
    version='0.0.1',
    author='neco_arc',
    author_email='3306601284@qq.com',
    description='A simple Python library',
    long_description='README.md',
    long_description_content_type='text/markdown',
    url='https://github.com/johndoe/my_library',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        #    'hm3u8dl-cli',
        # 'pygame',
        'requests',
        'pyinstaller',
        'tqdm',
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
    ],
)