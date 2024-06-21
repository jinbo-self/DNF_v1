import asyncio
import pickle
import socket
import struct
import json

import numpy as np
import websockets
from ultralytics import YOLO



async def process_image(image_data):
    # 这里调用YOLO处理图片，并返回识别的类和坐标
    # 这里假设返回的结果是一个列表，格式如下
    # [{'class': 'person', 'bbox': [x1, y1, x2, y2]}, ...]
    #
    # 使用dummy数据代替实际处理

    results = model(image_data)  # 对图像进行预测
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

    result = {'所有门坐标': 所有门坐标, '所有怪物坐标': 所有怪物坐标, '所有物品坐标': 所有物品坐标,
              '角色坐标': 角色坐标}
    return result
def numpy_type_converter(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj
async def handler(websocket, path):
    buffer = b""
    try:
        async for image_data in websocket:
            # print("Received image data!")
            if image_data == "EOF":
                image_data = pickle.loads(buffer)
                result = await process_image(image_data)
                print(result)
                await websocket.send(json.dumps(result, default=numpy_type_converter).encode('utf-8'))
                buffer = b""
            else:
                buffer += image_data

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        print("Connection cleaned up.")
model = YOLO('best.pt')
start_server = websockets.serve(handler, 'localhost', 12345)
print("Server started at ws://localhost:12345")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



