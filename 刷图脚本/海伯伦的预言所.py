import time

import 数据
from 函数功能类 import 取当前房间, 获取最左门, 获取最上门, 获取最右门, 获取最下门, 打怪, isBoss房间, Boss房间处理, \
    获取技能可用列表, 关闭窗口, 取裂缝房间, 释放技能
from 常用类的初始化 import 按键, 识字
from 键鼠类 import key_press_release, mouse_mov_click
from 高级算法 import 移动到目标点附近_通用版, 自动拾取_通用版, 角色纵向移动_通用版, 角色跑动_通用版


def 海伯伦的预言所单次判断是否过图(房间号):
    当前房间号 = 取当前房间()
    if (房间号 != 当前房间号 and 当前房间号 != (999, 999)) or isBoss房间():
        print("已过图:", 房间号)
        数据.全_无法拾取 = False
        按键.release_all_keys()
        return True
    return False


def 海伯伦的预言所持续判断是否过图(房间号):
    for i in range(200):
        当前房间号 = 取当前房间()
        if 房间号 != 当前房间号 and 当前房间号 != (999, 999):
            print("已过图:", 房间号)
            数据.全_无法拾取 = False
            按键.release_all_keys()
            return True
        time.sleep(0.01)
        with 数据.全局锁:
            所有物品坐标 = 数据.全_所有物品坐标
        if not 所有物品坐标:
            自动拾取_通用版()
            return False
        print("未过图:", 房间号)
        return False


