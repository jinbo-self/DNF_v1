
from ultralytics import YOLO

from 识字类 import 识字初始化
from 键鼠类 import KeyController
import configparser

# 创建配置解析器对象
config = configparser.ConfigParser()
识字 = 识字初始化()
按键 = KeyController()
# subprocess.run(['regsvr32', '/s', 'op_x64.dll'], capture_output=True, text=True)
# op = Dispatch("op.opsoft")

intX = 0
intY = 0
