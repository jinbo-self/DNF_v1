import math
import random
import time

import numpy as np
import win32con
import win32gui
from PIL import Image

import 数据
from 其他 import 初始化账号, 运行清理进程
from 键鼠类 import key_press_release, mouse_mov_click
import heapq
from 常用类的初始化 import 识字, 按键, config
from 高级算法 import 移动到目标点附近_通用版, 取最近物品, is距离近


class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Cost from start to node
        self.h = 0  # Heuristic from node to end
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __lt__(self, other):
        return self.f < other.f


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance


def A星寻路(maze, start, end):
    """A*寻路"""
    start_node = Node(None, tuple(start))
    end_node = Node(None, tuple(end))
    open_list = []
    closed_list = set()

    heapq.heappush(open_list, (start_node.f, start_node))

    while open_list:
        current_node = heapq.heappop(open_list)[1]
        closed_list.add(current_node)

        if current_node == end_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        (x, y) = current_node.position
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for next in neighbors:
            try:
                maze_value = maze[next[0]][next[1]]
            except IndexError:
                continue
            if maze_value == 1:
                continue
            neighbor = Node(current_node, next)

            if neighbor in closed_list:
                continue

            neighbor.g = current_node.g + 1
            neighbor.h = heuristic(neighbor.position, end_node.position)
            neighbor.f = neighbor.g + neighbor.h

            if add_to_open(open_list, neighbor):
                heapq.heappush(open_list, (neighbor.f, neighbor))


def add_to_open(open_list, neighbor):
    for node in open_list:
        if neighbor == node[1] and neighbor.g > node[1].g:
            return False
    return True


# Define the maze


def move_window(title, class_name):
    # 获取窗口句柄
    hwnd = win32gui.FindWindow(class_name, title)
    if hwnd:
        # 移动窗口
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
        return True
    else:
        return False


def 启动游戏():
    pass


def 从城镇进图():
    key_press_release('down', 2)
    key_press_release('1')
    time.sleep(3)
    mouse_mov_click(数据.比拉谢尔面板[0], 数据.比拉谢尔面板[1])
    time.sleep(0.5)
    mouse_mov_click(数据.比拉谢尔面板_毁坏的克洛诺斯岛[0], 数据.比拉谢尔面板_毁坏的克洛诺斯岛[1])
    key_press_release('space')
    time.sleep(0.5)
    key_press_release('right', 5)


def 进入赛利亚房间():
    key_press_release('esc')
    time.sleep(0.01)
    mouse_mov_click(数据.设置_选择角色[0], 数据.设置_选择角色[1])
    time.sleep(0.5)
    key_press_release('space')  # 模拟空格键单击


def 关闭公告():
    mouse_mov_click((数据.公告_关闭[0] + 数据.公告_关闭[2]) / 2, (数据.公告_关闭[1] + 数据.公告_关闭[3]) / 2)


def 选图():
    次数 = 0
    while 识字.获取所选地图名称() != 数据.全_脚本模式:
        key_press_release('down')
    for i in range(5):
        key_press_release('left')
        time.sleep(0.1)
    if 数据.全_角色名望 >= 33989:  # 冒险
        次数 = 4
    elif 数据.全_角色名望 >= 29369:  # 冒险
        次数 = 3
    elif 数据.全_角色名望 >= 23259:  # 冒险
        次数 = 2
    elif 数据.全_角色名望 >= 13195:  # 冒险
        次数 = 1
    for i in range(次数):
        key_press_release('right')
        time.sleep(0.1)
    key_press_release('space')


