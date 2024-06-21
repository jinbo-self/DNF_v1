import socket
import struct
import json

import numpy as np
from ultralytics import YOLO

model = YOLO("best.pt")


def process_image(image_data):
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


def main():
    server_address = ('0.0.0.0', 12345)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print('Server is listening...')

    while True:
        connection, client_address = server_socket.accept()
        try:
            data = connection.recv(4)
            if not data:
                break
            # 获取图片数据的长度
            image_size = struct.unpack('>I', data)[0]
            image_data = connection.recv(image_size)  # 接收图片数据

            result = process_image(image_data)  # 处理图片

            # 发送处理结果
            result_data = json.dumps(result).encode('utf-8')
            connection.sendall(struct.pack('>I', len(result_data)) + result_data)

        finally:
            connection.close()


if __name__ == '__main__':
    main()
