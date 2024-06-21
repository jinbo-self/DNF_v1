import numpy as np
from PIL import Image, ImageOps
from paddleocr import PaddleOCR
import mss

import logging

from 数据 import *

# 设置ppocr的日志级别为WARNING，这将关闭DEBUG信息
logging.getLogger('ppocr').setLevel(logging.WARNING)

class 识字初始化:

    def __init__(self):
        self.ocr = PaddleOCR()
        self.sct = mss.mss()

    def get_sct(self):
        return self.sct

    def 识字(self, region):
        sct_img = self.sct.grab(region)
        # 将捕获的数据转换为PIL.Image对象
        self.img = Image.frombytes('RGB', (sct_img.width, sct_img.height), sct_img.rgb)
        ocr = self.ocr
        cropped_image = self.img
        # cropped_image = self.img.crop(region)
        # 计算新的尺寸，假设我们想要放大到原来的两倍
        h, w = cropped_image.height, cropped_image.width
        border = [0, 0]
        transform_size = 320  # 图片增加边框到320大小
        if w < transform_size or h < transform_size:
            if h < transform_size:
                border[0] = (transform_size - h) / 2.0
            if w < transform_size:
                border[1] = (transform_size - w) / 2.0
            # top，buttom，left，right 对应边界的像素数目（分别为图像上面， 下面， 左面，右面填充边界的长度）

            cropped_image = ImageOps.expand(cropped_image,
                                            border=(int(border[0]), int(border[0]), int(border[1]), int(border[1])),
                                            fill=(215, 215, 215))
        try:
            result = ocr.ocr(np.array(cropped_image), cls=False)
            for line in result:
                for i in line:
                    return i[-1][0]
        except Exception as e:
            return ""

    def in城镇(self):
        字符 = self.识字(人物)
        if "人物" in 字符:
            return True
        else:
            return False

    def in赛利亚房间(self):
        字符 = self.识字(赛丽亚)
        if "赛丽亚" in 字符:
            return True
        else:
            return False

    def is公告界面(self):
        字符 = self.识字(公告_关闭)
        if "关闭" in 字符:
            return True
        else:
            return False

    def 获取所选地图名称(self):
        字符 = self.识字(所选地图名字)
        if 字符 != "":
            return 字符
        else:
            return ""

    def is开门(self, 当前房间):
        行数 = len(小地图路径.地图数据)
        列数 = len(小地图路径.地图数据[0])
        房间宽度 = int((小地图位置[2] - 小地图位置[0]) / 列数)
        房间高度 = int((小地图位置[3] - 小地图位置[1]) / 行数)
        #当前房间左上角坐标
        当前房间x = int(小地图位置[0] + 当前房间[1] * 房间宽度)
        当前房间y = int(小地图位置[1] + 当前房间[0] * 房间高度)
        #当前房间左边
        if self.识字((当前房间x - 房间宽度, 当前房间y, 当前房间x, 当前房间y + 房间高度)) == '?' or self.识字(
                (当前房间x - 房间宽度, 当前房间y, 当前房间x, 当前房间y + 房间高度)) == '？':
            return True
        #当前房间上边
        elif self.识字((当前房间x, 当前房间y - 房间高度, 当前房间x + 房间宽度, 当前房间y)) == '?' or self.识字(
                (当前房间x, 当前房间y - 房间高度, 当前房间x + 房间宽度, 当前房间y)) == '？':
            return True
        #当前房间右边
        elif self.识字(
                (当前房间x + 房间宽度, 当前房间y, 当前房间x + 房间宽度 * 2, 当前房间y + 房间高度)) == '?' or self.识字(
            (当前房间x + 房间宽度, 当前房间y, 当前房间x + 房间宽度 * 2, 当前房间y + 房间高度)) == '？':
            return True
        # 当前房间下边
        elif self.识字(
                (当前房间x, 当前房间y + 房间高度, 当前房间x + 房间宽度, 当前房间y + 2 * 房间高度)) == '?' or self.识字(
            (当前房间x, 当前房间y + 房间高度, 当前房间x + 房间宽度, 当前房间y + 2 * 房间高度)) == '？':
            return True
        else:
            return False

    def is通关(self):
        字符 = self.识字(跳过翻牌)
        if "奖励" in 字符:
            return True
        else:
            return False



if __name__ == '__main__':
    pass
    识字 = 识字初始化()
    print(识字.识字((0, 0, 726, 280)))
    # while True:
    #     print(识字.识字(人物))
