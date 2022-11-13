# ----------------------------------------------
#              SCURM_Vision_Extend
#               Coding By Pikachu
#                 拓展模块信息
#
#            LAST_UPDATE:JUL21/2021
# ----------------------------------------------
from module.ModuleDebugs import Debugs
from module.ModuleCamera import Camera
from module.ModuleShared import Shared
from module.ModuleConfig import *
import platform
import Config
import Define
import numpy
import time
import cv2
import os

# ZED相机自动import模块-------------------------------------------------------------------------------------------------
if Config.camera_type == "ZED":
    import pyzed.sl as sl
    from Utils import *


# 相机查看模块----------------------------------------------------------------------------------------------------------
def ImageWatcher(in_pfps, in_imgs, in_text="Unknow"):
    in_imgs = cv2.putText(in_imgs, str("%03d" % in_pfps), (0, 35), cv2.FONT_HERSHEY_COMPLEX, 1.5, (100, 200, 200), 3)
    try:
        if in_imgs is not None:
            cv2.imshow("Image Watcher of " + in_text, in_imgs)
            cv2.waitKey(1)
        else:
            if Config.empty_warn:
                Debugs("WATCHS", "传入图像为空!!!", 1)
    except cv2.error:
        Debugs("WATCHS", "请关闭图像输出!", 2)


# 看门狗模块------------------------------------------------------------------------------------------------------------
def WatchDogLoop(in_conf, in_spid):
    tp_data = in_conf["LoopDog"]
    tp_data[str(in_spid)] = time.time()
    in_conf["LoopDog"] = tp_data


# 进程销毁模块----------------------------------------------------------------------------------------------------------
def KillsProcess(in_pids=None):
    if in_pids is None:
        in_pids = os.getppid()
    Debugs("-KILL-", "结束进程：%05d" % (os.getppid()))
    if platform.system() == 'Windows':
        os.system("taskkill /PID " + str(in_pids))
    else:
        pass
        os.system("sudo kill -9 " + str(in_pids))

