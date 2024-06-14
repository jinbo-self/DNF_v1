import threading
import time

import mss
import numpy as np
from ultralytics import YOLO

import 数据
from 其他 import 获取启动时间, 运行清理进程
from 函数功能类 import move_window, DNF获取角色信息, 有疲劳, 设置城镇超时, 回到赛利亚房间, 切换下个角色
from 常用类的初始化 import 按键, config, 识字
from 登录 import 登录
from 白图架构 import 白图, 白图刷图
from 键鼠类 import mouse_mov_click


def 进入主线程():
    print("进入主线程")
    数据.全_刷完 = False
    按键.release_all_keys()
    while True:
        获取启动时间()
        窗口状态 = move_window("地下城与勇士：创新世纪", "地下城与勇士")
        if not 窗口状态:
            print("游戏不存在")
            数据.全_登录 = True
            登录()
            数据.全_登录 = False
            数据.全_登录超时 = 0
        mouse_mov_click(10, 10)
        config.read("配置.ini")
        数据.全_脚本模式 = config['配置']['全_脚本模式']

        if 识字.识字(数据.副本名称) == 数据.全_脚本模式:
            白图刷图()
        if 识字.in城镇():
            DNF获取角色信息()
        if 有疲劳() and 识字.in城镇():
            白图()
        设置城镇超时()
        if not 有疲劳() and 识字.in城镇():
            # 回到赛利亚房间()
            切换下个角色()

        if 数据.全_刷完:
            break
    print("已刷完")
    数据.全_进图 = False
    数据.全_图内超时 = 0

    数据.全_城镇 = False
    数据.全_城镇超时 = 0

    数据.全_登录 = False
    数据.全_登录超时 = 0

    print("关闭游戏")
    运行清理进程()
    print("等待6：30重启")


def 副线程():
    print("进入副线程")
    with mss.mss() as sct:
        model = YOLO("best.pt")
        while True:
            time.sleep(0.01)
            sct_img = sct.grab((0, 0, 800, 600))
            img = np.array(sct_img)[:, :, :3]
            img = img.astype(np.uint8)
            results = model(img)  # 对图像进行预测
            所有门坐标 = []
            所有物品坐标 = []
            所有怪物坐标 = []

            角色坐标 = (999, 999)

            #
            for r in results:
                boxes = r.boxes  # Boxes object for bbox outputs
                # img = r.plot(img=img)
                # #Boss,LittleBoss,Hero,Monster,Door,Object
                for box in boxes:
                    if r.names[int(np.array(box.cls.cpu())[0])] == "Door":
                        门 = np.array(box.xyxy.cpu())[0]
                        所有门坐标.append(((门[2] + 门[0]) / 2, 门[3]))
                    elif r.names[int(np.array(box.cls.cpu())[0])] == "Object":
                        物品 = np.array(box.xyxy.cpu())[0]
                        所有物品坐标.append(((物品[2] + 物品[0]) / 2, 物品[3]))
                    elif (r.names[int(np.array(box.cls.cpu())[0])] == "Boss"
                          or r.names[int(np.array(box.cls.cpu())[0])] == "LittleBoss"
                          or r.names[int(np.array(box.cls.cpu())[0])] == "Monster"):
                        怪物 = np.array(box.xyxy.cpu())[0]
                        所有怪物坐标.append(((怪物[2] + 怪物[0]) / 2, 怪物[3]))
                    elif r.names[int(np.array(box.cls.cpu())[0])] == "Hero":
                        角色 = np.array(box.xyxy.cpu())[0]
                        角色坐标 = ((角色[2] + 角色[0]) / 2, 角色[3])

            with 数据.写锁:
                数据.全_所有门坐标 = 所有门坐标
                数据.全_所有怪物坐标 = 所有怪物坐标
                数据.全_所有物品坐标 = 所有物品坐标
                数据.全_角色坐标 = 角色坐标



if __name__ == '__main__':
    print("开始程序")
    thread = threading.Thread(target=副线程)
    thread.start()
    进入主线程()
    thread.join()
