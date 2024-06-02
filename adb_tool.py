import random

from adbutils import adb
import cv2 as cv
import matplotlib.pyplot as plt
import time

def connect(serial,timeout):
    return adb.connect(serial,timeout)

def click_with_random(device,pos,t_random,p_random):
    clk_x = pos[0] + int(random.uniform(-1*p_random[0],p_random[0]))
    clk_y = pos[1] + int(random.uniform(-1*p_random[1],p_random[1]))
    delay_time = random.uniform(0,t_random)
    time.sleep(delay_time)
    device.click(clk_x,clk_y)

def swipe(device, pos, dir, distance, duration):#duration in seconds
    target_x = pos[0]
    target_y = pos[1]
    if(dir=="up"):
        target_y = min(pos[1] - distance,20)
    elif(dir=="down"):
        target_y = max(pos[1] + distance,760)
    elif(dir=="left"):
        target_x = min(pos[0] - distance,20)
    elif(dir=="right"):
        target_x = max(pos[0] + distance,1260)
    device.swipe(pos[0],pos[1],target_x,target_y,duration)


def get_device(serial):
    for device in adb.device_list():
        if(device.serial == serial):
            return device
    return None




