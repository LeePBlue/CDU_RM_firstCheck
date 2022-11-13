#  ■■■■■■■■■■■■■■■■■■■■■■■
#
#          RoboMaster Vision Core Program
#             机甲大师对抗赛视觉组核心程序
#                     入口程序
#
#                Code by Yourname
#             Last Update： MAR20/2021
#
#      注意：本PY文件只能在Master分支进行修改
#         其他分支请修改Define.py/Config.py
#
#  ■■■■■■■■■■■■■■■■■■■■■■■

from module.ModuleDebugs import Debugs
from module.ModuleShared import Shared
from module.ModuleConfig import *
import Config
import Extend
import numpy
import time
import os


# 自定义初始化函数------------------------------------------------------------------------------------------------------
# 含义：本函数在系统初始化的时候调用，可以自定义需要初始化的内容（例如载入网络模型、特殊设备载入、部分硬件初始化等）----
def InitalOthers(in_conf, in_decv, in_lock):
    pass


# 自定义其他线程块------------------------------------------------------------------------------------------------------
# 含义：本函数作为独立进程执行，对于InitalOthers里面的数据必须存入全局变量in_conf才能获取到，本进程不和其他进程干涉-----
def DefineOthers(in_conf, in_lock, Picture):
    while True:
        pass


# 将方法添加进线程------------------------------------------------------------------------------------------------------
defineProcess = [DefineOthers]


# 装甲板的识别线程------------------------------------------------------------------------------------------------------
def InitalArmors(in_conf):
    extend_datas = {}
    # 你需要初始化的内容----------------------------
    # 数据需要放进extend_datas----------------------
    # ----------------------------------------------
    return extend_datas


# 装甲板的识别线程------------------------------------------------------------------------------------------------------
def DefineArmors(in_conf, armors_imgs, armors_delt, extend_datas=None):
    # 此处是调用识别和追踪的代码-------------------------------------
    # armors_imgs是当前接收的图像
    # armors_time是当前帧的时间戳
    # armors_last是上个帧的时间戳
    # extend_datas 是初始化参数值
    if extend_datas is None:
        extend_datas = {}
    # 你需要修改的代码在这里改----------------------------------------
    Shared.Put(in_conf, "Record", "DAT1", 0)
    Shared.Put(in_conf, "Record", "DAT2", 0)
    # 切换大符模式，切换之后需要等待大约1.5秒会生效-------------------
    # 当且仅当开启了自动滤波后并且需要击打大符的时候才需要修改大符模式
    # Shared.Put(in_conf, "Record", "TYPE", True)       # 开启大符模式
    # time.sleep(1)
    # Shared.Put(in_conf, "Record", "TYPE", False)      # 关闭大符模式
    # time.sleep(1)
    # ----------------------------------------------------------------
