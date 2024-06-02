import adb_tool
from enum import Enum
import cv2 as cv
import numpy as np
import time
import os

#所有页面
class Page(Enum):
    Unknown = -1
    Download = 0
    Main = 1
    Main_Shouye = 11
    Main_Zhandou = 21
    #战斗子页面
    Main_Zhandou_zhuxian = 121
    Main_Zhandou_huodong = 221
    Main_Zhandou_benghuaizhita = 321
    Main_Zhandou_duoyuanliefeng = 421
    Main_Zhandou_jvqingguanqia = 521
    Main_Zhandou_lunzhuanshilian = 621
    Main_Zhandou_luoxuanhuilang = 721
    Main_Zhandou_yaoritiaozhan = 821
    Main_Zhandou_jingshenjiban = 921
    Main_Zhandou_xuzhouzhiting = 1021
    #当期活动页面
    Main_Zhandou_Event1 = 1121
    Main_Zhandou_Event2 = 1221

    Main_Zhuangbei = 31
    Main_Shangdian = 41
    Main_Shejiao = 51
    Main_Qita = 61

    Battle = 2
    #需要特制定位的页面
    SpecialEvent = 4
    Saosaodazuozhan = 14
    Kongxiangmiyu = 24

def PageCheckfunc_download(img,result):
    copy = img.copy()
    Polylist = []
    Polylist.append(np.array([[0, 90], [130, 90], [130, 540], [0, 540]]))
    Polylist.append(np.array([[250, 90], [1030, 90], [1030, 540], [250, 540]]))
    Polylist.append(np.array([[1150, 90], [1280, 90], [1280, 540], [1150, 540]]))
    Polylist.append(np.array([[530, 23], [530, 83], [720, 83], [720, 23]]))
    target = cv.fillPoly(copy, Polylist, (255, 255, 255))
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_downloadpage.png")), cv.COLOR_BGR2RGB)
    min,max,topleft_min,topleft_max = cv.minMaxLoc(cv.matchTemplate(src,target,cv.TM_CCOEFF_NORMED))
    result[Page.Download] = (max,topleft_max)

    return result


def PageCheckfunc_main(img,result):
    temp = 0
    #遍历次级页面
    for key in pagecheckfunc_dic:
        if(key.value >= 10 and key.value < 100 and key.value%10 == 1):
            result = pagecheckfunc_dic[key](img,result)
            if(result[key][0] > temp):
                temp = result[key][0]

    result[Page.Main] = (temp-0.0000001,(0,0))
    return result

def PageCheckfunc_shouye(img,result):
    target = img[14:120,603:703]
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_on_shouye.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Shouye] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou(img,result):
    target = img[20:95,630+113*1:680+113*1]
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_on_zhandou.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))

    temp = 0
    #遍历次级页面
    for key in pagecheckfunc_dic:
        if(key.value >= 100 and key.value%100 == 21):
            result = pagecheckfunc_dic[key](img,result)
            if(result[key][0] > temp):
                temp = result[key][0]

    result[Page.Main_Zhandou] = (temp-0.0000001,max,topleft_max)
    return result

def PageCheckfunc_zhuangbei(img,result):
    target = img[20:95,630+113*2:680+113*2]
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_on_zhuangbei.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhuangbei] = (max,topleft_max)
    return result

def PageCheckfunc_shangdian(img,result):
    target = img[20:95, 630 + 113 * 3:680 + 113 * 3]
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_on_shangdian.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Shangdian] = (max,topleft_max)
    return result

def PageCheckfunc_shejiao(img,result):
    target = img[20:95, 630 + 113 * 4:680 + 113 * 4]
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_on_shejiao.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Shejiao] = (max,topleft_max)
    return result

def PageCheckfunc_qita(img,result):
    target = img[20:95, 630 + 113 * 5:680 + 113 * 5]
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_on_qita.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Qita] = (max,topleft_max)
    return result

def PageCheckfunc_battle(img,result):
    #result[Page.Battle] = (0,(0,0))
    return result

def PageCheckfunc_special(img,result):
    #result[Page.SpecialEvent] = (0,(0,0))
    return result

