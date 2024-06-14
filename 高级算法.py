import math
import time

import 数据

from 常用类的初始化 import 按键
from 键鼠类 import key_press_release


def 取最近物品(所有物品坐标, 人物坐标):
    min_distance = float('inf')  # 初始化最小距离为无穷大
    loc = (0, 0)
    for (x, y) in 所有物品坐标:
        distance = math.sqrt((x - 人物坐标[0]) ** 2 + (y - 人物坐标[1]) ** 2)  # 计算距离
        if distance < min_distance:
            min_distance = distance
            loc = (x, y)
    return loc


def 判断是否为背包满了():
    return False


def 弹起(键代码):
    if 键代码 == 'left':
        if 数据.全_左方向键:
            数据.全_左方向键 = False
            按键.key_release(键代码)
            return True
    elif 键代码 == 'up':
        if 数据.全_上方向键:
            数据.全_上方向键 = False
            按键.key_release(键代码)
            return True
    elif 键代码 == 'right':
        if 数据.全_右方向键:
            数据.全_右方向键 = False
            按键.key_release(键代码)
            return True
    elif 键代码 == 'down':
        if 数据.全_下方向键:
            数据.全_下方向键 = False
            按键.key_release(键代码)
            return True
    else:
        按键.key_release(键代码)
        return True
    return False


def 按下(键代码):
    if 键代码 == 'left':
        if not 数据.全_左方向键:
            数据.全_左方向键 = True
            按键.key_press(键代码)
            return True
    elif 键代码 == 'up':
        if not 数据.全_上方向键:
            数据.全_上方向键 = True
            按键.key_press(键代码)
            return True
    elif 键代码 == 'right':
        if not 数据.全_右方向键:
            数据.全_右方向键 = True
            按键.key_press(键代码)
            return True
    elif 键代码 == 'down':
        if not 数据.全_下方向键:
            数据.全_下方向键 = True
            按键.key_press(键代码)
            return True
    else:
        按键.key_press(键代码)
        return True
    return False


def 取横向移动方向(起始x, 目标x, x偏移):
    if 起始x > 目标x and 起始x - 目标x > x偏移:
        return 'left'
    if 起始x < 目标x and 目标x - 起始x > x偏移:
        return 'right'
    return ''


def 角色走动_通用版():
    if 数据.全_横向移动方向 == 'left':
        按键.key_release('right')
    elif 数据.全_横向移动方向 == 'right':
        按键.key_release('left')
    if 数据.全_横向移动方向 in 按键.获取所有按下的事件():
        return
    按键.key_press(数据.全_横向移动方向)


def 角色跑动_通用版():
    if 数据.全_横向移动方向 == 'left':
        按键.key_release('right')
    elif 数据.全_横向移动方向 == 'right':
        按键.key_release('left')
    if 数据.全_横向移动方向 in 按键.获取所有按下的事件():
        return
    key_press_release(数据.全_横向移动方向)
    按键.key_press(数据.全_横向移动方向)


def 角色纵向移动_通用版():
    if 数据.全_纵向移动方向 == 'up':
        按键.key_release('down')
    elif 数据.全_纵向移动方向 == 'down':
        按键.key_release('up')
    if 数据.全_纵向移动方向 in 按键.获取所有按下的事件():
        return
    按键.key_press(数据.全_纵向移动方向)


def 取纵向移动方向(起始y, 目标y, y偏移):
    if 起始y > 目标y and 起始y - 目标y > y偏移:
        return 'up'
    if 起始y < 目标y and 目标y - 起始y > y偏移:
        return 'down'
    return ''


def is距离近(人物坐标, 目的坐标, X距离, Y距离):
    x = abs(人物坐标[0] - 目的坐标[0])
    y = abs(人物坐标[1] - 目的坐标[1])
    if x > X距离 or y > Y距离:
        return False
    else:
        return True