def 打怪():
    #
    print("打怪")
    with 数据.全局锁:
        怪物坐标 = 数据.全_所有怪物坐标
    按键.release_all_keys()
    if 怪物坐标 == (0, 0):
        return
    while 怪物坐标:
        print("跑到目标", 怪物坐标)

        with 数据.全局锁:
            人物坐标 = 数据.全_角色坐标
            所有怪物坐标 = 数据.全_所有怪物坐标
        怪物坐标 = 取最近物品(所有怪物坐标, 人物坐标)
        if isBoss房间() and "裂缝" not in 识字.识字((612, 241, 726, 280)) or 识字.in城镇():
            print("Boss返回")
            # Boss房间处理()  # boss房间捡物，翻牌，售卖，再次,疲劳判断
            break
        if 怪物坐标 == (0, 0):
            break
        print("走进目标", 怪物坐标)
        技能列表 = 获取技能可用列表()
        if 移动到目标点附近_通用版(怪物坐标[0], 怪物坐标[1], 120, 40):
            按键.release_all_keys()
            释放技能(技能列表)
        with 数据.全局锁:
            人物坐标 = 数据.全_角色坐标
            所有怪物坐标 = 数据.全_所有怪物坐标
        怪物坐标 = 取最近物品(所有怪物坐标, 人物坐标)

        if 人物坐标 == (999, 999):  #被遮挡
            keys = "qwertasdfghx"
            random_key = random.choice(keys)
            key_press_release(random_key)
        技能列表 = 获取技能可用列表()
        按键.release_all_keys()
        释放技能(技能列表)
        with 数据.全局锁:
            人物坐标 = 数据.全_角色坐标
            所有怪物坐标 = 数据.全_所有怪物坐标
        怪物坐标 = 取最近物品(所有怪物坐标, 人物坐标)
        if 怪物坐标 == (0, 0):
            break
    按键.release_all_keys()


def 捡物():
    物品坐标 = 获取物品坐标()
    while 物品坐标 != (0, 0):
        # print("跑到目标", 怪物坐标)
        人物坐标 = 获取人物坐标()
        while not is距离近(人物坐标, 物品坐标, 40, 40) and 物品坐标 != (0, 0):
            if is距离近(人物坐标, 物品坐标, 120, 120):
                走到目标(物品坐标)
                key_press_release('x')
            人物坐标 = 获取人物坐标()
            物品坐标 = 获取物品坐标()
            # print("人物坐标", 人物坐标, "怪物坐标", 怪物坐标)
            跑到目标(物品坐标, 识字)

            if 人物坐标 == (999, 999):  # 被遮挡往中间跑
                跑到目标((428, 379), 识字)
        # print("获取技d能列表")
        key_press_release('x')
        # print("释放技能:", 技能列表)
        物品坐标 = 获取物品坐标()
        # print("获取怪物坐标：", 怪物坐标)
    按键.release_all_keys()