def PageCheckfunc_zhandou_zhuxian(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_on_zhuxian.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_zhuxian] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_huodong(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_on_huodong.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_huodong] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_benghuaizhita(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_benghuaizhita.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_benghuaizhita] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_duoyuanliefeng(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_duoyuanliefeng.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_duoyuanliefeng] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_jichengdianwanshi(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_jichengdianwanshi.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_jichengdianwanshi] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_jichengdianwanshi(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_jichengdianwanshi.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_jichengdianwanshi] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_jingshenjiban(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_jingshenjiban.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_jingshenjiban] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_jvqingguanqia(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_jvqingguanqia.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_jvqingguanqia] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_lunzhuanshilian(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_lunzhuanshilian.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_lunzhuanshilian] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_luoxuanhuilang(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_luoxuanhuilang.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_luoxuanhuilang] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_xuzhouzhiting(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_xuzhouzhiting.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_xuzhouzhiting] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_yaoritiaozhan(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_yaoritiaozhan.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_yaoritiaozhan] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_duoyuanliefeng(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Event/Event_btn_duoyuanliefeng.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_duoyuanliefeng] = (max,topleft_max)
    return result

#当期活动
def PageCheckfunc_zhandou_event1(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Update/Event_btn_dangqihuodong_back.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_Event1] = (max,topleft_max)
    return result

def PageCheckfunc_zhandou_event2(img,result):
    target = img
    src = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/Update/Event_btn_dangqihuodong2_back.png")), cv.COLOR_BGR2RGB)
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
    result[Page.Main_Zhandou_Event2] = (max,topleft_max)
    return result



pagecheckfunc_dic={
    Page.Download : PageCheckfunc_download,
    Page.Main : PageCheckfunc_main,
    Page.Battle : PageCheckfunc_battle,
    Page.SpecialEvent : PageCheckfunc_special,

    Page.Main_Shouye : PageCheckfunc_shouye,
    Page.Main_Zhandou : PageCheckfunc_zhandou,
    Page.Main_Zhuangbei : PageCheckfunc_zhuangbei,
    Page.Main_Shangdian : PageCheckfunc_shangdian,
    Page.Main_Shejiao : PageCheckfunc_shejiao,
    Page.Main_Qita : PageCheckfunc_qita,

    Page.Main_Zhandou_zhuxian :PageCheckfunc_zhandou_zhuxian,
    Page.Main_Zhandou_huodong :PageCheckfunc_zhandou_huodong,
    Page.Main_Zhandou_benghuaizhita :PageCheckfunc_zhandou_benghuaizhita,
    Page.Main_Zhandou_duoyuanliefeng :PageCheckfunc_zhandou_duoyuanliefeng,
    Page.Main_Zhandou_jvqingguanqia :PageCheckfunc_zhandou_jvqingguanqia,
    Page.Main_Zhandou_lunzhuanshilian :PageCheckfunc_zhandou_lunzhuanshilian,
    Page.Main_Zhandou_luoxuanhuilang :PageCheckfunc_zhandou_luoxuanhuilang,
    Page.Main_Zhandou_yaoritiaozhan :PageCheckfunc_zhandou_yaoritiaozhan,
    Page.Main_Zhandou_jingshenjiban :PageCheckfunc_zhandou_jingshenjiban,
    Page.Main_Zhandou_xuzhouzhiting : PageCheckfunc_zhandou_xuzhouzhiting,

    Page.Main_Zhandou_Event1 : PageCheckfunc_zhandou_event1,
    Page.Main_Zhandou_Event2 : PageCheckfunc_zhandou_event2

}

def CheckPage(img):
    result = {}
    for key in pagecheckfunc_dic:
        if(key.value <10):
            result = pagecheckfunc_dic[key](img,result)

    value_dic = {}
    for key in result:
        value_dic[result[key][0]] = key

    max_value = max(value_dic)
    max_key = value_dic[max_value]
    max_result = result[max_key]
    print(max_key,max_result)

    if(max_result[0] < 0.95):
        print("匹配度过低，无法识别页面")
        return Page.Unknown,max_result
    else:
        return max_key,max_result


