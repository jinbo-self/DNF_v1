import os
import subprocess
import time

import win32gui

import 数据
from 其他 import 运行清理进程, 运行清理wegame, 初始化账号, 输入账户
from 函数功能类 import move_window, 关闭窗口, 进入游戏, 强制停止脚本
from 常用类的初始化 import 识字, config
from 键鼠类 import mouse_mov_click, key_press_release


def 启动WeGame():
    config.read('配置.ini')
    exe_path = config['配置']['wegame路径']
    subprocess.Popen([exe_path])
    while True:
        返回值 = move_window("WeGame", "TWINCONTROL")
        if "账号密码登录" in 识字.识字(数据.wegame_登录):
            数据.全_登录方式 = 1
            break
        elif 识字.识字(数据.wegame_登录) == "登录":
            break
    time.sleep(1)


def 等待登录成功():
    while True:
        if "验证" in 识字.识字(数据.wegame_验证):
            print("出现验证码，请手动输入")
            time.sleep(2)
        句柄 = win32gui.FindWindow("TWINCONTROL", "WeGame")
        rect = win32gui.GetWindowRect(句柄)
        宽度 = rect[2] - rect[0]
        高度 = rect[3] - rect[1]
        if 宽度 > 1250 and 高度 > 800:
            print("登录wegame成功")
            break
    while True:
        返回值 = move_window("WeGame", "TWINCONTROL")
        if 返回值:
            break


def 登录游戏():
    while True:
        if "主页" in 识字.识字(数据.wegame_主页):
            mouse_mov_click((数据.wegame_主页[0] + 数据.wegame_主页[2]) / 2,
                            (数据.wegame_主页[1] + 数据.wegame_主页[3]) / 2)
        if "启动" in 识字.识字(数据.wegame_启动):
            数据.全_游戏更新 = False
            mouse_mov_click((数据.wegame_启动[0] + 数据.wegame_启动[2]) / 2,
                            (数据.wegame_启动[1] + 数据.wegame_启动[3]) / 2)
            break
        if "更新" in 识字.识字(数据.wegame_启动):
            print("游戏可更新")
            mouse_mov_click((数据.wegame_启动[0] + 数据.wegame_启动[2]) / 2,
                            (数据.wegame_启动[1] + 数据.wegame_启动[3]) / 2)
            print("游戏更新中")
            数据.全_游戏更新 = True
    while True:
        窗口状态 = move_window("地下城与勇士：创新世纪", "地下城与勇士")
        if 窗口状态 and "游戏开始" in 识字.识字(数据.游戏开始):
            print("登录游戏成功")
            break


def 选择角色():
    print("选择角色")
    for i in range(3):
        mouse_mov_click(10, 10)
    for i in range(15):
        key_press_release('up')
        time.sleep(0.1)
    config.read('账号.ini')
    数据.全_角色进度 = config['进度']['角色']
    for i in range(int(数据.全_角色进度)):
        key_press_release('right')
        time.sleep(0.1)
    关闭窗口()
    进入游戏()
    关闭窗口()


def 登录():
    数据.全_登录超时 = 0
    数据.全_图内超时 = 0
    数据.全_城镇超时 = 0
    数据.全_城镇 = False
    数据.全_进图 = False
    config.read("配置.ini")
    if config['配置']['自动上号'] == '1':
        if not os.path.exists("账号.ini"):
            config['账号'] = {'0': '123456|跨三A|10'}
            config['进度'] = {'账号': '0', '角色': '0'}
            config['6点30初始化'] = {'初始化': '假'}
            with open('账号.ini', 'w') as configfile:
                config.write(configfile)
        if not os.path.exists("配置.ini"):
            config['配置'] = {'wegame路径': 'D:/WeGame/wegame.exe\n#路径',
                              '当前账号': '0',
                              '自动上号': '1\n#1为自动上号，0非手动',
                              '全_脚本模式': '海伯伦的预言所\n#海伯伦的预言所,随机白图,柯涅恩山,昆法特....目前只有海伯伦'}
            with open('配置.ini', 'w') as configfile:
                config.write(configfile)
        print("WeGame登录")
        数据.全_登录 = True
        数据.全_登录超时 = 0
        运行清理进程()
        运行清理wegame()
        启动WeGame()
        初始化账号()
        输入账户()
        等待登录成功()
        登录游戏()
        选择角色()
    else:
        print("请手动上号")
        强制停止脚本()


if __name__ == '__main__':
    print(识字.识字(数据.游戏开始))
