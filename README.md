# hkas

## 介绍
崩坏学园2自动化脚本v0.04


## 安装教程

1.  确保您的环境中包含python3
2.  打开命令行(cmd)并进入本项目根目录
3.  输入`python -m venv hkas_env`命令创建一个位于本目录的python虚拟环境，你可以修改hkas_env为自己想要的名字，但下一步的命令中需要同步修改
4.  输入`hkas_env\Scripts\activate`命令进入刚刚创建的虚拟环境
5.  输入`pip install -r .\deploy\requirements.txt`命令，安装deploy\requirements.txt文件中列出的项目依赖包
6.  确认所有依赖包安装无误后，输入`python main.py`命令运行本脚本，如果脚本窗口出现，说明安装成功

## 使用说明

目前仅在蓝叠模拟器5上测试过，不保证在其他模拟器能顺利运行

执行任务：

脚本程序第一行显示当前脚本状态，“闲置”代表脚本已连接到正确的adb服务器，并且没有执行任何自动化任务，“正在执行任务：xxx”代表程序正在执行该任务

脚本一旦开始执行某个任务，中途不会停止（即使按下暂停键），如果发现脚本在乱搞或希望中途停止，请直接关闭脚本程序

增添任务：

向任务等待队列中增加一项任务，具体的任务在下拉选项单中选择

“崩科学园”：自动化崩科校活，有些关卡的战斗部分没法按住右键和攻击就刷完（艹了），手动过关即可，不必退出程序

“日常活动”：快捷进行使魔的爱和虚轴之庭，没解锁快捷的话不会刷

“领取奖励”：领取日常任务奖励，按以下顺序执行：领取每日免费零时之种→检查使魔探险→领取存在感奖励→领取每周任务奖励

增添的任务在“暂停”状态时不会进入执行栏，只有在“启动中”状态程序才会按次序执行任务

程序在打开时默认为“暂停”状态

下方的“开始”，“暂停”按钮负责调控等待队列的状态，不负责暂停正在执行中的任务

买体力次数：

刷体力类的任务在清空体力时，购买体力继续刷的次数，默认为0

输入窗口内会同步更新剩余可用次数


【重要！】【重要！】【重要！】

目前所有战斗的逻辑均为按住向右和武器1，尝试使用【次元链接】（双周boss），【吉祥天女】（魔女/崩坏屋刷新），【盛夏清忆】（好像是全神抽卡？等up吧）之类的装备自动刷


#### 后续肯定会有的更新计划：

为崩科学园的战斗关卡匹配不同战斗逻辑

将崩科学园传送门玩法加入自动化

在日常活动中加入社团体力领取

在日常活动中加入刷双周boss，并贩卖得到的垃圾装备

#### 后续可能会有的更新计划：

学习Alas按时间自动重置（逼崩2有双倍体力导致体力值是个动画，血妈难识别，再说吧）

自动化崩坏之塔（真有必要吗？真能打过吗？）

自动切换装备刷好感

战斗逻辑中加入切备用选项（以方便切备用过关，刷主套好感）
