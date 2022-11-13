# coding:utf-8
#  ■■■■■■■■■■■■■■■■■■■■■■■
#
#          RoboMaster Vision Core Program
#             机甲大师对抗赛视觉组核心程序
#                     入口程序
#
#                Code by Pikachu
#             Last Update： JUL21/2021
#
#      注意：本PY文件只能在Master分支进行修改
#         其他分支请修改Define.py/Config.py
#
#  ■■■■■■■■■■■■■■■■■■■■■■■


# 引入模块信息 ----------------------------------
from module.ModuleSerial import Serial
from module.ModuleDebugs import Debugs
from module.ModuleShared import Shared
from module.ModuleConfig import *
import Config
import Define
import Extend
import numpy as np
import hashlib
import time
import os

if Config.use_threads:
    import threading as Thread
else:
    from multiprocessing import Process, Manager
    import multiprocessing as MPData

    if Config.ShareMemory:
        if Config.master_dvce == 'nx':
            from shared_numpy import shared_memory
        elif Config.master_dvce == 'minipc':
            from multiprocessing.managers import SharedMemoryManager


# 显示配置信息 ---------------------------------------------------------------------------------------------------------
def MasterShowInfo(in_conf, in_pcss, in_lock, Picture):
    # 进程加锁-----------------------------------------------------
    in_lock.acquire()
    # 初始化串口信息-----------------------------------------------
    in_conf['SendID'] = Config.master_send  # 发送方编号
    in_conf['RecvID'] = Config.master_recv  # 接收方编号
    in_conf["Option"] = Config.Option       # 自定义选项
    in_conf["Record"] = Config.Record       # 可变参数项
    in_conf["Serial"] = Config.Serial       # 串口数据集
    in_conf["FPLock"] = False               # 强制同步锁
    in_conf["PGLock"] = False               # 进程修改锁
    in_conf["ComNum"] = 0                   # 串口循环数
    in_conf["Receive"] = Config.Receive     # 串口接收区
    in_conf["LoopDog"] = {}                 # 看门狗数据
    # 初始化进程信息-----------------------------------------------
    Debugs(in_datas="----------------------------------------------------")
    for in_temp in Extend.extendProcess + Define.defineProcess:
        Debugs(in_datas="[进程]" + str(in_temp))
        in_pcss.append(in_temp)
    Debugs(in_datas="----------------------------------------------------")
    # 进程解锁-----------------------------------------------------
    in_lock.release()


# 初始各种设备 ---------------------------------------------------------------------------------------------------------
def MasterGetReady(in_conf, in_decv, in_lock, Picture):
    # 进程加锁-------------------------------------------------------------------------
    in_lock.acquire()
    if Config.serial_flag:
        # 初始化串口设备--------------------------------------------------------------
        in_decv["Serial"] = Serial(Config.serial_port,
                                   Config.serial_bbps,
                                   in_conf['SendID'],
                                   in_conf['RecvID'], 0x00, 0x00)
        # 写入串口变量-----------------------------------------------------------------
        Debugs(in_datas="----------------------------------------------------")
        Debugs(in_datas="[串口]" + " " +str(in_decv["Serial"])[8:-19] + "0x00" + str(in_decv["Serial"])[-12:-1])
        Debugs(in_datas="----------------------------------------------------")
        try:
            for in_loop in in_conf["Serial"]:
                if type(in_conf["Serial"][in_loop]) is bool:
                    continue
                if in_conf["Serial"][in_loop][3]:
                    if in_conf["Serial"][in_loop][0] == "P":
                        in_decv["Serial"].addSend(in_loop,
                                                  in_conf["Serial"][in_loop][0],
                                                  in_conf["Serial"][in_loop][1],
                                                  in_conf["Record"][in_conf["Serial"][in_loop][2]]['d'])
                    elif in_conf["Serial"][in_loop][0] == "G":
                        in_decv["Serial"].addSend(in_loop,
                                                  in_conf["Serial"][in_loop][0],
                                                  in_conf["Serial"][in_loop][1],
                                                  None)
                    else:
                        Debugs("Serial", "无法添加： " + in_loop, 2)
                    in_temp = in_decv["Serial"].getSend(in_loop)
                    if in_temp is None:
                        Debugs("Serial", "无法添加： " + in_loop, 2)
                    else:
                        Debugs("Serial", "添加：" + in_temp['name']
                               + "--" + in_temp['flag'] + '/' + in_temp['type'], 4)
                else:
                    Debugs("Serial", "跳过变量： " + in_loop, 2)
        except TypeError:
            Debugs("Serial", "无法打开串口！！", 3)
            Debugs("Serial", "AT " + Config.serial_port, 3)
            return 8
    # 自定初始化内容--------------------------------------------------------------------
    Define.InitalOthers(in_conf, in_decv, in_lock)
    # 进程解锁--------------------------------------------------------------------------
    in_lock.release()
    return 0