def 海伯伦的预言所过图(房间号):
    print("过图")
    按键.release_all_keys()
    if 房间号 == (4, 1):
        起始时间 = time.time()
        while time.time() - 起始时间 < 数据.全_刷图超时:
            with 数据.全局锁:
                物品坐标 = 数据.全_所有物品坐标
            if 物品坐标 and not 数据.全_超时捡物:
                自动拾取_通用版()
                continue
            with 数据.全局锁:
                当前门坐标 = 数据.全_所有门坐标
            if 当前门坐标:
                门坐标 = 获取最上门(当前门坐标)
                print("门坐标：", 门坐标)
                if 移动到目标点附近_通用版(门坐标[0], 门坐标[1] - 40, 20, 12):
                    continue
            if 海伯伦的预言所单次判断是否过图(房间号):
                数据.全_超时捡物 = False
                return True

            # 按键.release_all_keys()
            # 数据.全_纵向移动方向 = 'up'
            # 角色纵向移动_通用版()
            # return 海伯伦的预言所持续判断是否过图(房间号)
    elif 房间号 == (3, 1):
        with 数据.全局锁:
            角色坐标 = 数据.全_角色坐标
        if 角色坐标:
            if 角色坐标[0] >= 600 and 角色坐标[0] != 999:
                起始时间 = time.time()
                while time.time() - 起始时间 < 数据.全_刷图超时:
                    with 数据.全局锁:
                        物品坐标 = 数据.全_所有物品坐标
                    if 物品坐标 and not 数据.全_超时捡物:
                        自动拾取_通用版()
                        continue
                    with 数据.全局锁:
                        当前门坐标 = 数据.全_所有门坐标
                    if 当前门坐标:
                        门坐标 = 获取最右门(当前门坐标)
                        if 移动到目标点附近_通用版(门坐标[0], 门坐标[1], 20, 12):
                            continue
                    if 海伯伦的预言所单次判断是否过图(房间号):
                        数据.全_超时捡物 = False
                        return True

            else:
                起始时间 = time.time()
                while time.time() - 起始时间 < 数据.全_刷图超时:
                    with 数据.全局锁:
                        物品坐标 = 数据.全_所有物品坐标
                    if 物品坐标:
                        自动拾取_通用版()
                        continue
                    with 数据.全局锁:
                        当前门坐标 = 数据.全_所有门坐标
                    if 当前门坐标:
                        门坐标 = 获取最上门(当前门坐标)
                        if 移动到目标点附近_通用版(800, 434, 20, 12):
                            continue
                    if 海伯伦的预言所单次判断是否过图(房间号):
                        数据.全_超时捡物 = False
                        return True

            # 按键.release_all_keys()
            # 数据.全_横向移动方向 = 'right'
            # 角色跑动_通用版()
            #return 海伯伦的预言所持续判断是否过图(房间号)
    elif 房间号 == (3, 2):
        起始时间 = time.time()
        while time.time() - 起始时间 < 数据.全_刷图超时:
            with 数据.全局锁:
                物品坐标 = 数据.全_所有物品坐标
            if 物品坐标 and not 数据.全_超时捡物:
                自动拾取_通用版()
                continue
            with 数据.全局锁:
                当前门坐标 = 数据.全_所有门坐标
            if 当前门坐标:
                门坐标 = 获取最上门(当前门坐标)
                if 移动到目标点附近_通用版(门坐标[0], 门坐标[1], 20, 12):
                    continue
            if 海伯伦的预言所单次判断是否过图(房间号):
                数据.全_超时捡物 = False
                return True

            # 按键.release_all_keys()
            # 数据.全_纵向移动方向 = 'up'
            # 角色纵向移动_通用版()
            #return 海伯伦的预言所持续判断是否过图(房间号)
    elif 房间号 == (3, 3):
        with 数据.全局锁:
            角色坐标 = 数据.全_角色坐标
        if 角色坐标:
            起始时间 = time.time()
            while time.time() - 起始时间 < 数据.全_刷图超时:
                with 数据.全局锁:
                    物品坐标 = 数据.全_所有物品坐标
                if 物品坐标 and not 数据.全_超时捡物:
                    自动拾取_通用版()
                    continue
                with 数据.全局锁:
                    当前门坐标 = 数据.全_所有门坐标
                if 当前门坐标:
                    门坐标 = 获取最上门(当前门坐标)
                    if 移动到目标点附近_通用版(门坐标[0], 门坐标[1]):
                        continue
                if 海伯伦的预言所单次判断是否过图(房间号):
                    数据.全_超时捡物 = False
                    return True

            # 按键.release_all_keys()
            # 数据.全_横向移动方向 = 'left'
            # 角色跑动_通用版()
            #return 海伯伦的预言所持续判断是否过图(房间号)
    elif 房间号 == (2, 2):
        with 数据.全局锁:
            角色坐标 = 数据.全_角色坐标
        if 角色坐标:
            起始时间 = time.time()
            while time.time() - 起始时间 < 数据.全_刷图超时:
                with 数据.全局锁:
                    物品 = 数据.全_所有物品坐标
                if 物品 and not 数据.全_超时捡物:
                    自动拾取_通用版()
                    continue
                with 数据.全局锁:
                    当前门坐标 = 数据.全_所有门坐标
                if 当前门坐标:
                    门坐标 = 获取最上门(当前门坐标)
                    if 移动到目标点附近_通用版(门坐标[0], 门坐标[1], 20, 12):
                        continue
                if 海伯伦的预言所单次判断是否过图(房间号):
                    数据.全_超时捡物 = False
                    return True

            # 按键.release_all_keys()
            # 数据.全_横向移动方向 = 'right'
            # 角色跑动_通用版()
        # return 海伯伦的预言所持续判断是否过图(房间号)
    elif 房间号 == (2, 3):
        起始时间 = time.time()
        while time.time() - 起始时间 < 数据.全_刷图超时:
            with 数据.全局锁:
                物品坐标 = 数据.全_所有物品坐标
            if 物品坐标 and not 数据.全_超时捡物:
                自动拾取_通用版()
                continue
            if 移动到目标点附近_通用版(800, 0, 20, 12):
                continue
            if 海伯伦的预言所单次判断是否过图(房间号):
                数据.全_超时捡物 = False
                return True

            # 按键.release_all_keys()
            # 数据.全_纵向移动方向 = 'up'
            # 角色纵向移动_通用版()
            # return 海伯伦的预言所持续判断是否过图(房间号)
    elif 房间号 == (2, 1):
        with 数据.全局锁:
            角色坐标 = 数据.全_角色坐标
        if 角色坐标:

            起始时间 = time.time()
            while time.time() - 起始时间 < 数据.全_刷图超时:
                with 数据.全局锁:
                    物品坐标 = 数据.全_所有物品坐标
                if 物品坐标 and not 数据.全_超时捡物:
                    自动拾取_通用版()
                    continue
                if 移动到目标点附近_通用版(0, 0, 20, 12):
                    continue
                if 海伯伦的预言所单次判断是否过图(房间号):
                    数据.全_超时捡物 = False
                    return True

            # 按键.release_all_keys()
            # 数据.全_横向移动方向 = 'left'
            # 角色跑动_通用版()
            # return 海伯伦的预言所持续判断是否过图(房间号)
    elif 房间号 == (1, 1):
        with 数据.全局锁:
            角色坐标 = 数据.全_角色坐标
        if 角色坐标:

            起始时间 = time.time()
            while time.time() - 起始时间 < 数据.全_刷图超时:
                with 数据.全局锁:
                    物品坐标 = 数据.全_所有物品坐标
                if 物品坐标 and not 数据.全_超时捡物:
                    自动拾取_通用版()
                    continue
                if 移动到目标点附近_通用版(688, 432, 20, 12):
                    continue
                if 海伯伦的预言所单次判断是否过图(房间号):
                    数据.全_超时捡物 = False
                    return True

            # 按键.release_all_keys()
            # 数据.全_横向移动方向 = 'right'
            # 角色跑动_通用版()
            # return 海伯伦的预言所持续判断是否过图(房间号)
    elif 房间号 == (1, 2):
        with 数据.全局锁:
            角色坐标 = 数据.全_角色坐标
        if 角色坐标:

            起始时间 = time.time()
            while time.time() - 起始时间 < 数据.全_刷图超时:
                with 数据.全局锁:
                    物品坐标 = 数据.全_所有物品坐标
                if 物品坐标 and not 数据.全_超时捡物:
                    自动拾取_通用版()
                    continue
                if 移动到目标点附近_通用版(688, 432, 20, 12):
                    continue
                if 海伯伦的预言所单次判断是否过图(房间号):
                    数据.全_超时捡物 = False
                    return True

            # 按键.release_all_keys()
            # 数据.全_横向移动方向 = 'right'
            # 角色跑动_通用版()
            # return 海伯伦的预言所持续判断是否过图(房间号)
    elif 房间号 == (1, 3):
        with 数据.全局锁:
            角色坐标 = 数据.全_角色坐标
        if 角色坐标:

            起始时间 = time.time()
            while time.time() - 起始时间 < 数据.全_刷图超时:
                with 数据.全局锁:
                    物品坐标 = 数据.全_所有物品坐标
                if 物品坐标 and not 数据.全_超时捡物:
                    自动拾取_通用版()
                    continue
                if 移动到目标点附近_通用版(688, 432, 20, 12):
                    continue
                if 海伯伦的预言所单次判断是否过图(房间号):
                    数据.全_超时捡物 = False
                    return True

            # 按键.release_all_keys()
            # 数据.全_横向移动方向 = 'right'
            # 角色跑动_通用版()
            # return 海伯伦的预言所持续判断是否过图(房间号)
    数据.全_超时捡物 = True
    return False


