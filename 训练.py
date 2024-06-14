
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolov8n.yaml")
    # model = YOLO("last.pt")  # 加载预训练模型（建议用于训练）
    model = YOLO("yolov8n.pt")
    # 使用模型
    model.train(data="coco128.yaml", epochs=100,batch=10,device='cpu')  # 训练模型amp=false可以解决Nan问题

    # metrics = model.val()  # 在验证集上评估模型性能
    # results = model(
    #     r"C:\Users\Administrator\Desktop\文件\代码类\crypto_unicorns_first-master\datasets\coco128\images\train2017\自己.png")  # 对图像进行预测
    # print(len(results))
    # results = model(
    #     r"C:\Users\Administrator\Desktop\文件\代码类\crypto_unicorns_first-master\datasets\coco128\images\train2017\15.png")  # 对图像进行预测
    # print(len(results))
    # for r in results:
    #     boxes = r.boxes  # Boxes object for bbox outputs
    #     for box in boxes:
    #         print("坐标:", np.array(box.xyxy.cpu())[0], "类别序号:", int(np.array(box.cls.cpu())[0]), "类别:",
    #               r.names[int(np.array(box.cls.cpu())[0])])