def 跑动按键(左右方向, 上下方向):
    """参数为(左右方向, 上下方向)"""
    按键1 = 左右方向
    按键2 = 上下方向
    方向 = ['up', 'down', 'right', 'left']

    if 按键1 in 按键.获取所有按下的事件() and 按键2 in 按键.获取所有按下的事件():
        # 已经按下就不管，释放其他方向
        临时 = [按键1, 按键2]
        方向列表 = [direction for direction in 方向 if direction not in 临时]
        按键.key_release(方向列表[0])
        按键.key_release(方向列表[1])
    elif 按键1 in 按键.获取所有按下的事件():  # right or left
        # 释放按键
        方向列表 = [direction for direction in 方向 if direction != 按键1]
        按键.key_release(方向列表[0])
        按键.key_release(方向列表[1])
        按键.key_release(方向列表[2])
        # 按下 up or down 按一次
        按键.key_press(按键2)
    elif 按键2 in 按键.获取所有按下的事件():  # up or down
        # 释放按键
        方向列表 = [direction for direction in 方向 if direction != 按键2]
        按键.key_release(方向列表[0])
        按键.key_release(方向列表[1])
        按键.key_release(方向列表[2])
        # 按下 right or left 按两次次，跑起来
        key_press_release(按键1)
        按键.key_press(按键1)
    else:  # 一个按键都没有，那就释放所有按键，重新跑起来
        按键.release_all_keys()
        按键.key_press(按键2)
        key_press_release(按键1)
        按键.key_press(按键1)


def 走动按键(左右方向, 上下方向):
    """参数为(左右方向, 上下方向)"""
    按键1 = 左右方向
    按键2 = 上下方向
    方向 = ['up', 'down', 'right', 'left']

    if 按键1 in 按键.获取所有按下的事件() and 按键2 in 按键.获取所有按下的事件():
        # 已经按下就不管，释放其他方向
        临时 = [按键1, 按键2]
        方向列表 = [direction for direction in 方向 if direction not in 临时]
        按键.key_release(方向列表[0])
        按键.key_release(方向列表[1])
    elif 按键1 in 按键.获取所有按下的事件():  # right or left
        # 释放按键
        方向列表 = [direction for direction in 方向 if direction != 按键1]
        按键.key_release(方向列表[0])
        按键.key_release(方向列表[1])
        按键.key_release(方向列表[2])
        # 按下 up or down 按一次
        按键.key_press(按键2)
    elif 按键2 in 按键.获取所有按下的事件():  # up or down
        # 释放按键
        方向列表 = [direction for direction in 方向 if direction != 按键2]
        按键.key_release(方向列表[0])
        按键.key_release(方向列表[1])
        按键.key_release(方向列表[2])
        # 按下 right or left 按两次次，跑起来
        按键.key_press(按键1)
    else:  # 一个按键都没有，那就释放所有按键，重新跑起来
        按键.release_all_keys()
        按键.key_press(按键2)
        按键.key_press(按键1)


def 跑到目标(目的坐标, 横轴偏差=0, 纵轴偏差=0):
    with 数据.全局锁:
        实时坐标 = 数据.全_角色坐标

    if 实时坐标 == (999, 999):
        按键.release_all_keys()
        按键.key_press('up')
        key_press_release('right')
        按键.key_press('right')
        return False

    if is距离近(实时坐标, 目的坐标, 120, 100):
        按键.release_all_keys()
        print("跑到目标附近")
        return 走到目标(目的坐标, 横轴偏差, 纵轴偏差)
    # 向右走
    if 目的坐标[0] > 实时坐标[0] and 目的坐标[1] == 实时坐标[1]:
        print("向右跑")
        if 'right' in 按键.获取所有按下的事件():
            按键.key_release('left')
            按键.key_release('up')
            按键.key_release('down')
        else:
            按键.release_all_keys()
            key_press_release('right')
            按键.key_press('right')
    # 向左走
    if 目的坐标[0] < 实时坐标[0] and 目的坐标[1] == 实时坐标[1]:
        print("向左跑")

        if 'left' in 按键.获取所有按下的事件():
            按键.key_release('right')
            按键.key_release('up')
            按键.key_release('down')
        else:
            按键.release_all_keys()
            key_press_release('left')
            按键.key_press('left')

    # 向下跑
    if 目的坐标[1] > 实时坐标[1] and 目的坐标[0] == 实时坐标[0]:
        print("向下跑")

        if 'down' in 按键.获取所有按下的事件():
            按键.key_release('right')
            按键.key_release('up')
            按键.key_release('left')
        else:
            按键.release_all_keys()
            按键.key_press('down')

    # 向上跑
    if 目的坐标[1] < 实时坐标[1] and 目的坐标[0] == 实时坐标[0]:
        print("向上跑")
        if 'up' in 按键.获取所有按下的事件():
            按键.key_release('right')
            按键.key_release('left')
            按键.key_release('down')
        else:
            按键.release_all_keys()
            按键.key_press('up')

    # 向右上跑
    if 目的坐标[0] > 实时坐标[0] and 目的坐标[1] < 实时坐标[1]:
        print("向右上跑")
        跑动按键('right', 'up')

    # 向右下跑
    if 目的坐标[0] > 实时坐标[0] and 目的坐标[1] > 实时坐标[1]:
        print("向右下跑")
        跑动按键('right', 'down')

    # 向左上跑
    if 目的坐标[0] < 实时坐标[0] and 目的坐标[1] < 实时坐标[1]:
        print("向左上跑")
        跑动按键('left', 'up')

    # 向左下跑
    if 目的坐标[0] < 实时坐标[0] and 目的坐标[1] > 实时坐标[1]:
        print("向左下跑")
        跑动按键('left', 'down')
    return False


