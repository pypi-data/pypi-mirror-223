import base64
import pyautogui


class Pic:
    def __init__(self, pic_path):
        self.pic_path = pic_path

    def base64_pic(self):
        with open(self.pic_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string

    # opencv 找图
    def find_pic(self, pic_path, click=False):
        import os
        import pyscreeze
        import cv2
        import numpy as np
        # 屏幕缩放系数 mac缩放是2 windows一般是1
        screenScale = 1
        # 事先读取按钮截图
        target = cv2.imdecode(np.fromfile(pic_path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
        # 先截图
        screenshot = pyscreeze.screenshot('my_screenshot.png')
        # 读取图片 灰色会快
        temp = cv2.imread(r'my_screenshot.png', cv2.IMREAD_GRAYSCALE)

        theight, twidth = target.shape[:2]
        tempheight, tempwidth = temp.shape[:2]
        # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
        scaleTemp = cv2.resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
        # 匹配图片
        res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
        mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        os.remove('my_screenshot.png')
        if max_val >= 0.8:
            # 计算出中心点
            top_left = max_loc
            tagHalfW, tagHalfH = int(twidth / 2), int(theight / 2)
            tagCenter = (top_left[0] + tagHalfW, top_left[1] + tagHalfH)
            if click:
                pyautogui.click(tagCenter)
            return tagCenter
        else:
            # print("没找到")
            return None