def BackToZhandouMain(device):
    img = np.array(device.screenshot())
    page,result = CheckPage(img)
    pos = (result[1][0] +5, result[1][1] +5)
    if(page == Page.Unknown):
        print("unknown page,can't BackToZhandouMain")
        return False
    elif(page == Page.Main_Zhandou_huodong):
        return True
    elif(page == Page.Main_Zhandou_zhuxian):
        target_pos = (100,270)
        adb_tool.click_with_random(device,target_pos,0.2,(3,3))
        time.sleep(1)
    elif(page.value > 100 and page.value%100 == 21):
        target_pos = (pos[0] + 20,pos[1] + 20)
        adb_tool.click_with_random(device, target_pos, 0.2, (3,3))
        time.sleep(1)
    elif(page.value == Page.Battle):
        print("Battling, can't BackToZhandouMain")
    elif(page.value >= 10 and page.value < 100):
        target_pos = [770, 45]
        adb_tool.click_with_random(device, target_pos, 0.2, (3,3))
        time.sleep(1)
    return BackToZhandouMain(device)

def Match_and_Click(device, img,bias=(20,20),circle = 4,label="",mode="mc"):
    if(label!=""):
        print(label)
    for _ in range(circle):
        time.sleep(0.5)
        src = np.array(device.screenshot())
        min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, img, cv.TM_CCOEFF_NORMED))
        print("Match result:",max)
        if (max >= 0.95):
            target_pos = (topleft_max[0] + bias[0], topleft_max[1] + bias[1])
            if("c" in mode):
                adb_tool.click_with_random(device, target_pos, 0.2, (3, 3))
            return True
    return False

def GotoTargetEvent(device,img_list):
    if(BackToZhandouMain(device)):
        count = 0
        while(count < 5):
            for img in img_list:
                if(Match_and_Click(device, img,circle=1)):
                    return True
            adb_tool.swipe(device, [975, 425], "up", 100, 1)
            time.sleep(0.5)
            count+=1

        count = 0
        while(count < 5):
            for img in img_list:
                if(Match_and_Click(device, img,circle=1)):
                    return True
            adb_tool.swipe(device, [975, 425], "down", 100, 1)
            time.sleep(0.5)
            count += 1

        print("未能找到目标活动位置")
        return False
    else:
        return False


def Double_and_buy_stamina(device,mqueue):
    flag = 0  #0~未触发双倍或购买  -1~体力不足且不购买  1~使用双倍或购买
    double_target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_window_duihuanshuangbeitili.png")), cv.COLOR_BGR2RGB)
    buy_target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_window_buchongtili.png")), cv.COLOR_BGR2RGB)
    duihuan_target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_duihuan.png")), cv.COLOR_BGR2RGB)
    goumai_target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_goumai.png")), cv.COLOR_BGR2RGB)
    qvxiao_target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_qvxiao.png")), cv.COLOR_BGR2RGB)
    time.sleep(1)
    src = np.array(device.screenshot())
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, double_target, cv.TM_CCOEFF_NORMED))
    if(max >=0.95):#使用双倍体力
        time.sleep(1)
        Match_and_Click(device,duihuan_target,circle = 1,label="双倍体力")
        flag = 1


    time.sleep(1)

    src = np.array(device.screenshot())
    min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, buy_target, cv.TM_CCOEFF_NORMED))
    if(max >=0.95):#购买体力窗口
        if(mqueue.buy_count[0] > 0):#确定购买
            if(Match_and_Click(device, goumai_target)):
                flag = 1
                mqueue.change_buycount(mqueue.buy_count[0] - 1)
        else:#不购买体力
            Match_and_Click(device,qvxiao_target)
            time.sleep(0.5)
            adb_tool.click_with_random(device,[50,130],0.2,[3,3])
            flag = -1

    return flag




