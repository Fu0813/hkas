import time
import threading
import BaseControl
import cv2 as cv
import numpy as np

import adb_tool

import os



class MissionQueue:
    def __init__(self,main_script):
        self.mission_list = []
        self.mthread = MissionThread(self)
        self.main_script = main_script
        self.buy_count = [0]
        self.current_mission = None

    def add(self,name):
        print("add mission:",name)
        self.mission_list.append(name)
        if(self.main_script.webui != None):
            self.main_script.webui.Slot_add_mission(name)

    def delete(self,idx):
        target = idx
        self.mission_list.pop(target)
        if (self.main_script.webui != None):
            self.main_script.webui.Slot_delete_mission(idx)

    def complete_one(self):
        self.current_mission=None
        self.main_script.change_state(self.main_script.States.NoMission)

    def start_one(self):
        if(len(self.mission_list) >0):
            self.current_mission = self.mission_list[0]
            self.main_script.change_state(self.main_script.States.WorkOnMission, self.current_mission)

            self.mission_list.pop(0)
            if (self.main_script.webui != None):
                self.main_script.webui.Slot_start_one(0)
            return True
        else:
            return False

    def change_buycount(self,count):
        if(self.buy_count[0] != count):
            self.buy_count[0] = count
            if (self.main_script.webui != None):
                self.main_script.webui.Slot_change_buycount(count)


    def is_running(self):
        return self.mthread.is_running()



class MissionThread(threading.Thread):
    def __init__(self,mqueue):
        super().__init__()
        self.mqueue = mqueue
        self.mevent = threading.Event()
        self.on_mission = False

    def run(self):
        while(True):
            self.mevent.wait()
            if(len(self.mqueue.mission_list) > 0 and self.mqueue.current_mission == None and self.mqueue.main_script.get_state() == self.mqueue.main_script.States.NoMission):
                if(self.mqueue.start_one()):
                    mission_dic[self.mqueue.current_mission](self.mqueue.main_script.device, self.mqueue)
                self.mqueue.complete_one()
                time.sleep(1)


    def pause(self):
        self.mevent.clear()

    def resume(self):
        self.mevent.set()

    def is_running(self):
        return self.mevent.is_set()




#mission functions
#重启设置
def mfunc_restart(device,mequeue):
    target_0 =  cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_gameicon.png")), cv.COLOR_BGR2RGB)
    if(BaseControl.Match_and_Click(device,target_0,circle=2)):#进入游戏
        time.sleep(1)
        target_check = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_mihoyo.png")), cv.COLOR_BGR2RGB)
        if(BaseControl.Match_and_Click(device,target_check,circle=2,label="检查mihoyo图标",mode="m")):
            while(True):
                target_sl = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_shilingtishi.png")), cv.COLOR_BGR2RGB)
                if(BaseControl.Match_and_Click(device,target_sl,mode="m")):
                    time.sleep(2.5)
                    adb_tool.click_with_random(device,[400,350],0.5,[10,10])
                    break
            time.sleep(5)
            target_1 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_lingqv.png")), cv.COLOR_BGR2RGB)
            while(True):
                time.sleep(1)
                if(not BaseControl.Match_and_Click(device,target_1,label="领取按钮",circle=1)):
                   break
            time.sleep(1)
            target_2 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_jinribuzaitishi.png")), cv.COLOR_BGR2RGB)
            BaseControl.Match_and_Click(device, target_2,label="今日不在提示按钮",circle=2)
            time.sleep(1)
            target_3 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_jinrihuodong_back.png")),cv.COLOR_BGR2RGB)
            BaseControl.Match_and_Click(device, target_3,label="活动页退出按钮",circle=2)