def 强制返回等待虚弱():
    关闭窗口()
    key_press_release('esc')
    time.sleep(0.5)
    mouse_mov_click(497, 494)
    time.sleep(0.35)
    key_press_release('space')
    # 等待虚弱状态
    print("等待虚弱状态")
    关闭窗口()
    time.sleep(10)
    while 识字.识字((528, 559, 563, 573)) != '100%':
        print("进度：", 识字.识字((528, 559, 563, 573)))
        time.sleep(30)
        关闭窗口()
    print("虚弱已过")


def 海伯伦的预言所():
    数据.全_已加BUFF = False
    全局放技能 = 0
    while True:
        房间号 = 取当前房间()
        if 房间号 == (4, 1):
            print("房间号", 房间号)
            with 数据.全局锁:
                当前门坐标 = 数据.全_所有门坐标
            if 当前门坐标 or 识字.is开门(房间号):
                print("首图加buff")
                if 全局放技能 == 0:
                    全局放技能 = 1
                    key_press_release('y')

                if 海伯伦的预言所过图(房间号):
                    continue
                else:
                    print("过图超时")
                    移动到目标点附近_通用版(400, 448, 20, 20)
                    time.sleep(2)
        elif 房间号 == (2, 1):
            print("房间号", 房间号)
            技能列表 = 获取技能可用列表()
            释放技能(技能列表)
            with 数据.全局锁:
                当前门坐标 = 数据.全_所有门坐标
            if 当前门坐标 or 识字.is开门(房间号):
                if 海伯伦的预言所过图(房间号):
                    continue
                else:
                    print("过图超时")
                    移动到目标点附近_通用版(400, 448, 20, 20)
                    time.sleep(2)
        elif 房间号 == (2, 3):
            print("房间号", 房间号)
            技能列表 = 获取技能可用列表()
            释放技能(技能列表)
            with 数据.全局锁:
                当前门坐标 = 数据.全_所有门坐标
            if 当前门坐标 or 识字.is开门(房间号):
                if 海伯伦的预言所过图(房间号):
                    continue
                else:
                    print("过图超时")
                    移动到目标点附近_通用版(400, 448, 20, 20)
                    time.sleep(2)
        elif 取裂缝房间() != (999, 999) or (识字.in城镇() and 识字.识字((528, 559, 563, 573)) != '100%'):
            print("发现深渊，强制退出")
            按键.release_all_keys()
            强制返回等待虚弱()
            break
        elif isBoss房间() and "裂缝" not in 识字.识字((612, 241, 726, 280)) and "不稳定" not in 识字.识字(
                (612, 241, 726, 280)):
            print("Boss处理")
            Boss房间处理()  # boss房间捡物，翻牌，售卖，再次,疲劳判断
            break
        elif 房间号 != (999, 999):
            while True:
                打怪()
                with 数据.全局锁:
                    当前门坐标 = 数据.全_所有门坐标
                if isBoss房间() and "裂缝" not in 识字.识字((612, 241, 726, 280)):
                    break
                if 识字.in城镇():
                    print("意外返回城镇")
                    按键.release_all_keys()
                    break
                if 当前门坐标 or 识字.is开门(房间号):
                    if 海伯伦的预言所过图(房间号):
                        # 过图成功
                        break
                    else:
                        print("过图超时")
                        移动到目标点附近_通用版(400, 448, 20, 20)
                        time.sleep(2)



                else:  # 寻怪
                    print("寻怪")
                    当前时间 = time.time()
                    with 数据.全局锁:
                        角色 = 数据.全_角色坐标
                        怪物坐标 = 数据.全_所有怪物坐标
                    if 角色[0] < 450 and not isBoss房间():
                        # 最好判断有无怪物和超时一起

                        while time.time() - 当前时间 < 4 and (怪物坐标 == [] or 怪物坐标 == (0, 0)):
                            if 识字.in城镇():
                                print("意外返回城镇")
                                按键.release_all_keys()
                                break
                            with 数据.全局锁:
                                怪物坐标 = 数据.全_所有怪物坐标
                            移动到目标点附近_通用版(800, 438, 20, 20)
                            time.sleep(0.01)
                        break
                    elif 角色[0] > 450 and not isBoss房间():
                        while time.time() - 当前时间 < 4 and (怪物坐标 == [] or 怪物坐标 == (0, 0)):
                            if 识字.in城镇():
                                print("意外返回城镇")
                                按键.release_all_keys()
                                break
                            with 数据.全局锁:
                                怪物坐标 = 数据.全_所有怪物坐标
                            移动到目标点附近_通用版(0, 497, 20, 20)
                            time.sleep(0.01)
                        break