# 获取颜色信息 ---------------------------------------------------------------------------------------------------------
def MasterGetColor(in_conf, in_decv, in_lock, Picture):
    if not Config.master_jump:
        # 进程加锁-----------------------------------------------------
        in_lock.acquire()
        Debugs("MASTER", "GETTING COLOR..")
        in_decv['Serial'].addSend("COLO", "G", "S", "B")
        mainTmpNum = 0
        while in_decv['Serial'].getRecv('COLO') is None:
            mainTmpNum = mainTmpNum + 1
            if mainTmpNum % 100 == 0:
                Debugs("MASTER", "GET COLOR: 0x%02x" % (mainTmpNum // 100 % 256))
            in_decv['Serial'].comSend()
            in_decv['Serial'].comRecv()
            time.sleep(Config.serial_wait)
        Shared.Add(in_conf, "Receive", "COLO", in_decv['Serial'].getRecv('COLO')['data'])
        in_decv['Serial'].delSend('COLO')
        Debugs("MASTER", "我方兵种颜色：" + Shared.Get(in_conf, "Receive", "COLO"), 4)
        # 进程解锁-----------------------------------------------------
        in_lock.release()


# 启动线程模块 ---------------------------------------------------------------------------------------------------------
def StartProcesses(in_conf, in_pcss, in_lock, InternThread, Picture):
    ProcessThread = []
    Debugs("MASTER", "---------------", 0)
    Debugs("MASTER", " Start Process ", 0)
    Debugs("MASTER", "---------------", 0)
    for pcss_loop in in_pcss:
        if Config.use_threads:
            pcss_temp = Thread.Thread(target=pcss_loop,
                                      name=str(pcss_loop)[10:22]+"-00",
                                      args=(in_conf, in_lock, Picture))
        else:
            pcss_temp = Process(target=pcss_loop, name=str(pcss_loop)[10:22]+"-00", args=(in_conf, in_lock, Picture))
        InternThread[str(pcss_loop)[10:22] + "-00"] = [pcss_loop, (in_conf, in_lock, Picture)]
        pcss_temp.start()
        ProcessThread.append(pcss_temp)
    return ProcessThread


def SerialMainLoop(in_conf, in_decv, in_lock, in_thre):
    Extend.WatchDogLoop(in_conf, str(os.getpid()) + "-" + "Master")
    if not Config.serial_flag:
        return False
    time.sleep(Config.serial_wait)
    # 进程加锁-----------------------------------------------------
    in_lock.acquire()
    in_conf["ComNum"] = in_conf["ComNum"] + 1
    if Config.debug_tnum and in_conf["ComNum"] % 100 == 0:
        Debugs("SERIAL", "串口:   0x%05x" % (in_conf["ComNum"] // 100))
    # 修改发送变量------------------------------------------------------------------------------------------------------
    serial_flag = False
    for in_loop in in_conf["Serial"]:
        if type(in_conf["Serial"][in_loop]) is bool:
            continue
        if in_conf["Serial"][in_loop][3]:
            in_temp = in_decv["Serial"].getSend(in_loop)
            # 识别串口变量是否存在
            if in_temp is None:
                # 不存在则直接添加
                serial_flag = True
                if Config.serial_show:
                    Debugs("Serial", " 添加发送： " + in_loop, 0)
                if in_conf["Serial"][in_loop][0] == "P":
                    in_decv['Serial'].addSend(in_loop,
                                              in_conf["Serial"][in_loop][0],
                                              in_conf["Serial"][in_loop][1],
                                              in_conf["Record"][in_conf["Serial"][in_loop][2]]['d'])
                elif in_conf["Serial"][in_loop][0] == "G":
                    in_decv["Serial"].addSend(in_loop,
                                              in_conf["Serial"][in_loop][0],
                                              in_conf["Serial"][in_loop][1],
                                              None)
                else:
                    Debugs("Serial", "无法添加： " + in_loop, 2)
            else:
                # 存在则判断是否需要删除
                try:
                    serial_type = in_conf["Record"][in_conf["Serial"][in_loop][2]]['c']
                except KeyError:
                    continue
                if serial_type:
                    serial_flag = True
                if in_conf["Serial"][in_loop][0] == "G":
                    continue
                if not in_conf["Serial"][in_loop][3]:
                    # 需要删除
                    in_decv['Serial'].delSend(in_loop)
                    if Config.serial_show:
                        Debugs("Serial", "删除发送： " + in_loop, 0)
                elif Shared.Ptr(in_conf, "Record", in_conf["Serial"][in_loop][2]) is not None:
                    # 判断数据
                    if Config.serial_show:
                        Debugs("Serial", "存在数据： " + in_loop, 0)
                    # 进行更新
                    if in_conf["Record"][in_conf["Serial"][in_loop][2]]['c']:
                        in_decv['Serial'].putSend(in_loop, Shared.Get(in_conf,"Record",in_conf["Serial"][in_loop][2]))
                    if Config.serial_show:
                        Debugs("Serial", "修改发送： " + in_loop, 0)
    # 执行串口发送------------------------------------------------------------------------------------------------------
    if serial_flag:
        in_decv["Serial"].comSend()
    # 接收串口变量------------------------------------------------------------------------------------------------------
    if in_decv["Serial"].comRecv():
        for in_loop in in_conf["Serial"]:
            if type(in_conf["Serial"][in_loop]) is bool:
                continue
            if in_decv["Serial"].getRecv(in_loop) is None:
                if Config.serial_dels:
                    if not Config.serial_dttl:
                        Shared.Del(in_conf, "Receive", in_loop)
                    else:
                        if Shared.Ttl(in_conf, "Receive", in_loop):
                            Shared.Del(in_conf, "Receive", in_loop)
                if Config.serial_show:
                    Debugs("Serial", "删除接收： " + in_loop, 0)
        for in_temp in in_decv["Serial"].lstRecv():
            if Shared.Get(in_conf, "Receive", in_temp) is None:
                Shared.Add(in_conf, "Receive", in_temp, in_decv["Serial"].getRecv(in_temp)['data'])
                if Config.serial_show:
                    Debugs("Serial", "添加接收： " + in_temp, 0)
            else:
                Shared.Put(in_conf, "Receive", in_temp, in_decv["Serial"].getRecv(in_temp)['data'])
                if Config.serial_show:
                    Debugs("Serial", "修改接收： " + in_temp, 0)
    # 进程解锁---------------------------------------------------------------------------------------
    in_lock.release()


# 串口信息修改 ---------------------------------------------------------------------------------------------------------
def ComInformation(in_conf, in_decv, in_lock, in_thre):
    pass


# 进行无限循环 ---------------------------------------------------------------------------------------------------------
def MasterMainLoop(in_conf, in_decv, in_lock, InternThread, in_thre, MaxRelaunchs):
    mainLoopCount = 0
    try:
        while True:
            time.sleep(Config.master_wait)
            mainLoopCount = mainLoopCount + 1
            mainErrorFlag = False
            mainRelaunchs = False
            mainErrorCode = 0x00
            if Config.debug_tnum and mainLoopCount % 100 == 0:
                Debugs("MASTER", "主线程: 0x%05x" % (mainLoopCount // 100))
            SerialMainLoop(in_conf, in_decv, in_lock, in_thre)
            ComInformation(in_conf, in_decv, in_lock, in_thre)
            for loop_temp in in_conf["LoopDog"]:
                if time.time()-in_conf["LoopDog"][loop_temp] > Config.timeout_dog:
                    Debugs("MASTER", "线程触发超时！！", 3)
                    Debugs("MASTER", "AT:" + loop_temp, 3)
                    mainErrorFlag = True
                    mainErrorCode = 0x02
            for loop_temp in in_thre:
                if not loop_temp.is_alive():
                    loop_text = "[MP] " + str(loop_temp)[1:32] + str(loop_temp)[-19:-1]
                    Debugs("MASTER", "线程异常退出!!!",3)
                    Debugs("MASTER", str(loop_temp.name), 3)
                    Debugs(in_datas="----------------------------------------------------")
                    Debugs(in_datas=loop_text.replace("'",""))
                    Debugs(in_datas="----------------------------------------------------")
                    if Config.retrys_flag:
                        if "Camera" in loop_temp.name:
                            Debugs("MASTER", "摄像机无法重启!", 2)
                            Debugs("MASTER", str(loop_temp.name), 2)
                            mainErrorFlag = True
                            mainRelaunchs = False
                        elif loop_temp.name in MaxRelaunchs:
                            if MaxRelaunchs[loop_temp.name] < Config.retrys_maxs:
                                MaxRelaunchs[loop_temp.name] += 1
                                mainRelaunchs = True
                                mainErrorFlag = False
                            else:
                                Debugs("MASTER", "达重启次数上限!", 2)
                                Debugs("MASTER", str(loop_temp.name), 2)
                                mainErrorFlag = True
                                mainRelaunchs = False
                        else:
                            Debugs("MASTER", "首次重启此线程!", 2)
                            MaxRelaunchs[loop_temp.name] = 1
                            mainRelaunchs = True
                            mainErrorFlag = False
                    if mainRelaunchs:
                        Debugs("MASTER", "正在尝试重启!!!", 0)
                        Debugs("MASTER", "线程ID：%05d" %(loop_temp.pid), 0)
                        Debugs("MASTER", str(loop_temp.name), 0)
                        try:
                            loop_temp.kill()
                            loop_temp.terminate()
                            Extend.KillsProcess(loop_temp.pid)
                            if Config.use_threads:
                                loop_temp = Thread.Thread(target=InternThread[loop_temp.name][0],
                                                          name=loop_temp.name,
                                                          args=InternThread[loop_temp.name][1])
                            else:
                                loop_temp = Process(target=InternThread[loop_temp.name][0],
                                                    name=loop_temp.name,
                                                    args=InternThread[loop_temp.name][1])
                            loop_temp.start()
                            time.sleep(1)
                        except BaseException:
                            Debugs("MASTER", "重启时遇到问题!", 0)
                            mainErrorFlag = True
                    else:
                        if loop_temp.exitcode < len(Config.excode_text):
                            mainErrorCode = loop_temp.exitcode
                        else:
                            mainErrorCode = 0x01
                        mainErrorFlag = True
            if mainErrorFlag:
                for loop_data in in_thre:
                    Debugs("MASTER", "停止进程:"+str(loop_data.name)[6:-3], 1)
                    loop_data.terminate()
                Debugs("MASTER", "---------------", 0)
                return mainErrorCode
    except KeyboardInterrupt:
        Debugs("MASTER", "用户主动停止！！", 0)
        mainErrorCode = 0x00
        for loop_data in in_thre:
            Debugs("MASTER", "停止进程:" + str(loop_data.name)[6:-3], 1)
            loop_data.terminate()
        return mainErrorCode


if __name__ == '__main__':
    MemData = None
    Md5Data = hashlib.md5()
    TimeSTP = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    Md5Data.update(TimeSTP.encode("utf8"))
    Debugs(in_datas="■■■■■■■■■■■■■■■■■■■■■■■■■■")
    Debugs(in_datas="■ 机甲大师超级对抗赛四川大学火锅战队视觉组主进程 ■")
    Debugs(in_datas="■ RoboMaster RMUC SCU Hotpot Vision Main Process ■")
    Debugs(in_datas="■ %s %s ■" % (TimeSTP, Md5Data.hexdigest()[:-6]))
    Debugs(in_datas="■■■■■■■■■■■■■■■■■■■■■■■■■■")
    if Config.use_threads:
        sharedConfig = {}
        sharedTHLock = Thread.Lock()
        Picture = []
    else:
        if Config.use_MPSpawn:
            MPData.set_start_method('spawn')
        ManagerTools = Manager()
        sharedConfig = ManagerTools.dict()
        sharedTHLock = ManagerTools.Lock()
        if Config.use_MPQueue:
            Picture = Manager().Queue(Config.camera_maxp)
        else:
            if Config.ShareMemory:
                if Config.master_dvce == 'nx':
                    Picture = []
                    if Config.camera_type == 'ZED':
                        # ZED需要深度信息
                        for i in range(0, Config.camera_maxp):
                            img = shared_memory.SharedMemory(create=True,
                                                             size=camera_resol_widt * camera_resol_high * 3)
                            d_mat = np.zeros(shape=(camera_resol_widt, camera_resol_high, 4), dtype=np.float32)
                            depth = shared_memory.SharedMemory(create=True, size=d_mat.nbytes)
                            Picture.append([img, depth])
                    else:
                        for i in range(0, Config.camera_maxp):
                            img = shared_memory.SharedMemory(create=True,
                                                             size=camera_resol_widt * camera_resol_high * 3)
                            Picture.append(img)
                else:
                    Shareds = SharedMemoryManager()
                    Shareds.start()
                    Picture = []
                    for i in range(0,Config.camera_maxp):
                        Picture.append(Shareds.SharedMemory(size=camera_resol_widt * camera_resol_high * 3))
            else:
                Picture = ManagerTools.list()
            if Config.use_ImgLock:
                masterFRLock = []
                for i in range(0, Config.camera_maxp):
                    masterFRLock.append({
                        '#': i,
                        't': time.time(),
                        'l': False,
                    })
                    if not Config.ShareMemory:
                        Picture.append(None)
                sharedConfig['FRLock'] = masterFRLock
    masterThread = []
    masterDevice = {}
    FeedWatchDog = []
    InternThread = {}
    MaxRelaunchs = {}
    Excodes = MasterShowInfo(sharedConfig, masterThread, sharedTHLock, Picture)
    Excodes = MasterGetReady(sharedConfig, masterDevice, sharedTHLock, Picture)
    if Excodes == 0:
        MasterGetColor(sharedConfig, masterDevice, sharedTHLock, Picture)
        Threads = StartProcesses(sharedConfig, masterThread, sharedTHLock, InternThread, Picture)
        Excodes = MasterMainLoop(sharedConfig, masterDevice, sharedTHLock, InternThread, Threads, MaxRelaunchs)
        for main_temp in Threads:
            main_temp.terminate()
    Debugs("MASTER", "主线程已经结束!", 3)
    Debugs("MASTER", "返回代码： 0x0" + str(Excodes), 3)
    Debugs("MASTER", Config.excode_text[Excodes], 3)
    Debugs("MASTER", "---------------", 0)
    Debugs("MASTER", "  End Program  ", 0)
    Debugs("MASTER", "---------------", 0)
    Debugs(in_datas="----------------------------------------------------")
    exit(Excodes)