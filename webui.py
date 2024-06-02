from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebChannel import *
from PyQt5.QtWebEngineWidgets import *
import os

class MyObjectCls(QObject):
    sigSetParentWindowTitle = pyqtSignal(str)

    signal_add_mission = pyqtSignal(str)
    signal_delete_mission = pyqtSignal(int)
    signal_start_one = pyqtSignal(int)
    signal_complete_one = pyqtSignal(int)
    signal_change_buycount = pyqtSignal(int)
    signal_change_state = pyqtSignal(str)

    def __init__(self, main_script=None, parent=None):
        QObject.__init__(self, parent)
        self._main_script = main_script
        if(self._main_script != None):
            self._main_script.webui = self

    def Slot_change_state(self,stat):
        self.signal_change_state.emit(stat)

    def Slot_add_mission(self, name):
        # 发送信号，传递返回值
        self.signal_add_mission.emit(name)

    def Slot_delete_mission(self, idx):
        # 发送信号，传递返回值
        self.signal_delete_mission.emit(idx)

    def Slot_start_one(self, idx):
        # 发送信号，传递返回值
        self.signal_start_one.emit(idx)

    def Slot_complete_one(self, idx):
        # 发送信号，传递返回值
        self.signal_complete_one.emit(idx)

    def Slot_change_buycount(self, idx):
        # 发送信号，传递返回值
        self.signal_change_buycount.emit(idx)

    @pyqtSlot(str)
    def change_serial(self,serial):
        self._main_script.serial = serial

    @pyqtSlot(str)
    def print(self,text):
        print(text)

    @pyqtSlot(str)
    def add_mission(self,mission):
        if(self._main_script!=None):
            self._main_script.mqueue.add(mission)

    @pyqtSlot()
    def resume(self):
        if (self._main_script != None):
            self._main_script.mqueue.mthread.resume()

    @pyqtSlot()
    def pause(self):
        if (self._main_script != None):
            self._main_script.mqueue.mthread.pause()

    @pyqtSlot(int)
    def change_buycount(self,count):
        if (self._main_script != None):
            self._main_script.mqueue.change_buycount(count)


    @pyqtSlot(str)
    def setParentWindowTitle(self, msg):
        self.sigSetParentWindowTitle.emit(msg)

    @pyqtSlot(int)
    def delete_mission(self,idx):
        if(self._main_script!=None):
            self._main_script.mqueue.delete(idx)


class MainWin(QWebEngineView):
    def __init__(self,main_entry,main_script=None):
        QWebEngineView.__init__(self)
        self.__channel = QWebChannel(self.page())
        self.__my_object = MyObjectCls(main_script=main_script,parent=self)
        self.__channel.registerObject('MyObject',self.__my_object)
        self.page().setWebChannel(self.__channel)       
        self.__my_object.sigSetParentWindowTitle.connect(self.setWindowTitle)
        self.page().load(QUrl.fromLocalFile(main_entry))

    def closeEvent(self, event):
        os._exit(0)



if __name__ == '__main__':
    import sys, os

    app = QApplication(sys.argv)
    main_entry = os.path.realpath(os.path.dirname(__file__) + "/Assets/webui/index.html")
    w = MainWin(main_entry)
    w.resize(500, 720)
    w.show()
    app.exec_()