import requests
import random
from pprint import pprint


class Api:
    def __init__(self):
        self._key = '5d6ffcb535f0b986622d6c27d155dce2'

    def yiyan(self, type='r'):
        # (a:动画；b:漫画；c:游戏；d:文学；e:原创；f:来自网络；g:其他；h:影视；i:诗词；j:网易云；k:哲学)
        if type == 'r':  # r:随机
            type = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'])
            # print(type)
        resp = requests.get(f'http://api.a20safe.com/api.php?api=6&key={self._key}&type={type}').json()
        # pprint(resp)
        data = resp['data'][0]['motto']
        from_ = resp['data'][0]['from']
        # print(f'「 {data} 」\n\t\t————{from_}')
        return data, from_

    def txt_to_mp3(self, txt, speed=3):
        import requests
        resp = requests.get(f'http://api.a20safe.com/api.php?api=8&key={self._key}&text={txt}&spd={speed}').json()
        url = resp['data'][0]["mp3url"]
        # print(url)
        return url

    def yan_zheng_ma(self, pic_base64):
        resp = requests.get(f'https://api.a20safe.com/api.php?api=13&key={self._key}&imgbase64={pic_base64}').json()
        pprint(resp)


if __name__ == '__main__':
    # import pic_
    # pic_base64 = pic_.Pic(r'C:\Users\Administrator\Desktop\Snipaste_2023-07-21_10-00-48.png').base64_pic()
    # Api().yan_zheng_ma(pic_base64)
    Api().yiyan()