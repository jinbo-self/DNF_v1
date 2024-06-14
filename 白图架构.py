import time

import 数据
from 函数功能类 import 从城镇进图, 选图, 设置图内超时, 设置城镇超时, 有疲劳
from 刷图脚本.海伯伦的预言所 import 海伯伦的预言所
from 常用类的初始化 import config, 识字


def 移动到白图副本门口(随机数):
    if 随机数 == 1:
        从城镇进图()


def 白图刷图():
    while True:
        副本名称 = 识字.识字(数据.副本名称)
        设置图内超时()
        print(副本名称)
        if "海伯伦的预言所" in 副本名称:
            海伯伦的预言所()
            config.read("账号.ini")
            config['进度']['已刷次数'] = str(int(config['进度']['已刷次数']) + 1)
            print("通关：",副本名称,"已刷次数：", config['进度']['已刷次数'])
            with open('账号.ini', 'w') as configfile:
                config.write(configfile)

            数据.全_通关次数 += 1
        if "频道" in 副本名称:
            break
        设置图内超时()

        if not 有疲劳() and 识字.识字(数据.副本名称) != "":
            print("角色已完成")
            设置图内超时()
            设置城镇超时()
            break


def 白图():
    随机数 = 0
    config.read("配置.ini")
    脚本模式 = config['配置']['全_脚本模式']
    if 脚本模式 == "海伯伦的预言所":
        随机数 = 1
    移动到白图副本门口(随机数)
    选图()
    while True:
        if 识字.识字(数据.副本名称) == "":
            time.sleep(1)
            continue
        break
    白图刷图()
