import threading
import time
import pydirectinput



def mouse_move(x, y):
    """
    移动鼠标到指定的(x, y)坐标位置。
    """
    pydirectinput.moveTo(x, y)


def mouse_click():
    """
    模拟鼠标点击
    """
    pydirectinput.mouseDown()
    time.sleep(0.1)
    pydirectinput.mouseUp()


def mouse_mov_click(x, y):
    mouse_move(int(x), int(y))  # 移动鼠标到(x, y)
    mouse_click()  # 单击鼠标左键


def key_press_release(key_name, delay=0.01):
    """
    模拟按键的长按功能，持续按下指定的键'key_code'，持续时间为'delay'秒。
    """
    # 开始时间
    start_time = time.time()

    # 按下按键
    while (time.time() - start_time) < delay:
        pydirectinput.keyDown(key_name)
        time.sleep(0.01)  # 微小延时

    # 释放按键
    pydirectinput.keyUp(key_name)


def 字符串输入(str):
    for i in range(len(str)):
        key_press_release(str[i])


class KeyController:
    def __init__(self):
        self.events = {}
        self.threads = {}
    def 获取所有按下的事件(self):
        return self.threads
    def key_press(self, key_name):
        """
        启动一个线程来持续按下一个键，直到调用 key_release。
        """
        if key_name in self.threads:
            # 如果已经有线程在运行，先释放
            self.key_release(key_name)

        # 创建一个新的事件
        stop_event = threading.Event()
        self.events[key_name] = stop_event

        # 创建并启动线程
        thread = threading.Thread(target=self._hold_key, args=(key_name, stop_event))
        self.threads[key_name] = thread
        thread.start()

    def key_release(self, key_name):
        """
        释放指定的键。
        """
        if key_name in self.events:
            self.events[key_name].set()  # 触发停止事件
            self.threads[key_name].join()  # 等待线程结束
            del self.events[key_name]  # 清理事件
            del self.threads[key_name]  # 清理线程

    def release_all_keys(self):
        """
        释放所有按下的键。
        """
        for key in list(self.events.keys()):
            self.key_release(key)

    def _hold_key(self, key_name, stop_event):
        """
        线程函数，持续按下键直到事件被设置。
        """
        pydirectinput.keyDown(key_name)
        while not stop_event.is_set():
            pydirectinput.keyDown(key_name)
            time.sleep(0.01)
        pydirectinput.keyUp(key_name)


# 使用示例
if __name__ == "__main__":
    time.sleep(1)
    字符串输入("123456")
