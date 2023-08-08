import base64
import urllib.parse
from Crypto.Cipher import AES
import re
import base64
import binascii


def debase64_(data: str):
    return base64.b64decode(data).decode('utf-8').encode().decode('unicode_escape')


def deescape_(data: str):
    return urllib.parse.unquote(data.replace('%u', '\\u').encode().decode('unicode-escape'))


def deunicode_(data: str):
    return data.encode('utf-8').decode('unicode_escape')


def deaes_cbc(data: str, key: str, iv: str):
    def add_16(par):  # 补位到16倍数位
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    # 对key进行补位 。key，iv 进行编码，把data编码成字节
    key = add_16(key.encode('utf-8'))
    iv = iv.encode('utf-8')
    if '/' in data or '+' in data or '=' in data:  # 为普通字节
        data = base64.decodebytes(data.encode('utf-8'))
    else:
        data = binascii.a2b_hex(data.encode('utf-8'))  # 为十六位数
    aes = AES.new(key, AES.MODE_CBC, iv)
    text = aes.decrypt(data)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', "", text.decode('utf-8'))
    return text


def yinhua_jiemi(jump_url, key='57A891D97E332A9D'):
    import requests
    import re
    """
    :param url:樱花动漫解析网址
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    url = 'https://danmu.yhdmjx.com/m3u8.php?url=' + jump_url
    resp = requests.get(url).text
    iv = re.search('<script>var.?bt_token.?=.?"(?P<iv>.*?)";.?</script>', resp)['iv']
    data = re.search('getVideoInfo\("(?P<data>.*?)"\)', resp)['data']
    url = deaes_cbc(data, key, iv)
    return url


if __name__ == '__main__':
    url = 'https://danmu.yhdmjx.com/m3u8.php?url=ksxUY0Bd5nJghA51z%2FAPtRkpMKTYl2cAnnQGM3ZLcqRHFyfmO2GUfBvm9fTyDDg0'
    print(yinhua_jiemi(url))