def 走到目标(目的坐标, 横轴偏差=0, 纵轴偏差=0):
    # 先声明一下

    # 开始
    with 数据.全局锁:
        实时坐标 = 数据.全_角色坐标
    if is距离近(实时坐标, 目的坐标, 横轴偏差, 纵轴偏差):
        print("走动目标附近")
        按键.release_all_keys()
        # 走到目标(目的坐标, 横轴偏差, 纵轴偏差)
        return True
        # 向右走
    if 目的坐标[0] > 实时坐标[0] and 目的坐标[1] == 实时坐标[1]:
        print("向右走")
        if 'right' in 按键.获取所有按下的事件():
            按键.key_release('left')
            按键.key_release('up')
            按键.key_release('down')
        else:
            按键.release_all_keys()
            按键.key_press('right')
    # 向左走
    if 目的坐标[0] < 实时坐标[0] and 目的坐标[1] == 实时坐标[1]:
        print("向左走")

        if 'left' in 按键.获取所有按下的事件():
            按键.key_release('right')
            按键.key_release('up')
            按键.key_release('down')
        else:
            按键.release_all_keys()
            按键.key_press('left')

    # 向下跑
    if 目的坐标[1] > 实时坐标[1] and 目的坐标[0] == 实时坐标[0]:
        print("向下走")

        if 'down' in 按键.获取所有按下的事件():
            按键.key_release('right')
            按键.key_release('up')
            按键.key_release('left')
        else:
            按键.release_all_keys()
            按键.key_press('down')

    # 向上跑
    if 目的坐标[1] < 实时坐标[1] and 目的坐标[0] == 实时坐标[0]:
        print("向上走")
        if 'up' in 按键.获取所有按下的事件():
            按键.key_release('right')
            按键.key_release('left')
            按键.key_release('down')
        else:
            按键.release_all_keys()
            按键.key_press('up')

    # 向右上跑
    if 目的坐标[0] > 实时坐标[0] and 目的坐标[1] < 实时坐标[1]:
        print("向右上走")
        走动按键('right', 'up')

    # 向右下跑
    if 目的坐标[0] > 实时坐标[0] and 目的坐标[1] > 实时坐标[1]:
        print("向右下走")
        走动按键('right', 'down')

    # 向左上跑
    if 目的坐标[0] < 实时坐标[0] and 目的坐标[1] < 实时坐标[1]:
        print("向左上走")
        走动按键('left', 'up')

    # 向左下跑
    if 目的坐标[0] < 实时坐标[0] and 目的坐标[1] > 实时坐标[1]:
        print("向左下走")
        走动按键('left', 'down')
    return False


