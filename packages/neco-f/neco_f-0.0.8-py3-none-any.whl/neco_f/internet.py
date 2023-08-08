import requests
from tqdm import tqdm
import os


# 请求超时重试
def request_timeout_retry(url: str, headers: dict = {}, out_time: int = 2, retry_cnt: int = 3):
    '''
    :param url: 地址
    :param data: 请求头
    :param out_time: 超时时间
    :param retry_cnt: 重试次数
    '''
    for i in range(retry_cnt):
        try:
            resp = requests.get(url, headers=headers, timeout=out_time)
            return resp
        except requests.exceptions.RequestException:
            pass
    print(f'{url} 访问超时！')
    return False


# 进度条下载
def download(url: str, fname: str):
    resp = requests.get(url, stream=True)  # 用流stream的方式获取url的数据
    total = int(resp.headers.get('content-length', 0))  # 拿到文件的长度，并把total初始化为0
    with open(fname, 'wb') as file, tqdm(  # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
            desc=fname,  # 下载界面显示文件的名称
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


# n_m3u8 下载入口
def n_m3u8DL(fileurl: str, workDir=None, saveName=None, baseUrl=None, headers=None, maxThreads=64, minThreads=50,
             retryCount=15, timeOut=10, useKeyBase64=None, stopSpeed=30, enableDelAfterDone=True,
             enableBinaryMerge=False, disableIntegrityCheck=False):
    """
    :param fileurl:文件地址可以为网络或者本地
    :param workDir:保存地址
    :param saveName:保存名字，不需要后缀
    :param maxThreads:最大线程默认32
    :param minThreads:最小线程默认16
    :param retryCount:指定程序最大重试次数。某些时候我们并不能一次性成功下载所有分片，在一次任务结束后，程序会检测已下载的TS分片数量和m3u8文件中的分片数量是否相等，不一致则进入重试环节。默认值为15
    :param timeOut:指定程序进行网络请求的超时时长，默认值为10秒
    :param useKeyBase64:强制使用AES-128解密，并使用输入的Base64String来作为解密KEY
    :param stopSpeed:低于这个速度会重试，默认0
    :param enableDelAfterDone:用于开启程序的下载完成后自动删除临时目录功能，默认开启
    :param enableBinaryMerge:二进制合并,默认关闭
    :param disableIntegrityCheck:不进行完整性检验，默认关闭
    """

    from threading import Thread
    command = 'N_m3u8DL-CLI.exe'
    command += f' "{fileurl}"'
    if workDir:
        command += f' --workDir "{workDir}"'
    if saveName:
        command += f' --saveName "{saveName}"'
    if baseUrl:
        command += f' --baseUrl "{baseUrl}"'
    if headers:
        # 格式为 Cookie:xxxxx|User-Agent:xxxx  即用|进行分割
        temp = ''.join(f'{key}:{value}|' for key, value in zip(headers.keys(), headers.values()))
        command += f' --headers "{temp}"'
    if maxThreads != 32:
        command += f' --maxThreads "{maxThreads}"'
    if minThreads != 16:
        command += f' --minThreads "{minThreads}"'
    if retryCount != 15:
        command += f' --retryCount "{retryCount}"'
    if timeOut != 10:
        command += f' --timeOut "{timeOut}"'
    if useKeyBase64:
        command += f' --useKeyBase64 "{useKeyBase64}"'
    if stopSpeed != 30:
        command += f' --stopSpeed "{stopSpeed}"'
    if enableDelAfterDone:
        command += f' --enableDelAfterDone'
    if enableBinaryMerge:
        command += f' --enableBinaryMerge'
    if disableIntegrityCheck:
        command += f' --disableIntegrityCheck'
    # print(command)
    os.system(command)


# 使用wget下载
def wget_downloader(url: str, save_dir: str, save_name: str, wget_path: str = 'wget.exe'):
    import subprocess
    command = f'{wget_path} {url}'
    if save_dir and save_name:
        save_path = fr'{save_dir}\{save_name}'
        command += f' -O {save_path}'
    subprocess.call(command)


# 使用idm进行下载
def idm_download(url, save_dir, save_name):
    # 需要将idm文件夹加入系统变量path
    from subprocess import call
    import time
    idm_path = 'C:\Program Files (x86)\Internet Download Manager\IDMan.exe'
    call(f'{idm_path} /d {url} /p {save_dir} /f {save_name} /n')


if __name__ == '__main__':
    import threading
    from m_f.always_used import wait_threads

    threads = []
    for i in range(3):
        threads.append(threading.Thread(target=wget_downloader, args=(
            'https://yunpan.aliyun.com/downloads/apps/desktop/aDrive.exe', r'C:\Users\33066\Desktop', f'{i}.mp4')))
    wait_threads(threads)
    print('over')