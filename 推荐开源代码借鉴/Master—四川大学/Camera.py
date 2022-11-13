# ----------------------------------------------
#              SCURM_Vision_Camera
#               Coding By Pikachu
#                 相机校准工具
#
#            LAST_UPDATE:JUL21/2021
# ----------------------------------------------
from module.ModuleDebugs import Debugs
from module.ModuleCamera import Camera
from module.ModuleConfig import *
import platform
import Config
import time
import cv2
import os


# ----------------------------------------------
def camera_clrs():
    osName = platform.system()
    if osName == 'Windows':
        os.system("cls")
        os.system("mode con cols=52 lines=40")
        os.system("color 3f")
    elif osName == 'Linux':
        os.system("clear")
        os.system("xrandr -s 420x640")
    elif osName == 'Darwin':
        os.system("clear")
    print("")


# --------------------------------------------------------------------------------------------------
def camera_draw(tmp,fps,oft=True):
    # 顶部数据展示 --------------------------------------------------------------
    tmp = cv2.putText(tmp,fps,
                      (0, 50), cv2.FONT_HERSHEY_COMPLEX, 2,
                      (100, 200, 200), 2)
    # 底栏数据展示 --------------------------------------------------------------
    tmp = cv2.putText(tmp, "AAC[",
                      (0, camera_resol_high-20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (255, 255, 255), 2)
    tmp = cv2.putText(tmp, str(camera_color_data[0]),
                      (70, camera_resol_high-20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (0, 0, 255), 2)
    tmp = cv2.putText(tmp, str(camera_color_data[1]),
                      (130, camera_resol_high-20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (0, 255, 0), 2)
    tmp = cv2.putText(tmp, str(camera_color_data[2]),
                      (190, camera_resol_high-20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (255, 0, 0), 2)
    tmp = cv2.putText(tmp, "]ISO",
                      (240, camera_resol_high-20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (255, 255, 255), 2)
    tmp = cv2.putText(tmp, str(1000000 // camera_resol_sfps),
                      (315, camera_resol_high-20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (0, 255, 255), 2)
    tmp = cv2.putText(tmp, "HAG(",
                      (420, camera_resol_high-20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (255, 255, 255), 2)
    tmp = cv2.putText(tmp, str(camera_gain_color['R']),
                      (500, camera_resol_high-20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (0, 0, 255), 2)
    tmp = cv2.putText(tmp, str(camera_gain_color['G']),
                      (755, camera_resol_high - 20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (0, 255, 0), 2)
    tmp = cv2.putText(tmp, str(camera_gain_color['B']),
                      (1010, camera_resol_high - 20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (255, 0, 0), 2)
    tmp = cv2.putText(tmp, ")",
                      (1265, camera_resol_high - 20), cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (255, 255, 255), 2)
    # 中央数据展示 ------------------------------------------------------------------------------
    pos = [i for i in tmp[int(camera_resol_high // 2), int(camera_resol_widt // 2)]]
    tmp = cv2.rectangle(tmp,
                        (round(camera_resol_widt / 2) - 100, round(camera_resol_high / 2) - 100),
                        (round(camera_resol_widt / 2) + 100, round(camera_resol_high / 2) + 100),
                        (255, 255, 255), 2)
    tmp = cv2.rectangle(tmp,
                        (round(camera_resol_widt / 2) - 50, round(camera_resol_high / 2) - 50),
                        (round(camera_resol_widt / 2) + 50, round(camera_resol_high / 2) + 50),
                        (0, 255, 0), 2)
    tmp = cv2.line(tmp, (round(camera_resol_widt / 2) - 30, round(camera_resol_high / 2)),
                   (round(camera_resol_widt / 2) + 30, round(camera_resol_high / 2)),
                   (0, 255, 255), 2, cv2.LINE_AA)
    tmp = cv2.line(tmp, (round(camera_resol_widt / 2), round(camera_resol_high / 2) - 30),
                   (round(camera_resol_widt / 2), round(camera_resol_high / 2) + 30),
                   (0, 255, 255), 2, cv2.LINE_AA)
    if oft:
        tmp = cv2.putText(tmp, "RGB",
                          (round(camera_resol_widt / 2) + 55, round(camera_resol_high / 2) - 38),
                          cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 255), 1)
        tmp = cv2.putText(tmp, "0x%02X" % (pos[2]),
                          (round(camera_resol_widt / 2) + 55, round(camera_resol_high / 2) - 24),
                          cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 255), 1)
        tmp = cv2.putText(tmp, "0x%02X" % (pos[1]),
                          (round(camera_resol_widt / 2) + 55, round(camera_resol_high / 2) - 12),
                          cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 255, 50), 1)
        tmp = cv2.putText(tmp, "0x%02X" % (pos[0]),
                          (round(camera_resol_widt / 2) + 55, round(camera_resol_high / 2)),
                          cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 50, 50), 1)
        tmp = cv2.putText(tmp, "--------",
                          (round(camera_resol_widt / 2) + 55, round(camera_resol_high / 2) + 13),
                          cv2.FONT_HERSHEY_COMPLEX, 0.2, (255, 255, 255), 1)
        tmp = cv2.putText(tmp, "E-%02X" % (pos[2]),
                          (round(camera_resol_widt / 2) + 55, round(camera_resol_high / 2) + 26),
                          cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 255), 1)
        tmp = cv2.putText(tmp, "E-%02X" % (pos[1]),
                          (round(camera_resol_widt / 2) + 55, round(camera_resol_high / 2) + 38),
                          cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 255, 50), 1)
        tmp = cv2.putText(tmp, "E-%02X" % (pos[0]),
                          (round(camera_resol_widt / 2) + 55, round(camera_resol_high / 2) + 50),
                          cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 50, 50), 1)
    return tmp

# -------------------------------------------------------------------------------------------------
def camera_wrgb(tmp):
    tmp = cv2.rectangle(tmp,
                        (round(camera_resol_widt / 2) - 300, round(camera_resol_high / 2) - 100),
                        (round(camera_resol_widt / 2) - 100, round(camera_resol_high / 2) + 100),
                        (255, 255, 255), 2)
    tmp = cv2.rectangle(tmp,
                        (round(camera_resol_widt / 2) + 100, round(camera_resol_high / 2) - 100),
                        (round(camera_resol_widt / 2) + 300, round(camera_resol_high / 2) + 100),
                        (255, 255, 255), 2)
    tmp = cv2.rectangle(tmp,
                        (round(camera_resol_widt / 2) - 250, round(camera_resol_high / 2) - 50),
                        (round(camera_resol_widt / 2) - 150, round(camera_resol_high / 2) + 50),
                        (0, 255, 0), 2)
    tmp = cv2.rectangle(tmp,
                        (round(camera_resol_widt / 2) + 150, round(camera_resol_high / 2) - 50),
                        (round(camera_resol_widt / 2) + 250, round(camera_resol_high / 2) + 50),
                        (0, 255, 0), 2)
    tmp = cv2.line(tmp, (round(camera_resol_widt / 2) - 230, round(camera_resol_high / 2)),
                   (round(camera_resol_widt / 2) - 170, round(camera_resol_high / 2)),
                   (0, 255, 255), 2, cv2.LINE_AA)
    tmp = cv2.line(tmp, (round(camera_resol_widt / 2) - 200, round(camera_resol_high / 2) - 30),
                   (round(camera_resol_widt / 2) - 200, round(camera_resol_high / 2) + 30),
                   (0, 255, 255), 2, cv2.LINE_AA)
    tmp = cv2.line(tmp, (round(camera_resol_widt / 2) + 170, round(camera_resol_high / 2)),
                   (round(camera_resol_widt / 2) + 230, round(camera_resol_high / 2)),
                   (0, 255, 255), 2, cv2.LINE_AA)
    tmp = cv2.line(tmp, (round(camera_resol_widt / 2) + 200, round(camera_resol_high / 2) - 30),
                   (round(camera_resol_widt / 2) + 200, round(camera_resol_high / 2) + 30),
                   (0, 255, 255), 2, cv2.LINE_AA)
    tmp = cv2.putText(tmp, "R",
                      (round(camera_resol_widt / 2) - 250, round(camera_resol_high / 2) - 120),
                      cv2.FONT_HERSHEY_COMPLEX, 5.0,
                      (100, 100, 255), 5)
    tmp = cv2.putText(tmp, "G",
                      (round(camera_resol_widt / 2) - 50, round(camera_resol_high / 2) - 120),
                      cv2.FONT_HERSHEY_COMPLEX, 5.0,
                      (100, 255, 100), 5)
    tmp = cv2.putText(tmp, "B",
                      (round(camera_resol_widt / 2) + 150, round(camera_resol_high / 2) - 120),
                      cv2.FONT_HERSHEY_COMPLEX, 5.0,
                      (255, 100, 100), 5)
    return tmp

# ------------------------------------------------------------------------------------------------
def camera_gain(tmp, i):
    tmp = cv2.putText(tmp, "Put",
                      (round(camera_resol_widt / 2) - 270, round(camera_resol_high / 2) + 150),
                      cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (255, 255, 255), 2)
    tmp = cv2.putText(tmp, color_l[i],
                      (round(camera_resol_widt / 2) - 220, round(camera_resol_high / 2) + 150),
                      cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (255 if i == "B" else 0, 0, 255 if i == "R" else 0), 2)
    tmp = cv2.putText(tmp, "LED in",
                      (round(camera_resol_widt / 2) - 120, round(camera_resol_high / 2) + 150),
                      cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (255, 255, 255), 2)
    tmp = cv2.putText(tmp, "Green",
                      (round(camera_resol_widt / 2) + 5, round(camera_resol_high / 2) + 150),
                      cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (100, 200, 200), 2)
    tmp = cv2.putText(tmp, "Rectangle",
                      (round(camera_resol_widt / 2) + 120, round(camera_resol_high / 2) + 150),
                      cv2.FONT_HERSHEY_COMPLEX, 1.0,
                      (255, 255, 255), 2)
    return tmp

# -------------------------------------------------------------------------------------
def camera_data(in_file, in_name, in_data="", in_text="", in_nums=0, in_info=""):
    if  in_file is None:
        Debugs("CAMREA", "文件的路径不对!", 2)
        return False
    data_flag = False
    data_temp = []
    with open(in_file, "r", encoding="utf-8") as data_file:
        data_line = data_file.readlines()
        Debugs("CAMREA", "正在查找.......", 2)
        for data_loop in data_line:
            if in_name in data_loop:
                if in_info != "":
                    data_info = in_info
                else:
                    data_info = in_name + " = " + in_data
                    if in_text != "":
                        try:
                            for i in range(0,int(in_nums)):
                                data_info += " "
                        except ValueError:
                            Debugs("CAMREA", "空格的数量不对!", 2)
                        data_info += " # " + in_text
                data_info += "\n"
                data_temp.append(data_info)
                Debugs(in_datas="----------------------------------------------------")
                Debugs(in_datas="写入了参数: %17s 值: %18s" % (in_name, data_info))
                Debugs(in_datas="----------------------------------------------------")
                data_flag = True
            else:
                data_temp.append(data_loop)
        data_file.close()
    if not data_flag:
        Debugs("CAMREA", "写入的参数不对!", 2)
        return False
    else:
        with open(in_file+".new","w",encoding="utf-8") as data_file:
            for data_loop in data_temp:
                data_file.writelines(data_loop)
        if os.path.exists(in_file + ".old"):
            os.remove(in_file + ".old")
        os.rename(in_file, in_file + ".old")
        os.rename(in_file + ".new", in_file)
        Debugs("CAMREA", "参数成功写入了!", 2)
        data_file.close()
        return True


# -------------------------------------------------------------------------------------
def camera_menu():
    camera_clrs()
    Debugs(in_datas="■■■■■■■■■■■■■■■■■■■■■■■■■■")
    Debugs(in_datas="■         四川大学火锅战队视觉组相机工具         ■")
    Debugs(in_datas="■         SCU Hotpot Vision Camera Tools         ■")
    Debugs(in_datas="■■■■■■■■■■■■■■■■■■■■■■■■■■")
    print()
    Debugs(in_datas="----------------------------------------------------")
    Debugs(in_datas="|                     工具列表                     |")
    Debugs(in_datas="----------------------------------------------------")
    Debugs(in_datas="|               0.查看指定相机图像                 |")
    Debugs(in_datas="|                                                  |")
    Debugs(in_datas="|               1.校准相机感光时间（调整曝光度）   |")
    Debugs(in_datas="|                                                  |")
    Debugs(in_datas="|               2.校准硬件滤光参数（自动筛颜色）   |")
    Debugs(in_datas="|                                                  |")
    Debugs(in_datas="|               3.校准静态颜色基准（手动白平衡）   |")
    Debugs(in_datas="|                                                  |")
    Debugs(in_datas="|               4.棋盘图自动化校准（测量畸变值）   |")
    Debugs(in_datas="|                                                  |")
    Debugs(in_datas="|               q.关闭并退出本程序                 |")
    Debugs(in_datas="----------------------------------------------------")


# --------------------------------------------------------------------------
def camera_show():
    if Config.camera_type == "MV":
        Cameras = Camera(0)
    elif Config.camera_type == "ZED":
        Cameras = Camera(0, "ZED", Config.svofilepath)
    else:
        Debugs("CAMREA", "相机类型设定有误！", 3)
        return 1
    camera_show_rfps = 0
    camera_show_pfps = 0
    camera_show_last = time.time()
    Cameras.gain(in_data=camera_color_data)
    while (cv2.waitKey(1) & 0xFF) != ord('q'):
        camera_show_rfps = camera_show_rfps + 1
        if time.time() - camera_show_last >= 1:
            camera_show_pfps = camera_show_rfps
            camera_show_rfps = 0
            camera_show_last = time.time()
        tmp = camera_draw(Cameras.shot(),str(camera_show_pfps))
        cv2.imshow("Image Watcher - Press q to Return", tmp)
    Debugs("CAMREA", "用户主动退出程序！", 4)
    cv2.destroyAllWindows()
    Cameras.exit()
    return 0


# ----------------------------------------------------------------
def camera_conf(in_type):
    if Config.camera_type == "MV":
        Cameras = Camera(0)
    elif Config.camera_type == "ZED":
        Cameras = Camera(0, "ZED", Config.svofilepath)
    else:
        Debugs("CAMREA", "相机类型设定有误！", 3)
        return 1
    camera_show_rfps = 0
    camera_show_pfps = 0
    camera_show_last = time.time()
    nums = 0
    for i in define_set_colors:
        flag = True
        loop = False
        maxs = 0
        while loop!=False or flag!=False:
            if flag:
                Debugs("CAMREA", "正在校准: "+color_l[i], 0)
                Debugs("CAMREA", "将灯条置于框中!", 0)
                Debugs("CAMREA", "然后按A继续!!!!", 0)
            else:
                Debugs("CAMREA", "校准中请勿移动.", 0)
            if in_type == "gain":
                data = camera_gain_color[i]
                Cameras.gain(in_data=data)
            elif in_type == "wrgb":
                data = camera_color_data
                Cameras.gain(in_data=data)
            while (flag and (cv2.waitKey(1) & 0xFF) != ord('a')) \
                or loop:
                camera_show_rfps = camera_show_rfps + 1
                if time.time() - camera_show_last >= 1:
                    camera_show_pfps = camera_show_rfps
                    camera_show_rfps = 0
                    camera_show_last = time.time()
                tmp = Cameras.shot()
                if loop:
                    pos = [i for i in tmp[int(camera_resol_high // 2), int(camera_resol_widt // 2)]]
                    if in_type == "time":
                        data = Cameras.time()
                        if maxs % 100 == 0:
                            Debugs("CAMREA", "当前曝光%07.2f"%data, 0)
                        ends = False
                        if maxs > define_all_maxtry:
                            Debugs("CAMREA", "超最大迭代次数", 4)
                            ends = True
                        if pos[2-nums] >= define_iso_target and pos[nums] <= define_iso_others:
                            ends = True
                        if ends:
                            Debugs("CAMREA", "满足条件，结束", 4)
                            camera_data("module/ModuleConfig.py",
                                        "camera_exposure_t",
                                        "%5d"%(int(data)),
                                        in_text="相机曝光时间",
                                        in_nums=1)
                            loop = False
                            flag = False
                            break
                        elif pos[2-nums]<define_iso_target:
                            if maxs % 100 == 0:
                                Debugs("CAMREA", "目标颜色不符合!", 0)
                            data += define_iso_setadd
                            Cameras.time(data)
                        elif pos[nums] > define_iso_others:
                            if maxs % 100 == 0:
                                Debugs("CAMREA", "其他颜色不符合!", 0)
                            data -= define_iso_setadd
                            Cameras.time(data)
                        tmp = camera_draw(tmp, str(camera_show_pfps), not flag)
                    elif in_type == "gain":
                        data = list(Cameras.gain())
                        ends = False
                        if maxs % 100 == 0:
                            Debugs("CAMREA", "当前:%s" % (str(data)), 0)
                        if maxs > define_all_maxtry:
                            Debugs("CAMREA", "超最大迭代次数", 4)
                            ends = True
                        if pos[2 - nums] >= define_rgb_target and pos[nums] <= define_rgb_others:
                            Debugs("CAMREA", "满足条件，结束", 4)
                            ends = True
                        if ends:
                            camera_data("module/ModuleConfig.py", "\"" + i + "\"",
                                        in_info="    \"%s\": [%3d,%4d,%4d]," % (i, data[0], data[1], data[2]))
                            loop = False
                            flag = False
                            break
                        elif pos[2 - nums] < define_rgb_target:
                            if maxs % 100 == 0:
                                Debugs("CAMREA", "目标颜色不符合!", 0)
                            data[nums] += define_rgb_setadd
                            Cameras.gain(in_data=data)
                        elif pos[nums] > define_rgb_others:
                            if maxs % 100 == 0:
                                Debugs("CAMREA", "其他颜色不符合!", 0)
                            data[nums] -= define_rgb_setadd
                            Cameras.gain(in_data=data)
                        tmp = camera_draw(tmp, str(camera_show_pfps), not flag)
                    elif in_type == "wrgb":
                        rgb = [[i for i in tmp[int(camera_resol_high // 2), int((camera_resol_widt) // 2 - 200)]],
                               [i for i in tmp[int(camera_resol_high // 2), int((camera_resol_widt) // 2)]],
                               [i for i in tmp[int(camera_resol_high // 2), int((camera_resol_widt) // 2 +200)]]]
                        ends = False
                        data = list(Cameras.gain())
                        if maxs > define_all_maxtry:
                            Debugs("CAMREA", "超最大迭代次数", 4)
                            ends = True
                        numb = 0
                        frgb = True
                        if maxs % 100 == 0:
                            Debugs("CAMREA", "当前次数: %5d" % (maxs), 4)
                            Debugs("CAMREA", "%s" % (str(data)), 0)
                        for pos in rgb:
                            if maxs % 100 == 0:
                                Debugs("CAMREA", "%1s [ R   G   B ]" % ('R' if numb == 2 else 'B' if numb == 0 else 'G'), 0)
                                Debugs("CAMREA", "%1d [%3d %3d %3d]" % (numb,pos[2],pos[1],pos[1]), 0)
                            if int(pos[2 - numb]) - int(pos[(2 - numb + 1) % 3]) < int(define_wbr_target):
                                if maxs % 100 == 0:
                                    Debugs("CAMREA", "互补颜色不符合!", 1)
                                frgb = False
                                data[numb] = data[numb] + int(define_wbr_setadd) if data[numb] < 253 else 255
                                data[(numb + 1) % 3] = data[(numb + 1) % 3]-int(define_wbr_setadd) if data[(numb + 1) % 3] > int(define_wbr_setadd) else 0
                                Cameras.gain(in_data=data)
                                time.sleep(0.001)
                            if int(pos[2 - numb]) - int(pos[(2 - numb + 2) % 3]) < int(define_wbr_target):
                                if maxs % 100 == 0:
                                    Debugs("CAMREA", "相邻颜色不符合!", 1)
                                frgb = False
                                data[numb] = data[2 - numb] + int(define_wbr_setadd) if data[numb] < 253 else 255
                                data[(numb + 2) % 3] = data[(numb + 2) % 3] - int(define_wbr_setadd) if data[(numb + 2) % 3] > int(define_wbr_setadd) else 0
                                Cameras.gain(in_data=data)
                                time.sleep(0.001)
                            numb += 1
                        ends = True if frgb else ends
                        if ends:
                            Debugs("CAMREA", "满足条件，结束", 4)
                            camera_data("module/ModuleConfig.py", "camera_color_data",
                                        in_data="[%3d,%4d,%4d]" % (data[2], data[1], data[0]),in_text="RGB",in_nums=2)
                            loop = False
                            flag = False
                            cv2.destroyAllWindows()
                            Cameras.exit()
                            return 0
                        tmp = camera_wrgb(tmp)
                        tmp = camera_draw(tmp, str(camera_show_pfps), flag)
                    else:
                        Debugs("CAMREA", "类型选择不正确!", 0)
                        Cameras.exit()
                        return -1
                    tmp = cv2.putText(tmp, "Hold On",
                                      (round(camera_resol_widt / 2) - 70, round(camera_resol_high / 2) + 150),
                                      cv2.FONT_HERSHEY_COMPLEX, 1.0,
                                      (255, 255, 255), 2)
                    cv2.imshow("Optical Calibration", tmp)
                    cv2.waitKey(1)
                    maxs = maxs + 1
                else:
                    if in_type == "wrgb":
                        tmp = cv2.putText(tmp, "Put the RGB LED in the Box",
                                          (round(camera_resol_widt / 2) - 260, round(camera_resol_high / 2) + 150),
                                          cv2.FONT_HERSHEY_COMPLEX, 1.0,
                                          (255, 255, 255), 2)
                        tmp = camera_wrgb(tmp)
                    else:
                        tmp = camera_gain(tmp,i)
                    tmp = cv2.putText(tmp, "Press a to Continue",
                                      (round(camera_resol_widt / 2) - 180, round(camera_resol_high / 2) + 180),
                                      cv2.FONT_HERSHEY_COMPLEX, 1.0,
                                      (0, 255, 255), 2)
                    tmp = camera_draw(tmp, str(camera_show_pfps), not flag)
                    cv2.imshow("Optical Calibration", tmp)
            if flag:
                flag = False
                loop = True
        nums += 2
    cv2.destroyAllWindows()
    Cameras.exit()
    return 0


# ----------------------------------------------------------------
if __name__ == '__main__':
    camera_main_input = ''
    while camera_main_input != 'q':
        cv2.destroyAllWindows()
        if len(camera_main_input) > 0:
            try:
                camera_main_input = int(camera_main_input)
                if camera_main_input == 0:
                    camera_show()
                elif camera_main_input == 1:
                    camera_conf("time")
                elif camera_main_input == 2:
                    camera_conf("gain")
                elif camera_main_input == 3:
                    camera_conf("wrgb")
                elif camera_main_input == 4:
                    pass
                else:
                    print("\n-------------输入选项不正确，请重新输入-------------")
                    time.sleep(2)
            except ValueError:
                print("\n-------------输入内容不正确，请重新输入-------------")
                time.sleep(2)
        camera_menu()
        camera_main_input = input("\n请输入你的选项: ")