def 移动到目标点附近_通用版(目标x, 目标y, x偏移=0, y偏移=0, 弹起x=None, 弹起y=None):
    return 跑到目标((目标x, 目标y), x偏移, y偏移)

    if not 弹起x:
        弹起x = True
    if not 弹起y:
        弹起y = True
    with 数据.全局锁:
        角色坐标 = 数据.全_角色坐标
    if 角色坐标 != (999, 999):
        if 角色坐标[0] == 目标x or abs(角色坐标[0] - 目标x) <= x偏移:
            if 弹起x:
                弹起(数据.全_横向移动方向)
        if 角色坐标[1] == 目标y or abs(角色坐标[1] - 目标y) <= y偏移:
            if 弹起y:
                弹起(数据.全_纵向移动方向)

        if (角色坐标[0] == 目标x and 角色坐标[1] == 目标y) or (
                abs(角色坐标[0] - 目标x) <= x偏移 and abs(角色坐标[1] - 目标y) <= y偏移):
            if 弹起x:
                弹起(数据.全_横向移动方向)
            if 弹起y:
                弹起(数据.全_纵向移动方向)
            return True
        数据.全_纵向移动方向 = 取纵向移动方向(角色坐标[1], 目标y, y偏移)
        print(数据.全_纵向移动方向)
        if 数据.全_纵向移动方向 != '' and 角色坐标[1] != 目标y:
            if abs(角色坐标[1] - 目标y) <= 55:
                print("纵向跑起来")
                角色纵向移动_通用版()
        数据.全_横向移动方向 = 取横向移动方向(角色坐标[0], 目标x, x偏移)
        print(数据.全_横向移动方向)
        if 数据.全_横向移动方向 != '' and 角色坐标[0] != 目标x:
            if abs(角色坐标[0] - 目标x) <= 55:
                print("横向走起来")
                角色走动_通用版()
            else:
                print("横向跑起来")
                角色跑动_通用版()
    else:
        目标x = 999
        目标y = 0
        if 角色坐标[0] == 目标x or abs(角色坐标[0] - 目标x) <= x偏移:
            if 弹起x:
                弹起(数据.全_横向移动方向)
        if 角色坐标[1] == 目标y or abs(角色坐标[1] - 目标y) <= y偏移:
            if 弹起y:
                弹起(数据.全_纵向移动方向)

        if (角色坐标[0] == 目标x and 角色坐标[1] == 目标y) or (
                abs(角色坐标[0] - 目标x) <= x偏移 and abs(角色坐标[1] - 目标y) <= y偏移):
            if 弹起x:
                弹起(数据.全_横向移动方向)
            if 弹起y:
                弹起(数据.全_纵向移动方向)
            return True
        数据.全_纵向移动方向 = 取纵向移动方向(角色坐标[1], 目标y, y偏移)
        print(数据.全_纵向移动方向)
        if 数据.全_纵向移动方向 != '' and 角色坐标[1] != 目标y:
            if abs(角色坐标[1] - 目标y) <= 55:
                print("纵向跑起来")
                角色纵向移动_通用版()
        数据.全_横向移动方向 = 取横向移动方向(角色坐标[0], 目标x, x偏移)
        print(数据.全_横向移动方向)
        if 数据.全_横向移动方向 != '' and 角色坐标[0] != 目标x:
            if abs(角色坐标[0] - 目标x) <= 55:
                print("横向走起来")
                角色走动_通用版()
            else:
                print("横向跑起来")
                角色跑动_通用版()

        return False


def 自身分解机分解装备():
    pass


def 自动拾取_通用版():
    print("捡物")

    # 按键.release_all_keys()

    with 数据.全局锁:
        所有物品坐标 = 数据.全_所有物品坐标
        # print("开始拾取：", 所有物品坐标, 数据.全_无法拾取)
    # print("捡物222222")
    if 所有物品坐标:
        # print("开始捡物11111111111111111111111111111111111")
        起始时间 = time.time()

        print("开始捡物")
        with 数据.全局锁:
            所有物品坐标 = 数据.全_所有物品坐标
            人物坐标 = 数据.全_角色坐标
        if not 所有物品坐标:
            return
        print(人物坐标, 所有物品坐标)
        物品坐标 = 取最近物品(所有物品坐标, 人物坐标)
        if 数据.全_已中途分解 == False and 判断是否为背包满了():
            自身分解机分解装备()
        数据.全_已中途分解 = True
        if 移动到目标点附近_通用版(物品坐标[0], 物品坐标[1], 10, 6):
            time.sleep(0.15)
            return
        # if time.time() - 起始时间 >= 4:
        #     print("拾取物品超时")
        #     数据.全_无法拾取 = True
        #     return

    # print("捡完了")
    # 按键.release_all_keys()


if __name__ == '__main__':
    time.sleep(2)
    数据.全_纵向移动方向 = 'up'
    数据.全_横向移动方向 = 'right'
    角色纵向移动_通用版()
    角色跑动_通用版()
