import asyncio
import json
import pickle
import threading
import time

import mss
import numpy as np
import websockets

from ultralytics import YOLO

import 数据
from 其他 import 获取启动时间, 运行清理进程
from 函数功能类 import move_window, DNF获取角色信息, 有疲劳, 设置城镇超时, 回到赛利亚房间, 切换下个角色, 装备分解
from 常用类的初始化 import 按键, config, 识字
from 登录 import 登录
from 白图架构 import 白图, 白图刷图
from 键鼠类 import mouse_mov_click
from datetime import datetime, timedelta


def 进入主线程():
    print("进入主线程")
    数据.全_刷完 = False
    按键.release_all_keys()
    while True:
        获取启动时间()
        窗口状态 = move_window("地下城与勇士：创新世纪", "地下城与勇士")
        if not 窗口状态:
            print("游戏不存在")
            数据.全_游戏结束 = False
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
            # 添加分解入库功能
            装备分解()

            切换下个角色()

        if 数据.全_刷完:

            数据.全_进图 = False
            数据.全_图内超时 = 0

            数据.全_城镇 = False
            数据.全_城镇超时 = 0

            数据.全_登录 = False
            数据.全_登录超时 = 0

            运行清理进程()
            if 30 > 获取到6点30的时间差() > 0:
                config.read("配置.ini")
                config['配置']['当前账号'] = '0'
                config['配置']['当前角色'] = '0'
                with open('配置.ini', 'w') as configfile:
                    config.write(configfile)

                config.read("账号.ini")
                config['配置']['当前账号'] = '0'
                config['配置']['当前角色'] = '0'
                config['进度']['账号'] = '0'
                config['进度']['角色'] = '0'
                config['进度']['已刷次数'] = '0'
                with open('账号.ini', 'w') as configfile:
                    config.write(configfile)
                数据.全_刷完 = False

            else:
                print("已刷完,等待6：30重启")
                time.sleep(600)
                continue

        if 0 > 获取到6点30的时间差() > -30:
            数据.全_刷完 = True


def 获取到6点30的时间差():
    # 获取当前时间并提取小时和分钟
    now = datetime.now()
    current_time = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)

    # 创建一个 timedelta 对象，表示6小时30分钟
    time_to_subtract = timedelta(hours=6, minutes=30)

    # 计算差值

    time_difference = current_time - time_to_subtract

    # 将差值转换为秒
    seconds_difference = time_difference.total_seconds()

    return seconds_difference


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


async def 副线程1():
    print("进入副线程1")
    uri = "ws://" + 数据.服务端ip + ":12345"
    try:
        async with websockets.connect(uri) as websocket:
            await capture_and_send_image(websocket)
    except Exception as e:
        print(f"Failed to establish connection: {e}")


async def capture_and_send_image(websocket):
    with mss.mss() as sct:
        while True:
            time.sleep(0.01)
            sct_img = sct.grab((0, 0, 800, 600))
            img = np.array(sct_img)[:, :, :3]
            img = img.astype(np.uint8)
            img = pickle.dumps(img)
            try:
                # print("发送数据")
                chunk_size = 1024 * 128  # 每块128KB

                for i in range(0, len(img), chunk_size):
                    chunk = img[i:i + chunk_size]
                    await websocket.send(chunk)
                await websocket.send("EOF")  # 表示传输结束
                response = await websocket.recv()
                result = json.loads(response.decode('utf-8'))
                # print(result)
                with 数据.写锁:
                    数据.全_所有门坐标 = result['所有门坐标']
                    数据.全_所有怪物坐标 = result['所有怪物坐标']
                    数据.全_所有物品坐标 = result['所有物品坐标']
                    数据.全_角色坐标 = result['角色坐标']

            except Exception as e:
                print(f"Connection closed: {e}")
                break


def start_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':
    print("开始程序")
    config.read('配置.ini')
    if config['配置']['在线推理'] == '1':
        # 创建一个新的事件循环
        new_loop = asyncio.new_event_loop()

        # 创建一个线程来运行事件循环
        t = threading.Thread(target=start_event_loop, args=(new_loop,))
        t.start()

        # 在新事件循环中添加异步任务
        asyncio.run_coroutine_threadsafe(副线程1(), new_loop)

        # 运行主线程任务
        进入主线程()
    else:
        thread = threading.Thread(target=副线程)
        thread.start()
        进入主线程()
        thread.join()