def 过图(房间号):
    """直接写死得了"""

    当前房间 = 取当前房间()
    上个房间 = 当前房间
    print(当前房间, 上个房间, 获取怪物坐标())
    路径算法 = A星寻路(数据.小地图路径.地图数据, 当前房间, 数据.小地图路径.终点)
    当前路径 = 路径算法.index(当前房间)
    # 小地图的xy与像素点坐标的xy居然是相反的。。。。。
    if 当前路径 != len(路径算法) + 1:
        下个房间走法 = 路径算法[当前路径 + 1]
        index = 1
        while 当前房间 == 上个房间 or 获取怪物坐标() == (0, 0):
            # 0,0  0,1  0,2
            # 1,0  1,1  1,2
            # 2,0  2,1  2,2
            print(当前房间, 上个房间)
            所有门坐标 = 获取门坐标()
            当前房间 = 取当前房间()
            人物坐标 = 获取人物坐标()
            if isBoss房间():
                break
            if 人物坐标 == (999, 999):
                跑到目标((392, 272))
                if 当前房间 != 上个房间 or 获取怪物坐标() != (0, 0):
                    break
            if 当前房间 == (999, 999):
                continue
            # direction = (下个房间走法[0] - 当前房间[0], 下个房间走法[1] - 当前房间[1])

            if not 所有门坐标:
                key_press_release('right')
                按键.key_press('right')
                time.sleep(1)
                按键.release_all_keys()
                if 当前房间 != 上个房间 or 获取怪物坐标() != (0, 0):
                    break
            if index == 1:
                index = index + 1
                key_press_release('right')
                按键.key_press('right')
                time.sleep(1)
                if 当前房间 != 上个房间 or 获取怪物坐标() != (0, 0):
                    break
            所有门坐标 = 获取门坐标()
            if 当前房间 == (4, 1) and 所有门坐标 != []:
                跑到目标(所有门坐标[0])
                if 当前房间 != 上个房间 or 获取怪物坐标() != (0, 0):
                    break
            elif 所有门坐标:  # 右边或者上边都行
                w = 0
                best_door = None
                if len(所有门坐标) == 1:  # 一个门的话只可能是右边或者上边
                    跑到目标(所有门坐标[0])
                    if 当前房间 != 上个房间 or 获取怪物坐标() != (0, 0):
                        break
                else:
                    # 往上边走
                    for 门坐标 in 所有门坐标:
                        if 门坐标[0] > w:
                            w = 门坐标[0]
                            best_door = 门坐标
                    跑到目标(best_door)
                    if 当前房间 != 上个房间 or 获取怪物坐标() != (0, 0):
                        break

            # for 门坐标 in 所有门坐标:
            #     print(门坐标, 人物坐标, 下个房间走法, 当前房间)
            #     if direction == (0, 1) and 门坐标[0]+门坐标偏移 > 人物坐标[0]:  #右边
            #         distance = abs(门坐标[0] - 人物坐标[0])
            #         if distance > max_distance:
            #             max_distance = distance
            #             best_door = 门坐标
            #     elif direction == (0, -1) and 门坐标[0]-门坐标偏移 < 人物坐标[0]:  #左边
            #         distance = abs(门坐标[0] - 人物坐标[0])
            #         if distance > max_distance:
            #             max_distance = distance
            #             best_door = 门坐标
            #     elif direction == (1, 0) and 门坐标[1]+门坐标偏移 >人物坐标[1]:  #下边
            #         distance = abs(门坐标[0] - 人物坐标[0])
            #         if distance > max_distance:
            #             max_distance = distance
            #             best_door = 门坐标
            #     elif direction == (-1, 0) and 门坐标[1]-门坐标偏移 < 人物坐标[1]:  #上边
            #         distance = abs(门坐标[0] - 人物坐标[0])
            #         if distance > max_distance:
            #             max_distance = distance
            #             best_door = 门坐标
            # best_door = 所有门坐标[0]
            # print(best_door)
            # if best_door is None:
            #     按键.release_all_keys()
            #     按键.key_press('up')
            #     按键.key_press('right')
            #     # if direction == (0, 1):  # 右边
            #     #     按键.key_press('right')
            #     # elif direction == (0, -1):  # 左边
            #     #     按键.key_press('left')
            #     # elif direction == (1, 0):  # 下边
            #     #     按键.key_press('down')
            #     # elif direction == (-1, 0):  # 上边
            #     #     按键.key_press('up')
            # else:
            #     跑到目标(best_door)
            # 当前房间 = 取当前房间()

    按键.release_all_keys()


def 获取人物坐标():
    sct = 识字.get_sct()
    sct_img = sct.grab((0, 0, 800, 600))
    img = np.array(sct_img)[:, :, :3]
    img = img.astype(np.uint8)
    results = model(img)  # 对图像进行预测
    #
    for r in results:
        boxes = r.boxes  # Boxes object for bbox outputs
        # img = r.plot(img=img)

        for box in boxes:
            if r.names[int(np.array(box.cls.cpu())[0])] == "Hero":
                loc = np.array(box.xyxy.cpu())[0]
                return (loc[2] + loc[0]) / 2, loc[3]
    return 999, 999


def 获取怪物坐标():
    """Class可以为怪物，物品，门"""
    sct = 识字.get_sct()
    sct_img = sct.grab((0, 0, 800, 600))
    img = np.array(sct_img)[:, :, :3]
    img = img.astype(np.uint8)
    results = model(img)  # 对图像进行预测
    tmp = []
    loc = (0, 0)
    人物坐标 = (0, 0)
    for r in results:
        boxes = r.boxes  # Boxes object for bbox outputs
        # img = r.plot(img=img)
        # #Boss,LittleBoss,Hero,Monster,Door,Object
        for box in boxes:
            if (r.names[int(np.array(box.cls.cpu())[0])] == "Boss"
                    or r.names[int(np.array(box.cls.cpu())[0])] == "LittleBoss"
                    or r.names[int(np.array(box.cls.cpu())[0])] == "Monster"):
                person = np.array(box.xyxy.cpu())[0]
                tmp.append(((person[2] + person[0]) / 2, person[3]))

    min_distance = float('inf')  # 初始化最小距离为无穷大
    if tmp != []:
        for (x, y) in tmp:
            distance = math.sqrt((x - 人物坐标[0]) ** 2 + (y - 人物坐标[1]) ** 2)  # 计算距离
            if distance < min_distance:
                min_distance = distance
                loc = (x, y)
    return loc