def GotoFight(device,img,is_skip,is_ticket,mqueue,bias = (20,20),label=""):
    if(Match_and_Click(device, img,bias = bias,label=label)):
        if(is_skip):#是快捷战斗
            #检查体力
            target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_buchongtili.png")), cv.COLOR_BGR2RGB)
            if(Match_and_Click(device,target,circle=2)):
                flag = Double_and_buy_stamina(device, mqueue)
                if(flag == -1):
                    return False
                elif(flag == 1):
                    time.sleep(0.2)
                    src = np.array(device.screenshot())
                    min, max, topleft_min, topleft_max = cv.minMaxLoc(
                        cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
                    if(max>=0.95):
                        return False
            #快捷战斗
            target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_kuaijiezhandou.png")), cv.COLOR_BGR2RGB)
            if(Match_and_Click(device, target,circle=2)):
                time.sleep(0.5)
                target2 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_queding.png")), cv.COLOR_BGR2RGB)
                if(Match_and_Click(device, target2)):
                    time.sleep(0.5)
                    target3 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_battleend_queding.png")), cv.COLOR_BGR2RGB)
                    if (Match_and_Click(device, target3)):
                        time.sleep(1)
                        Match_and_Click(device, target3,circle=1) #可能的角色升级
                        return True
                    else:
                        print("未找到快捷战斗后 确定按钮")
                        return False
                else:
                    print("未能找到确定按钮")
                    return False
            else:
                print("未能找到快捷战斗按钮")
                return False
        else:#不是快捷战斗
            if(is_ticket):#按一下双倍券按钮
                time.sleep(0.2)
                ticket_target_pos = [1100,540]
                adb_tool.click_with_random(device, ticket_target_pos, 0.2, (3, 3))
            #检查体力
            target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_buchongtili.png")), cv.COLOR_BGR2RGB)
            if (Match_and_Click(device, target,circle=2)):
                flag = Double_and_buy_stamina(device, mqueue)
                if (flag == -1):
                    return False
                elif (flag == 1):
                    time.sleep(0.2)
                    src = np.array(device.screenshot())
                    min, max, topleft_min, topleft_max = cv.minMaxLoc(
                        cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
                    if (max >= 0.98):
                        return False
            #按选择助战好友
            target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_xuanzezhuzhanhaoyou.png")), cv.COLOR_BGR2RGB)
            if(Match_and_Click(device, target,circle=2)):
                time.sleep(1)
                # 使魔同调率页面
                target = cv.cvtColor(
                    cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_window_shimo.png")),
                    cv.COLOR_BGR2RGB)
                src = np.array(device.screenshot())
                min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
                print("max:", max)
                if (max >= 0.95):
                    target_kaizhan = cv.cvtColor(
                        cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_shimo_kaizhan.png")),
                        cv.COLOR_BGR2RGB)
                    Match_and_Click(device, target_kaizhan)
                time.sleep(0.5)
                adb_tool.click_with_random(device, [500,270], 0.5, (10, 10))
                target2 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_kaizhan.png")), cv.COLOR_BGR2RGB)
                time.sleep(1)
                if(Match_and_Click(device, target2)):
                    return True
                else:
                    print("未能找到开战按钮")
                    return False
            else:
                print("未能找到选择助战好友按钮")
                return False

    else:
        print("未找到进入战斗按钮")
        return False

def GotoFight_pos(device, pos, is_skip, is_ticket, mqueue):
    adb_tool.click_with_random(device,pos,0.5,[3,3])
    time.sleep(0.5)
    if (is_skip):  # 是快捷战斗
        # 检查体力
        target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_buchongtili.png")), cv.COLOR_BGR2RGB)
        if (Match_and_Click(device, target,circle=2)):
            flag = Double_and_buy_stamina(device, mqueue)
            if (flag == -1):
                return False
            elif (flag == 1):
                time.sleep(0.2)
                src = np.array(device.screenshot())
                min, max, topleft_min, topleft_max = cv.minMaxLoc(
                    cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
                if (max >= 0.98):
                    return False
        # 快捷战斗
        target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_kuaijiezhandou.png")), cv.COLOR_BGR2RGB)
        if (Match_and_Click(device, target,circle=2)):
            time.sleep(0.5)
            target2 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_queding.png")), cv.COLOR_BGR2RGB)
            if (Match_and_Click(device, target2)):
                time.sleep(0.5)
                target3 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_battleend_queding.png")), cv.COLOR_BGR2RGB)
                if (Match_and_Click(device, target3)):
                    time.sleep(1)
                    Match_and_Click(device, target3)  # 可能的角色升级
                    return True
                else:
                    print("未找到快捷战斗后 确定按钮")
                    return False
            else:
                print("未能找到确定按钮")
                return False
        else:
            print("未能找到快捷战斗按钮")
            return False
    else:  # 不是快捷战斗
        if (is_ticket):  # 按一下双倍券按钮
            time.sleep(0.2)
            ticket_target_pos = [1100, 540]
            adb_tool.click_with_random(device, ticket_target_pos, 0.2, (3, 3))
        # 检查体力
        target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_buchongtili.png")), cv.COLOR_BGR2RGB)
        if (Match_and_Click(device, target,circle=2)):
            flag = Double_and_buy_stamina(device, mqueue)
            if (flag == -1):
                return False
            elif (flag == 1):
                time.sleep(0.5)
                src = np.array(device.screenshot())
                min, max, topleft_min, topleft_max = cv.minMaxLoc(
                    cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
                if (max >= 0.98):
                    return False
        # 按选择助战好友
        target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_xuanzezhuzhanhaoyou.png")), cv.COLOR_BGR2RGB)
        if (Match_and_Click(device, target,circle=2)):
            time.sleep(0.5)
            # 使魔同调率页面
            time.sleep(1)
            target = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_window_shimo.png")),
                                 cv.COLOR_BGR2RGB)
            src = np.array(device.screenshot())
            min, max, topleft_min, topleft_max = cv.minMaxLoc(cv.matchTemplate(src, target, cv.TM_CCOEFF_NORMED))
            print("max:", max)
            if (max >= 0.98):
                target_kaizhan = cv.cvtColor(
                    cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_shimo_kaizhan.png")),
                    cv.COLOR_BGR2RGB)
                Match_and_Click(device, target_kaizhan)

            time.sleep(0.5)
            adb_tool.click_with_random(device, [500, 270], 0.5, (10, 10))
            target2 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_btn_kaizhan.png")), cv.COLOR_BGR2RGB)
            time.sleep(1)
            if (Match_and_Click(device, target2)):
                return True
            else:
                print("未能找到开战按钮")
                return False
        else:
            print("未能找到选择助战好友按钮")
            return False


def check_shimotanxian(device):
    t1 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_shimotanxianS.png")), cv.COLOR_BGR2RGB)
    t2 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_shimotanxianA.png")), cv.COLOR_BGR2RGB)

    src = np.array(device.screenshot())[180:410,180:1260]
    min1, max1, topleft_min1, topleft_max1 = cv.minMaxLoc(cv.matchTemplate(src, t1, cv.TM_CCOEFF_NORMED))
    min2, max2, topleft_min2, topleft_max2 = cv.minMaxLoc(cv.matchTemplate(src, t2, cv.TM_CCOEFF_NORMED))

    result = max(max1, max2)

    print("check_shimotanxian result: ", result)
    if(result>=0.80):
        return True
    else:
        return False

def check_bluepoint(device,target):
    bluepoint_pos_dic = {
        "daily_entry" : [68,132],
        "shangdian" : [1026,0],
        "cunzaigan" : [0,270],
        "meizhourenwu" : [0,343],
        "shimotanxian" : [0,416]
    }
    t1 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_bluepoint.png")), cv.COLOR_BGR2RGB)
    t2 = cv.cvtColor(cv.imread(os.path.realpath(os.path.dirname(__file__) + "/Assets/p_bluepoint2.png")), cv.COLOR_BGR2RGB)

    src = np.array(device.screenshot())[bluepoint_pos_dic[target][1]:bluepoint_pos_dic[target][1]+26,bluepoint_pos_dic[target][0]:bluepoint_pos_dic[target][0]+26]
    min1, max1, topleft_min1, topleft_max1 = cv.minMaxLoc(cv.matchTemplate(src, t1, cv.TM_CCOEFF_NORMED))
    min2, max2, topleft_min2, topleft_max2 = cv.minMaxLoc(cv.matchTemplate(src, t2, cv.TM_CCOEFF_NORMED))

    result = max(max1,max2)

    print("check_bluepoint:",target,"result: ",result)
    return result

def hold_right_and_wp1(device):
    device.shell(["sendevent", "/dev/input/event4", "3", "53", "6147"])
    device.shell(["sendevent", "/dev/input/event4", "3", "54", "25257"])
    device.shell(["sendevent", "/dev/input/event4", "0", "2", "0"])

    device.shell(["sendevent", "/dev/input/event4", "3", "53", "26187"])
    device.shell(["sendevent", "/dev/input/event4", "3", "54", "28621"])
    device.shell(["sendevent", "/dev/input/event4", "0", "2", "0"])
    device.shell(["sendevent", "/dev/input/event4", "0", "0", "0"])

def stop_hold_right_and_wp1(device):
    device.shell(["sendevent", "/dev/input/event4", "3", "53", "26187"])
    device.shell(["sendevent", "/dev/input/event4", "3", "54", "28621"])
    device.shell(["sendevent", "/dev/input/event4", "0", "2", "0"])
    device.shell(["sendevent", "/dev/input/event4", "0", "0", "0"])

    device.shell(["sendevent", "/dev/input/event4", "0", "2", "0"])
    device.shell(["sendevent", "/dev/input/event4", "0", "0", "0"])