import time

import adb_tool
import mission
import webui
import sys, os
import PyQt5
import threading
from enum import Enum

#截图：image[ymin:ymax,xmin:xmax]


class HK2_script:
    class States(Enum):
        NoDevice = -1  # 没有找到device
        Connecting = 1  # 尝试连接
        NoMission = 2  # 闲置中
        WorkOnMission = 3  # 执行任务中

    def __init__(self):
        self.serial = "127.0.0.1:5555"
        self.state = self.States.NoDevice
        self.device = None
        self.connect_timeout = 1
        self.reconnect_flag = True

        self.mqueue = mission.MissionQueue(self)
        self.mqueue.mthread.start()
        self.webui = None

        self.connect_thread = threading.Thread(target = self.connect,name= "connect_thread")
        self.connect_thread_event = threading.Event()
        self.check_thread_event = threading.Event()
        self.check_device_thread = threading.Thread(target = self.check_device,name = "check_device_thread")
        self.state_lock = threading.Lock()

        self.mqueue.add("重启设置")
        self.mqueue.mthread.resume()

    def start_thread(self):
        self.check_device_thread.start()
        self.connect_thread.start()
        self.check_thread_event.set()

    def connect(self):
        while(True):
            self.connect_thread_event.wait()
            print("connect to:", self.serial)
            self.change_state(self.States.Connecting, self.serial)
            try:
                adb_tool.connect(self.serial, self.connect_timeout)
                self.connect_pause()
            except:
                print("connect failed...")

    def connect_resume(self):
        self.connect_thread_event.set()
        self.check_thread_event.clear()
    def connect_pause(self):
        self.connect_thread_event.clear()
        self.check_thread_event.set()

    def check_device(self):
        while(True):
            self.check_thread_event.wait()
            try:
                self.device.info
                if(self.reconnect_flag):
                    self.change_state(self.States.NoMission)
                    self.reconnect_flag = False
                time.sleep(5)
            except:
                print("Nodevice")
                self.reconnect_flag = True
                self.change_state(self.States.NoDevice)
                self.connect_resume()
                time.sleep(self.connect_timeout)
                self.device = adb_tool.get_device(self.serial)

    def change_state(self,target_state,extra_text=""):
        print("change_state called:",target_state)
        state_text = ""
        if(target_state == self.States.NoDevice):
            state_text = "无连接"
        elif(target_state == self.States.Connecting):
            state_text = "尝试连接" + extra_text
        elif(target_state == self.States.NoMission):
            state_text = "闲置中 (" + self.serial + ")"
        elif(target_state == self.States.WorkOnMission):
            state_text = "正在执行：" + extra_text + " (" + self.serial + ")"
        self.state_lock.acquire()
        self.state = target_state
        self.state_lock.release()
        if(self.webui != None):
            self.webui.Slot_change_state(state_text)

    def get_state(self):
        self.state_lock.acquire()
        result = self.state
        self.state_lock.release()
        return result


if __name__ == "__main__":
    hk2 = HK2_script()

    app = PyQt5.QtWidgets.QApplication(sys.argv)
    main_entry = os.path.realpath(os.path.dirname(__file__) + "/Assets/webui/index.html")
    w = webui.MainWin(main_entry,hk2)
    w.resize(500, 720)
    w.show()

    hk2.start_thread()

    app.exec_()