def 获取物品坐标():
    """Class可以为怪物，物品，门"""
    sct = 识字.get_sct()
    sct_img = sct.grab((0, 0, 800, 600))
    img = np.array(sct_img)[:, :, :3]
    img = img.astype(np.uint8)
    results = model(img)  # 对图像进行预测
    tmp = []
    loc = (0, 0)
    人物坐标 = (0, 0)
    for r in results:
        boxes = r.boxes  # Boxes object for bbox outputs
        # img = r.plot(img=img)
        # #Boss,LittleBoss,Hero,Monster,Door,Object
        for box in boxes:
            if r.names[int(np.array(box.cls.cpu())[0])] == "Object":
                person = np.array(box.xyxy.cpu())[0]
                tmp.append(((person[2] + person[0]) / 2, person[3]))

    min_distance = float('inf')  # 初始化最小距离为无穷大

    if tmp != []:
        for (x, y) in tmp:
            distance = math.sqrt((x - 人物坐标[0]) ** 2 + (y - 人物坐标[1]) ** 2)  # 计算距离
            if distance < min_distance:
                min_distance = distance
                loc = (x, y)
    return loc


def 获取门坐标():
    sct = 识字.get_sct()
    sct_img = sct.grab((0, 0, 800, 600))
    img = np.array(sct_img)[:, :, :3]
    img = img.astype(np.uint8)
    results = model(img)  # 对图像进行预测
    tmp = []
    #
    for r in results:
        boxes = r.boxes  # Boxes object for bbox outputs
        # img = r.plot(img=img)
        # #Boss,LittleBoss,Hero,Monster,Door,Object
        for box in boxes:
            if r.names[int(np.array(box.cls.cpu())[0])] == "Door":
                person = np.array(box.xyxy.cpu())[0]
                tmp.append(((person[2] + person[0]) / 2, person[3]))
    return tmp