#崩科学院
def mfunc_bengke(device,mqueue):
    print("bengke start")
    BaseControl.BackToZhandouMain(device)
    time.sleep(0.5)
    target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_bengkexiaohuo.png")), cv.COLOR_BGR2RGB)
    target2 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_bengkexiaohuo_s.png")), cv.COLOR_BGR2RGB)
    BaseControl.GotoTargetEvent(device,[target,target2])

    #领使魔碎片
    target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/p_bengke_shimo.png")), cv.COLOR_BGR2RGB)
    if(BaseControl.Match_and_Click(device,target)):
        time.sleep(2)

        target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/p_btn_bengke_lingqvshouyi.png")), cv.COLOR_BGR2RGB)
        if(BaseControl.Match_and_Click(device,target)):
            time.sleep(1)

            adb_tool.click_with_random(device, [883, 543], 0.2, [5, 5])
            time.sleep(1)

        target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/p_btn_bengke_shimo_exit.png")), cv.COLOR_BGR2RGB)
        BaseControl.Match_and_Click(device,target)
        time.sleep(1)

    # 战斗
    target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/p_bengke_battle.png")), cv.COLOR_BGR2RGB)
    for _ in range(2):
        adb_tool.swipe(device, [500, 400], 'left', 200, 0.5)
        time.sleep(0.5)
        if (BaseControl.GotoFight(device, target, False, False, mqueue)):
            time.sleep(1)
            BaseControl.hold_right_and_wp1(device)
            target_battle_end = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_battleend_queding.png")), cv.COLOR_BGR2RGB)
            # 等待战斗结束
            while (True):
                time.sleep(1)
                if (BaseControl.Match_and_Click(device, target_battle_end)):
                    BaseControl.stop_hold_right_and_wp1(device)
                    break
        time.sleep(1)

    #占卜
    adb_tool.swipe(device,[500,400],'right',200,0.5)
    time.sleep(0.5)
    adb_tool.swipe(device, [500, 400], 'down', 200, 0.5)
    time.sleep(0.5)

    target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/p_bengke_zhanbu.png")), cv.COLOR_BGR2RGB)
    if(BaseControl.Match_and_Click(device, target)):
        time.sleep(2)

        target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/p_btn_bengke_kaishizhanbu.png")), cv.COLOR_BGR2RGB)
        BaseControl.Match_and_Click(device, target)
        time.sleep(2)

        adb_tool.click_with_random(device, [55, 55], 0.2, [5, 5])
        time.sleep(2)



    #退出
    adb_tool.click_with_random(device, [55, 55], 0.2, [5, 5])

#当期刷刷活动
def mfunc_eventloop(device,mqueue):
    print("event start")
    target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Update/Event_dangqihuodong.png")), cv.COLOR_BGR2RGB)
    target_bonus = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Update/Event_btn_dangqihuodong_bonus.png")), cv.COLOR_BGR2RGB)
    BaseControl.GotoTargetEvent(device,[target])
    flag = True
    time.sleep(2)
    while(flag):
        for _ in range(3):
            if(not BaseControl.Match_and_Click(device,target_bonus,mode="m")):
                adb_tool.swipe(device,[400,350],"left",200,0.5)
                time.sleep(1)
            else:
                break
        flag = BaseControl.GotoFight(device,target_bonus,False,True,mqueue)
        if(flag):
            time.sleep(5)
            adb_tool.click_with_random(device,[151,621],0.2,[5,5])
            BaseControl.hold_right_and_wp1(device)
            target_battle_end = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_battleend_queding.png")), cv.COLOR_BGR2RGB)
            #等待战斗结束
            while(True):
                time.sleep(1)
                if(BaseControl.Match_and_Click(device, target_battle_end)):
                    BaseControl.stop_hold_right_and_wp1(device)
                    time.sleep(1)
                    target_levelup = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_battleend_queding.png")), cv.COLOR_BGR2RGB)
                    BaseControl.Match_and_Click(device,target_levelup)
                    break
        time.sleep(2)

#当期刷刷活动2
def mfunc_event2loop(device,mqueue):
    print("event start")
    target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Update/Event_dangqihuodong2.png")), cv.COLOR_BGR2RGB)
    target_bonus = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Update/Event_btn_dangqihuodong2_bonus.png")), cv.COLOR_BGR2RGB)
    BaseControl.GotoTargetEvent(device,[target])
    flag = True
    time.sleep(2)
    while(flag):
        for _ in range(3):
            if(not BaseControl.Match_and_Click(device,target_bonus,mode="m")):
                adb_tool.swipe(device,[400,350],"left",200,0.5)
                time.sleep(1)
            else:
                break
        flag = BaseControl.GotoFight(device,target_bonus,False,True,mqueue,bias=(80,100),label="活动2")
        if(flag):
            time.sleep(5)
            adb_tool.click_with_random(device,[151,621],0.2,[5,5])
            BaseControl.hold_right_and_wp1(device)
            target_battle_end = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_battleend_queding.png")), cv.COLOR_BGR2RGB)
            #等待战斗结束
            while(True):
                time.sleep(1)
                if(BaseControl.Match_and_Click(device, target_battle_end)):
                    BaseControl.stop_hold_right_and_wp1(device)
                    time.sleep(1)
                    target_levelup = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_battleend_queding.png")), cv.COLOR_BGR2RGB)
                    for _ in range(3):
                        BaseControl.Match_and_Click(device,target_levelup,circle=1)
                        time.sleep(0.5)
                    break
        time.sleep(2)