# 相机拓展模块----------------------------------------------------------------------------------------------------------
def ExtendCamera(in_conf, in_lock, Picture):
    if not Config.camera_flag:
        return False
    # 图形通用初始化信息 -----------------------------------------------------
    ImgBuff = None                                          # 存储图像缓存引用
    # 多进程共享内存预载 -----------------------------------------------------
    if not Config.use_threads:                              # 没有使用：多线程
        if not Config.use_MPQueue:                          # 且不使用系统队列
            if Config.ShareMemory:                          # 并且使用共享内存
                ImgBuff = Picture                           # 图像输出-Picture
    # 相机通用初始化信息 -----------------------------------------------------
    camera_counts_nums = 0                                  # 存储图片处理计数
    camera_showfp_pfps = 0                                  # 图像当前周期帧率
    camera_showfp_rfps = 0                                  # 图像上个周期计数
    camera_showfp_last = time.time()                        # 图像帧率时间计数
    camera_videos_nums = 0                                  # 视频存储帧率计数
    camera_videos_sfps = Config.video_sfps                  # 视频存储对象存储
    camera_format_info = cv2.VideoWriter_fourcc(*'XVID')    # 视频编码对象存储
    camera_videos_save = None                               # 视频输出对象计数
    camera_errors_nums = 0                                  # 相机当前周期错误
    camera_errors_last = time.time()                        # 相机当前周期时间
    camera_errors_line = 0                                  # 已连续错误的帧数
    camera_nashor_last = False                              # 上次是否是打大符
    camera_colors_type = Shared.Get(in_conf, "Receive", "COLO") # 我方兵种颜色
    # ------------------------------------------------------------------------
    if Config.camera_type == "MV":
        # MV-摄像机 ----------------------------------------------------------
        Cameras = Camera(0)
        Cameras.shot()
        if Config.rgb_filters:
            Cameras.gain(in_text=["B" if camera_colors_type == "R" else "R"][0])
    elif Config.camera_type == "ZED":
        # ZED摄像机 ----------------------------------------------------------
        Cameras = Camera(0, "ZED", Config.svofilepath)
    else:
        # 相机设置错误--------------------------------------------------------
        Debugs("CAMREA", "相机类型设定有误！", 3)
        return False
    # ------------------------------------------------------------------------
    # 系统主循环--------------------------------------------------------------------------------------------------------
    while True:
        WatchDogLoop(in_conf, str(os.getpid()) + "-" + __name__)
        # ---------------------------------------------------------------------------------
        if Config.master_sync:
            while not in_conf["FPLock"]:
                pass
        # ---------------------------------------------------------------------------------
        if Config.camera_wait > 0:
            time.sleep(Config.camera_wait)
        if Config.debug_tnum and camera_counts_nums % 100 == 0:
            Debugs("CAMERA", "摄像头: 0x%05x" % (camera_counts_nums // 100))
        if Config.debug_bimg and camera_counts_nums % 100 == 0:
            if not Config.use_threads and Config.use_MPQueue:
                Debugs("CAMREA", "图像缓存:  %04d" % Picture.qsize())
            elif not Config.ShareMemory:
                Debugs("CAMREA", "图像缓存:  %04d" % len(Picture))
            else:
                Debugs("CAMREA", "固定缓存:  %04d" % Config.camera_maxp)
        camera_counts_nums = camera_counts_nums + 1
        # 判断是否达到掉帧阈值----------------------------------------------------------------
        if Config.endure_flag:
            if camera_errors_line >= Config.endure_line:
                Debugs("CAMREA", "连续掉帧限制!!!", 3)
                Debugs("CAMREA", "自动停止相机!!!", 3)
                Cameras.exit()
                exit(5)
                return 5
            if Config.endure_type and time.time() - camera_errors_last > Config.endure_time:
                if camera_errors_nums >= Config.endure_maxp:
                    Debugs("CAMREA", "周期掉帧限制!!!", 3)
                    Debugs("CAMREA", "自动停止相机!!!", 3)
                    exit(3)
                    return 3
                camera_errors_nums = 0
            elif camera_errors_nums >= Config.endure_maxp:
                Debugs("CAMREA", "总共掉帧限制!!!", 3)
                Debugs("CAMREA", "自动停止相机!!!", 3)
                exit(4)
                return 4
        # ----------------------------------------------------------------------------------
        camrea_tmpimg = Cameras.shot()
        if camrea_tmpimg is None:
            Debugs("CAMREA", "有一帧图像掉了!", 2)
            if Config.master_sync:
                in_conf["FPLock"] = False
            if Config.endure_flag:
                camera_errors_nums += 1
                camera_errors_line += 1
            else:
                Cameras.exit()
                exit(4)
            continue
        else:
            camera_errors_line = 0
        # 使用多进程的情况 -------------------------------------------------------------------
        if not Config.use_threads:
            # 使用分离式锁，读写锁操作-----------------------------
            if Config.use_ImgLock:
                camrea_nums = Config.camera_maxp
                # 尝试N次寻找  ------------------------------------
                while camrea_nums > 0:
                    camrea_oldest = float('inf')
                    camrea_oldsid = -1
                    # 寻找合适（最新/最老）的图片------------------
                    for camrea_fploop in in_conf['FRLock']:
                        if camrea_fploop['l']:
                            continue
                        if camrea_fploop['t'] < camrea_oldest:
                            camrea_oldest = camrea_fploop['t']
                            camrea_oldsid = camrea_fploop['#']
                    # 如果找到了 -----------------------------------
                    if camrea_oldsid >= 0:
                        # 先给分离式锁加锁--------------------------
                        camrea_tmpobj = {
                            '#': camrea_oldsid,
                            't': time.time(),
                            'l': True,
                        }
                        # 安全模式下需要二次加锁---------------------
                        if Config.Img_SafeMod:
                            in_lock.acquire()
                        # 写入分离式锁来进行加锁---------------------
                        camrea_tmpinf = in_conf['FRLock']
                        camrea_tmpinf[camrea_oldsid] = camrea_tmpobj
                        in_conf['FRLock'] = camrea_tmpinf
                        # 安全模式下需要进行解锁---------------------
                        if Config.Img_SafeMod:
                            in_lock.release()
                        # 将图像写入共享数据里面---------------------------------------------------
                        if Config.ShareMemory:
                            # 图像缓存读不到-------------------------------------------------------
                            if ImgBuff is None:
                                continue
                            # ZED模式写入----------------------------------------------------------
                            if Config.camera_type == 'ZED':
                                # 图像信息
                                ImgBuff[camrea_oldsid][0].buf[:] = bytes(camrea_tmpimg[0])
                                # 深度信息
                                depth = np.ndarray(buffer=camrea_tmpimg[1], dtype=np.uint8,
                                                   shape=camera_resol_high * camera_resol_widt * 4)
                                ImgBuff[camrea_oldsid][1].buf[:] = bytes(depth)
                            # MV 模式写入----------------------------------------------------------
                            elif Config.camera_type == 'MV':
                                ImgBuff[camrea_oldsid].buf[:] = bytes(camrea_tmpimg)
                            else:
                                continue
                        # 非共享内存直接写入-------------------------------------------------------
                        else:
                            Picture[camrea_oldsid] = camrea_tmpimg
                        # 解锁分离式进程锁，改写---------------------
                        camrea_tmpobj['l'] = False
                        # 安全模式下需要二次加锁---------------------
                        if Config.Img_SafeMod:
                            in_lock.acquire()
                        # 写入分离式锁来进行解锁---------------------
                        camrea_tmpinf = in_conf['FRLock']
                        camrea_tmpinf[camrea_oldsid] = camrea_tmpobj
                        in_conf['FRLock'] = camrea_tmpinf
                        # 安全模式下需要进行解锁---------------------
                        if Config.Img_SafeMod:
                            in_lock.release()
                        break
                    else:
                        camrea_nums = camrea_nums - 1
            # 使用队列，通过全局锁直接读写---------------------------
            elif Config.use_MPQueue:
                in_lock.acquire()
                Picture.put(camrea_tmpimg, timeout=0)
                in_lock.release()
        # 多线程情况，通过全局锁直接读写------------------------------
        else:
            in_lock.acquire()
            Picture.append(camrea_tmpimg)
            in_lock.release()
        # 帧率统计-------------------------------------------------------------
        camera_showfp_rfps = camera_showfp_rfps + 1
        camrea_showfp_nowt = time.time()
        if camrea_showfp_nowt - camera_showfp_last >= 1:
            # 大符模式检测与修改----------------------------------------------
            if Config.rgb_filters:
                camera_nashor_flag = Shared.Get(in_conf, "Record", "TYPE")
            if camera_nashor_last != camera_nashor_flag:
                camera_nashor_last = camera_nashor_flag
                if camera_nashor_flag:
                    Cameras.gain(in_text=camera_colors_type)
                else:
                    Cameras.gain(in_text=["B" if camera_colors_type == "R" else "R"])
            # ------------------------------------------------------------------
            camera_showfp_last = camrea_showfp_nowt
            if Config.debug_tfps:
                Debugs("CAMREA", "相机帧率：  %03d" % camera_showfp_rfps)
            camera_showfp_pfps = camera_showfp_rfps
            camera_showfp_rfps = 0
        # 图像输出--------------------------------------------------------------
        if Config.debug_imgs:
            if Config.camera_type == 'ZED':
                ImageWatcher(camera_showfp_pfps, camrea_tmpimg[0], "Camera")
            else:
                ImageWatcher(camera_showfp_pfps, camrea_tmpimg, "Camera")
        # 保存录像视频 ------------------------------------------------------------------------------
        if Config.debug_save:
            if camera_videos_nums == 0 or camera_videos_save is None:
                # 打开文件输出-----------------------------------------------------------------------
                camera_videos_save = cv2.VideoWriter('Videos/OutPut-' +
                                                     time.strftime("%Y%m%d%H%M%S", time.localtime())
                                                     + '.avi',
                                                     camera_format_info,
                                                     camera_videos_sfps,
                                                     (camera_resol_widt, camera_resol_high))
            camera_videos_nums = camera_videos_nums + 1
            # 执行文件输入---------------------------------------------------------------------------
            if camera_videos_save is not None:
                if Config.camera_type == "MV":
                    camera_videos_save.write(camrea_tmpimg)
                elif Config.camera_type == "ZED":
                    camera_videos_save.write(camrea_tmpimg[0])
            # 时间到！释放---------------------------------------------------------------------------
            if camera_videos_nums >= Config.video_time * Config.video_sfps:
                camera_videos_nums = 0
                if camera_videos_save is not None:
                    camera_videos_save.release()
                    camera_videos_save = None
                if Config.video_auto:
                    camera_videos_sfps = camera_showfp_pfps
        # -------------------------------------------------------------------
        if not Config.use_threads and Config.use_ImgLock:
            # 使用多进程且分离式锁，直接继续循环-----------------------------
            if Config.master_sync:
                in_conf["FPLock"] = False                    # 释放垂直同步锁
            continue
        if Config.use_threads or not Config.use_MPQueue:
            # 使用多线程或者没有用队列，删除多余-----------------------------
            if len(Picture) > Config.camera_maxp:
                Picture = Picture[Config.camera_maxp:]       # 删除溢出的图像
        else:
            # 使用队列并且多进程，清空一半内容-------------------------------
            if Picture.full():
                for i in range(0, Config.camera_maxp // 2):  # 前删除一半图像
                    Picture.get(0)
        # 其他情况（设置错误）重置垂直同步锁---------------------------------
        if Config.master_sync:
            in_conf["FPLock"] = False                        # 释放垂直同步锁
        # -------------------------------------------------------------------
    # 主循环结束--------------------------------------------------------------------------------------------------------


def ExtendArmors(in_conf, in_lock, Picture):
    armors_last = 0
    armors_time = 0
    armors_showfp_last = time.time()
    armors_showfp_rfps = 0
    armors_showfp_pfps = 0
    main_arm_num = 0
    ImgSize = 0
    ImgBuff = None
    if not Config.use_threads:
        if not Config.use_MPQueue:
            if Config.ShareMemory:
                ImgBuff = Picture
                ImgSize = camera_resol_widt * camera_resol_high * 3
    extend_datas = Define.InitalArmors(in_conf)
    while True:
        WatchDogLoop(in_conf, str(os.getpid()) + "-" + __name__)
        # ----------------------------------------------------------------
        if Config.master_sync:
            while in_conf["FPLock"]:
                pass
        # ----------------------------------------------------------------
        time.sleep(Config.armors_wait)
        if main_arm_num % 100 == 0:
            if Config.debug_tnum:
                Debugs("ARMORS", "装甲板: 0x%05x" % (main_arm_num // 100))
        main_arm_num = main_arm_num + 1
        # ----------------------------------------------------------------
        try:
            # 不使用系统多线程管理--------------------------------------------------------------------------------------
            armors_pops = False
            if not Config.use_threads:
                # 不使用分布式进程锁------------------------------------------------------------------------------------
                if Config.use_ImgLock:
                    # 先固定缓存数量------------------------------------------------------------------------------------
                    armors_nums = Config.camera_maxp
                    while armors_nums > 0:
                        if Config.Img_NewImgs:
                            armors_oldest = 0
                        else:
                            armors_oldest = float('inf')
                        armors_oldsid = -1
                        for armors_fploop in in_conf['FRLock']:
                            if armors_fploop['l']:
                                continue
                            if not Config.Img_NewImgs and armors_fploop['t'] < armors_oldest:
                                armors_oldest = armors_fploop['t']
                                armors_oldsid = armors_fploop['#']
                            elif Config.Img_NewImgs and armors_fploop['t'] > armors_oldest:
                                armors_oldest = armors_fploop['t']
                                armors_oldsid = armors_fploop['#']
                        if armors_oldsid >= 0 and armors_time < armors_oldest:
                            armors_tmpobj = {
                                '#': armors_oldsid,
                                't': armors_oldest,
                                'l': True,
                            }
                            if Config.Img_SafeMod:
                                in_lock.acquire()
                            if Config.Img_ReadMod:
                                armors_tmpinf = in_conf['FRLock']
                                armors_tmpinf[armors_oldsid] = armors_tmpobj
                                in_conf['FRLock'] = armors_tmpinf
                            if Config.Img_SafeMod:
                                in_lock.release()
                            if Config.ShareMemory:
                                if ImgBuff is None:
                                    continue
                                if Config.camera_type == 'ZED':
                                    img = numpy.ndarray(buffer=ImgBuff[armors_oldsid][0].buf, dtype=numpy.uint8,
                                                        shape=(camera_resol_widt, camera_resol_high, 3))
                                    depth = numpy.ndarray(buffer=ImgBuff[armors_oldsid][1].buf, dtype=numpy.float16,
                                                          shape=(camera_resol_widt, camera_resol_high, 4))
                                    armors_imgs = [img, depth]
                                else:
                                    ReadShareds = ImgBuff[armors_oldsid].buf
                                    armors_imgs = numpy.ndarray(buffer=ReadShareds, dtype=numpy.uint8,
                                                                shape=(camera_resol_high, camera_resol_widt, 3))
                            else:
                                armors_imgs = Picture[armors_oldsid]
                            armors_tmpobj['l'] = False
                            if Config.Img_SafeMod:
                                in_lock.acquire()
                            if Config.Img_ReadMod:
                                armors_tmpinf = in_conf['FRLock']
                                armors_tmpinf[armors_oldsid] = armors_tmpobj
                                in_conf['FRLock'] = armors_tmpinf
                            if Config.Img_SafeMod:
                                in_lock.release()
                            armors_last = armors_time
                            armors_time = armors_oldest
                            armors_nums = -1
                            break
                        else:
                            armors_nums = armors_nums - 1
                    if armors_nums == 0:
                        if Config.master_sync:
                            in_conf["FPLock"] = True
                        continue
                elif Config.use_MPQueue:
                    if Picture.qsize() > 0:
                        in_lock.acquire()
                        armors_imgs = Picture.get(0)
                        in_lock.release()
                    else:
                        if Config.armors_flag:
                            Debugs("ARMORS", "队列里没有图像", 1)
                        if Config.master_sync:
                            in_conf["FPLock"] = True
                        continue
                else:
                    armors_pops = True
            else:
                armors_pops = True
            if armors_pops:
                if len(Picture) > 0:
                    in_lock.acquire()
                    armors_imgs = Picture.pop(0)
                    in_lock.release()
                else:
                    if Config.armors_flag:
                        Debugs("ARMORS", "队列里没有图像", 1)
                    if Config.master_sync:
                        in_conf["FPLock"] = True
                    continue
        except ValueError or BaseException:
            Debugs("ARMORS", "严重的图像问题", 3)
            if Config.master_sync:
                in_conf["FPLock"] = True
            continue
        # 执行识别模块处理-------------------------------------------------
        armors_delt = armors_time - armors_last
        Define.DefineArmors(in_conf, armors_imgs, armors_delt, extend_datas)
        # 进行帧率统计-----------------------------------------------------
        armors_showfp_rfps = armors_showfp_rfps + 1
        armors_showfp_nowt = time.time()
        if armors_showfp_nowt - armors_showfp_last >= 1:
            armors_showfp_last = armors_showfp_nowt
            if Config.debug_tfps:
                Debugs("ARMORS", "识别帧率： %04d" % armors_showfp_pfps)
            armors_showfp_pfps = armors_showfp_rfps
            armors_showfp_rfps = 0
        # 输出图像窗口------------------------------------------------------
        if Config.debug_aimg:
            ImageWatcher(armors_showfp_pfps, armors_imgs, "Armors")
        # 释放垂直同步锁----------------------------------------------------
        if Config.master_sync:
            in_conf["FPLock"] = True
        # ------------------------------------------------------------------
    # 识别进程结束------------------------------------------------------------------------------------------------------


# 将方法添加进线程------------------------------------------------------------------------------------------------------
extendProcess = [ExtendCamera, ExtendArmors]