def 取当前房间():
    """先扫描颜色，再确定坐标，计算出房间号"""
    sct = 识字.get_sct()
    sct_img = sct.grab(数据.小地图位置)
    img = Image.frombytes('RGB', (sct_img.width, sct_img.height), sct_img.rgb)

    # 加载图像的像素数据
    pixels = img.load()
    行数 = len(数据.小地图路径.地图数据)
    列数 = len(数据.小地图路径.地图数据[0])
    房间宽度 = (数据.小地图位置[2] - 数据.小地图位置[0]) / 列数
    房间高度 = (数据.小地图位置[3] - 数据.小地图位置[1]) / 行数

    # 遍历每个像素
    for x in range(0, img.width, 数据.小地图遍历步长):
        for y in range(0, img.height, 数据.小地图遍历步长):
            # 获取位于 (x, y) 的像素的 RGB 颜色值
            color = pixels[x, y]
            if 数据.小地图角色颜色[0] > color[0] and color[1] > 数据.小地图角色颜色[1] and color[2] > \
                    数据.小地图角色颜色[2]:
                # 向下取整
                返回值 = (int(y // 房间宽度), int(x // 房间高度))
                return 返回值
    返回值 = (999, 999)
    return 返回值


def 取Boss房间():
    """先扫描颜色，再确定坐标，计算出房间号"""
    sct = 识字.get_sct()
    sct_img = sct.grab(数据.小地图位置)
    img = Image.frombytes('RGB', (sct_img.width, sct_img.height), sct_img.rgb)

    # 加载图像的像素数据
    pixels = img.load()
    行数 = len(数据.小地图路径.地图数据)
    列数 = len(数据.小地图路径.地图数据[0])
    房间宽度 = (数据.小地图位置[2] - 数据.小地图位置[0]) / 列数
    房间高度 = (数据.小地图位置[3] - 数据.小地图位置[1]) / 行数

    # 遍历每个像素
    for x in range(0, img.width, 数据.小地图遍历步长):
        for y in range(0, img.height, 数据.小地图遍历步长):
            # 获取位于 (x, y) 的像素的 RGB 颜色值
            color = pixels[x, y]  #200,100
            if 数据.小地图Boss颜色[0] + 5 > color[0] > 数据.小地图Boss颜色[0] - 5 \
                    and 数据.小地图Boss颜色[1] + 5 > color[1] > 数据.小地图Boss颜色[1] - 5 \
                    and 数据.小地图Boss颜色[2] + 5 > color[2] > 数据.小地图Boss颜色[2] - 5:
                # 向下取整
                返回值 = (int(y // 房间宽度), int(x // 房间高度))
                # print(数据.小地图位置[0]+x,数据.小地图位置[1]+y)
                return 返回值
    返回值 = (999, 999)
    return 返回值


def 取裂缝房间():
    """先扫描颜色，再确定坐标，计算出房间号"""
    sct = 识字.get_sct()
    sct_img = sct.grab(数据.小地图位置)
    img = Image.frombytes('RGB', (sct_img.width, sct_img.height), sct_img.rgb)

    # 加载图像的像素数据
    pixels = img.load()
    行数 = len(数据.小地图路径.地图数据)
    列数 = len(数据.小地图路径.地图数据[0])
    房间宽度 = (数据.小地图位置[2] - 数据.小地图位置[0]) / 列数
    房间高度 = (数据.小地图位置[3] - 数据.小地图位置[1]) / 行数

    # 遍历每个像素
    for x in range(0, img.width, 数据.小地图遍历步长):
        for y in range(0, img.height, 数据.小地图遍历步长):
            # 获取位于 (x, y) 的像素的 RGB 颜色值
            color = pixels[x, y]  #200,100
            if color[0] == 255:
                # 向下取整
                返回值 = (int(y // 房间宽度), int(x // 房间高度))
                # print(数据.小地图位置[0]+x,数据.小地图位置[1]+y)
                return 返回值
    返回值 = (999, 999)
    return 返回值


def isBoss房间():
    if 识字.识字(数据.小地图名字) != "" and 取当前房间() == (999, 999) and 取Boss房间() != (999, 999):
        return True
    else:
        return False


def Boss房间处理():
    按键.release_all_keys()
    while "挑战" not in 识字.识字((624, 75, 700, 100)):
        if "跳过" in 识字.识字(数据.跳过):
            key_press_release('esc')
            time.sleep(0.5)
            break
        key_press_release('ctrl')
        key_press_release('alt')
        技能列表 = 获取技能可用列表()
        if 'ctrl' in 技能列表:
            key_press_release('ctrl')
        elif 'alt' in 技能列表:
            key_press_release('alt')
        else:
            释放技能(技能列表)
        if 识字.in城镇():
            return

    key_press_release('v')
    time.sleep(1.5)
    key_press_release('a')
    time.sleep(0.5)
    key_press_release('space')
    time.sleep(0.5)
    key_press_release('left')
    time.sleep(0.5)
    key_press_release('space')
    time.sleep(0.5)
    key_press_release('esc')
    time.sleep(0.5)
    key_press_release('f10')
    if 有疲劳():
        key_press_release('f10')
    else:
        key_press_release('f12')
    time.sleep(5)


def 有疲劳():
    sct = 识字.get_sct()
    sct_img = sct.grab(数据.疲劳位置)
    rgb = np.array(sct_img)
    color = rgb[0, 0]
    color = (color[2], color[1], color[0])
    # print(color)
    # if color[0] == 数据.疲劳颜色[0] \
    #         and 数据.疲劳颜色[1] - 40 < color[1] < 数据.疲劳颜色[1] + 40 \
    #         and 数据.疲劳颜色[2] - 40 < color[2] < 数据.疲劳颜色[2] + 40:
    with 数据.全局锁:
        人物坐标 = 数据.全_角色坐标
    if color[0] < 10 and color[1] < 10 and color[2] < 10 and 人物坐标 != (999, 999):
        return False
    else:
        return True


def 释放技能(技能列表):
    print("释放技能")
    临时 = ['alt', 'ctrl']
    技能总览 = [direction for direction in 技能列表 if direction not in 临时]
    if 技能总览:
        技能 = random.choice(技能总览)
        key_press_release(技能)
        return

    key_press_release(random.choice(['q', 'w', 'e', 'r', 't', 'x'
                                                              'a', 's', 'd', 'f', 'g', 'h']))


def 获取技能可用列表():
    """先扫描颜色，再确定坐标，计算出技能位置"""
    sct = 识字.get_sct()
    sct_img = sct.grab(数据.技能位置)
    img = Image.frombytes('RGB', (sct_img.width, sct_img.height), sct_img.rgb)

    # 加载图像的像素数据qwerty ctl
    pixels = img.load()
    行数 = 2
    列数 = 7
    可用技能列表 = []
    技能宽度 = img.width / 列数
    技能高度 = img.height / 行数
    for x in range(0, img.width, 数据.小地图遍历步长):
        for y in range(0, img.height, 数据.小地图遍历步长):
            # 获取位于 (x, y) 的像素的 RGB 颜色值
            color = pixels[x, y]
            if color[0] == 数据.技能颜色[0] and color[1] == 数据.技能颜色[1]:  # 这里最好改成某个范围内
                可用技能列表.append(数据.技能字典[int(y // 技能高度), int(x // 技能宽度)])
                continue

    return list(set(可用技能列表))  # 去重


def 关闭窗口():
    """关闭公告和esc窗口"""
    key_press_release('esc')
    time.sleep(0.35)
    for i in range(5):
        字符 = 识字.识字(数据.公告_关闭)
        if "关闭" in 字符:
            print("关闭公告")
            time.sleep(0.35)
            mouse_mov_click((数据.公告_关闭[0] + 数据.公告_关闭[2]) / 2, (数据.公告_关闭[1] + 数据.公告_关闭[3]) / 2)
            time.sleep(0.35)
        字符 = 识字.识字(数据.游戏设置)
        if "游戏设置" in 字符:
            print("关闭窗口")
            key_press_release('esc')
            time.sleep(0.35)


def 制裁识别():
    字符 = 识字.识字(数据.公告_关闭)
    if "制裁" in 字符:
        print("制裁中")
        return True
    return False


def 保存配置A():
    config.read('配置.ini')
    config['配置']['运行时长'] = 数据.全_运行时长
    config['配置']['通关次数'] = 数据.全_通关次数
    config['配置']['完成角色'] = 数据.全_完成角色
    with open('配置.ini', 'w') as configfile:
        config.write(configfile)


def 设置图内超时():
    数据.全_进图 = True
    数据.全_图内超时 = 0
    数据.全_城镇 = False
    数据.全_城镇超时 = 0


def 设置城镇超时():
    数据.全_进图 = False
    数据.全_图内超时 = 0
    数据.全_城镇 = True
    数据.全_城镇超时 = 0


def 强制停止脚本():
    print("强行停止")
    按键.release_all_keys()
    数据.全_关闭主线程 = True
    数据.全_关闭副线程 = True
    保存配置A()
    设置图内超时()
    设置城镇超时()
    数据.全_登录超时 = 0
    数据.全_图内超时 = 0
    数据.全_城镇超时 = 0
    数据.全_城镇 = False
    数据.全_进图 = False
    数据.全_暂停 = False
    数据.全_启动 = False


def 制裁停止():
    if 制裁识别():
        强制停止脚本()


def 进入游戏():
    print("进入游戏")
    for i in range(5):
        mouse_mov_click(10, 10)
        制裁停止()
        字符 = 识字.识字(数据.频道)
        if "频道" in 字符:
            time.sleep(0.2)
            print("已经进入赛利亚房间")
            关闭窗口()
            break
        else:
            key_press_release('space')
        time.sleep(1)
    制裁停止()


def 领取在线奖励():
    pass


def 打开菜单():
    for i in range(5):
        if "游戏设置" in 识字.识字(数据.游戏设置):
            print("打开菜单成功")
            break
        time.sleep(0.35)
        mouse_mov_click(10, 10)
        time.sleep(0.35)
        key_press_release('esc')
        time.sleep(0.35)


def 切换到选择角色界面():
    打开菜单()
    for i in range(5):
        if "游戏开始" in 识字.识字(数据.游戏开始):
            print("切换到选择角色界面")
            time.sleep(3)
            return True
        if "选择角色" in 识字.识字(数据.选择角色):
            time.sleep(0.5)
            mouse_mov_click((数据.选择角色[0] + 数据.选择角色[2]) / 2,
                            (数据.选择角色[1] + 数据.选择角色[3]) / 2)
            time.sleep(0.5)
    return False


def 回到赛利亚房间():
    if not 识字.in赛利亚房间():
        print("回到赛利亚房间")
        if 切换到选择角色界面():
            进入游戏()
            return True
        return False
    print("角色在赛利亚房间")
    return True


def 关闭成长指南():
    if "成长" in 识字.识字(数据.成长指南):
        key_press_release('esc')
        time.sleep(0.35)
        关闭窗口()


def 计算角色身高():
    pass


def 打开角色信息():
    while True:
        if "个人信息" in 识字.识字(数据.个人信息):
            print("打开角色信息成功")
            time.sleep(0.1)
            break
        time.sleep(0.5)
        key_press_release('m')


def 获取角色等级():
    pass


def 获取角色职业():
    pass


def 获取角色名望值():
    数据.全_角色名望 = int(识字.识字(数据.角色名望位置).replace(',', ''))
    print(数据.全_角色名望)
    关闭窗口()


def 获取角色职业类型():
    pass


def DNF获取角色信息():
    关闭窗口()
    领取在线奖励()
    回到赛利亚房间()
    关闭成长指南()
    计算角色身高()
    打开角色信息()
    获取角色等级()
    获取角色职业()
    获取角色名望值()
    获取角色职业类型()


def 获取角色疲劳():
    有疲劳()


def 获取最左门(当前门坐标):
    """x最小的那个"""
    loc = (0, 0)
    min_distance = float('inf')  # 初始化最小距离为无穷大
    for (x, y) in 当前门坐标:
        if x < min_distance:
            min_distance = x
            loc = (x, y)
    return loc


def 获取最上门(当前门坐标):
    """y最小的那个"""
    loc = (0, 0)
    min_distance = float('inf')  # 初始化最小距离为无穷大
    for (x, y) in 当前门坐标:
        if y < min_distance:
            min_distance = y
            loc = (x, y)
    return loc


def 获取最下门(当前门坐标):
    """y最大的那个"""
    loc = (0, 0)
    max_distance = 0  # 初始化最小距离为无穷大
    for (x, y) in 当前门坐标:
        if y > max_distance:
            max_distance = y
            loc = (x, y)
    return loc


def 获取最右门(当前门坐标):
    """x最大的那个"""
    loc = (0, 0)
    max_distance = 0  # 初始化最小距离为无穷大
    for (x, y) in 当前门坐标:
        if x > max_distance:
            max_distance = x
            loc = (x, y)
    return loc


def 切换下个角色():
    print("切换到下个角色")
    按键.release_all_keys()
    初始化账号()
    if int(数据.全_角色进度) < int(数据.全_角色数):
        切换到选择角色界面()
        key_press_release('right')
        进入游戏()
        config.read("账号.ini")
        config['进度']['角色'] = str(int(config['进度']['角色']) + 1)
        with open('账号.ini', 'w') as configfile:
            config.write(configfile)
    else:
        config.read("账号.ini")
        config['进度']['角色'] = '0'
        config['进度']['账号'] = str(int(config['进度']['角色']) + 1)
        with open('账号.ini', 'w') as configfile:
            config.write(configfile)
        if 初始化账号():
            数据.全_刷完 = False
            print("换号")
            运行清理进程()
            time.sleep(5)
        else:
            数据.全_刷完 = True
            config.read("账号.ini")
            config['进度']['角色'] = '0'
            config['进度']['账号'] = '0'
            with open('账号.ini', 'w') as configfile:
                config.write(configfile)
    config.read("账号.ini")

    数据.全_账号进度 = config['进度']['账号']
    数据.全_角色进度 = config['进度']['角色']
    数据.全_完成角色 += 1


# 调用函数
if __name__ == '__main__':
    print(有疲劳())
    # time.sleep(2)
    # while not isBoss房间(识字):
    #     过图(识字)
    # Boss房间处理(识字)