#领取日常
def mfunc_claimreward(device,mqueue):
    print("claim reward")
    # 零时馈礼
    BaseControl.BackToZhandouMain(device)
    time.sleep(0.5)
    adb_tool.click_with_random(device, [650, 50], 0.2, [5, 5])
    time.sleep(1.5)

    if(BaseControl.check_bluepoint(device,"shangdian")>0.38): #他妈的阈值真低
        print("libaoshangdian")
        adb_tool.click_with_random(device, [992, 49], 0.2, [5, 5])
        time.sleep(0.5)

        adb_tool.click_with_random(device, [523, 225], 0.2, [5, 5])
        time.sleep(0.5)

        adb_tool.click_with_random(device, [72, 301], 0.2, [5, 5])
        time.sleep(0.5)

        adb_tool.swipe(device, [685, 434], "up", 200, 0.5)
        time.sleep(0.5)

        adb_tool.swipe(device, [685, 434], "up", 200, 0.5)
        time.sleep(0.5)

        target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_lingshikuili.png")), cv.COLOR_BGR2RGB)
        if(BaseControl.Match_and_Click(device,target,(130,330))):
            target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_lingshi_goumai.png")), cv.COLOR_BGR2RGB)
            BaseControl.Match_and_Click(device,target)
            time.sleep(0.5)
            target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_goumaichonggong_queding.png")), cv.COLOR_BGR2RGB)
            BaseControl.Match_and_Click(device, target)

    time.sleep(1)
    #每日项目
    BaseControl.BackToZhandouMain(device)
    time.sleep(0.5)

    adb_tool.click_with_random(device, [655, 53], 0.2, [5, 5])
    time.sleep(0.5)

    if (BaseControl.check_bluepoint(device, "daily_entry") > 0.38):
        time.sleep(0.5)
        adb_tool.click_with_random(device, [51, 166], 0.2, [3, 3])
        time.sleep(0.5)

        #使魔探险
        adb_tool.click_with_random(device, [73, 456], 0.2, [5, 5])
        time.sleep(0.5)

        while(True):
            if(not BaseControl.check_shimotanxian(device)):#仍有未领取或未执行的探险项
                adb_tool.click_with_random(device, [741, 266], 0.2, [5, 5])
                time.sleep(0.5)
                target_paiqian = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_yijianpaiqian.png")), cv.COLOR_BGR2RGB)
                target_chufa = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_chufa.png")), cv.COLOR_BGR2RGB)
                BaseControl.Match_and_Click(device,target_paiqian,circle=1)
                time.sleep(0.5)
                BaseControl.Match_and_Click(device,target_chufa,circle=1)
                time.sleep(0.5)
            else:
                time.sleep(1)
                break
        #每日存在感
        if (BaseControl.check_bluepoint(device, "cunzaigan") > 0.5):
            adb_tool.click_with_random(device, [75, 309], 0.2, [5, 5])
            time.sleep(0.2)

            adb_tool.click_with_random(device, [1020, 216], 0.2, [5, 5])
            time.sleep(0.5)

            adb_tool.click_with_random(device, [1020, 216], 0.2, [5, 5])
            time.sleep(1)

        #每周任务
        if (BaseControl.check_bluepoint(device, "meizhourenwu") > 0.5):
            adb_tool.click_with_random(device, [75, 382], 0.2, [5, 5])
            time.sleep(0.2)

            adb_tool.click_with_random(device, [1020, 216], 0.2, [5, 5])
            time.sleep(1)

            adb_tool.click_with_random(device, [1020, 216], 0.2, [5, 5])
            time.sleep(0.5)

#日常活动
def mfunc_dailywork(device,mqueue):
    print("daily work")
    #使魔的爱
    target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_duoyuanliefeng.png")), cv.COLOR_BGR2RGB)
    if(BaseControl.GotoTargetEvent(device,[target])):
        time.sleep(0.5)
        if(BaseControl.GotoFight_pos(device,[651,500],True,False,mqueue)):
            time.sleep(2)
            adb_tool.click_with_random(device, [15, 137], 0.2, [3, 3])
        else:
            adb_tool.click_with_random(device, [15, 137], 0.2, [3, 3])
    else:
        return False

    time.sleep(0.5)
    #虚轴之庭
    target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_xuzhouzhiting.png")), cv.COLOR_BGR2RGB)
    time.sleep(0.5)
    if(BaseControl.Match_and_Click(device,target)):
        time.sleep(0.5)
        adb_tool.click_with_random(device, [73, 252], 0.2, [3, 3])
        time.sleep(0.5)
        adb_tool.click_with_random(device, [73, 252], 0.2, [3, 3])
        time.sleep(0.5)
        x_target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/p_btn_xuzhouchuji.png")), cv.COLOR_BGR2RGB)
        while(True):
            if (BaseControl.GotoFight(device, x_target, True, False, mqueue,label="虚轴之庭出击")):
                target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_battleend_queding.png")), cv.COLOR_BGR2RGB)
                BaseControl.Match_and_Click(device,target)
                time.sleep(0.5)
                adb_tool.click_with_random(device,[61,137],0.2,[3,3])
                time.sleep(1)

            else:
                adb_tool.click_with_random(device, [15, 137], 0.2, [3, 3])
                break

mission_dic = {
    "重启设置": mfunc_restart,
    "崩科学院": mfunc_bengke,
    "日常活动":mfunc_dailywork,
    "领取奖励":mfunc_claimreward,
    "激战长空":mfunc_eventloop,
    "往夏回忆":mfunc_event2loop
}





