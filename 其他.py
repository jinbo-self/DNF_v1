import time

import psutil

import 数据
from 常用类的初始化 import config, 识字
from 键鼠类 import mouse_mov_click, key_press_release, 字符串输入


def 获取启动时间():
    if 数据.全_启动时间 == "":
        数据.全_启动时间 = time.time()


def 终止进程(process_name):
    """
    终止所有与给定名称匹配的进程。

    :param process_name: 要终止的进程名称
    """
    # 遍历所有正在运行的进程
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # 检查进程名称是否匹配
            if proc.info['name'] == process_name:
                # 终止进程
                proc.terminate()
                print(f"Terminated process {proc.info['name']} with PID {proc.info['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def 运行清理进程():
    终止进程("DNFchina.exe")
    终止进程("DNFchinaTest.exe")
    终止进程("Client.exe")
    终止进程("DNF.exe")
    终止进程("AdvertDialog.exe")
    终止进程("AdvertTips.exe")
    终止进程("WerFault.exe")
    终止进程("QQDL.exe")
    终止进程("ExceptionReport.exe")
    终止进程("QQLogin.exe")
    终止进程("TenSafe.exe")
    终止进程("TenSafe_1.exe")
    终止进程("Repair.exe")
    终止进程("Tencentdl.exe")
    终止进程("TASLogin.exe")
    终止进程("bugreport.exe")
    终止进程("DirverInject.exe")
    终止进程("TenioDL.exe")
    终止进程("iexplore.exe")
    终止进程("DNF.exe")
    终止进程("GameLoader.exe")
    终止进程("TesService.exe")
    终止进程("rundll32.exe")
    终止进程("TPHelper.exe")
    终止进程("tgp_gamead.exe")
    终止进程("tgp_daemon.exe")
    终止进程("wegame.exe")


def 运行清理wegame():
    终止进程("tgp_gamead.exe")
    终止进程("tgp_daemon.exe")
    终止进程("wegame.exe")


def 初始化账号():
    print("初始化账号信息")
    config.read('账号.ini')
    数据.全_账号进度 = config['进度']['账号']
    数据.全_角色进度 = config['进度']['角色']
    try:
        数据.全_账号信息 = config['账号'][数据.全_账号进度]
        字符 = 数据.全_账号信息.split('|')
        if len(字符) == 3:
            数据.全_账号 = 字符[0]
            数据.全_跨区 = 字符[1]
            数据.全_角色数 = 字符[2]
            print("数据.全_账号进度：",数据.全_账号进度,"角色数量:",数据.全_角色数,"跨区：",数据.全_跨区)
            return True
    except Exception as E:
        return False


def 输入账户():
    if 数据.全_登录方式 == 1:
        mouse_mov_click((数据.wegame_登录[0] + 数据.wegame_登录[2]) / 2,
                        (数据.wegame_登录[1] + 数据.wegame_登录[3]) / 2)
        time.sleep(1)
    mouse_mov_click(数据.wegame_账户[0], 数据.wegame_账户[1])

    for i in range(20):
        key_press_release('backspace')
        time.sleep(0.03)
    字符串输入(数据.全_账号)
    time.sleep(0.35)
    while "登录" in 识字.识字(数据.wegame_登录):
        mouse_mov_click((数据.wegame_登录[0] + 数据.wegame_登录[2]) / 2,
                        (数据.wegame_登录[1] + 数据.wegame_登录[3]) / 2)


if __name__ == '__main__':
    config.read('账号.ini')
    print(config['进度']['账号'])
    print(config['进度']['角色'])
    数据.全_账号进度 = config['进度']['账号']
    print(config['账号'][数据.全_账号进度])
    字符 = config['账号'][数据.全_账号进度].split('|')
    print(字符)
    if len(字符) == 3:
        数据.全_账号 = 字符[0]
        数据.全_跨区 = 字符[1]
        数据.全_角色数 = 字符[2]
        print(数据.全_账号, 数据.全_跨区, 数据.全_角色数)
