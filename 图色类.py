from win32com.client import Dispatch


class Demo:
    def __init__(self):
        #创建com对象
        self.op=Dispatch("op.opsoft");
        self.hwnd=0;
        self.send_hwnd=0;
        print("init");
