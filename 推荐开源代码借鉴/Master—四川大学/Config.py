#  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
#
#                     RoboMaster Vision Core Program
#                        机甲大师对抗赛视觉组核心程序
#                                配置文件
#
#                             Code by Pikachu
#                        Last Update： MAY25/2021
#
#  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# 此配置文件【谨慎修改】，如果要修改请务必查看参考修改教程，以免出错：
# https://scurm.coding.net/s/b2b521bf-b138-4054-bfd2-a62f487049a3/62
import module.ModuleConfig as extern

# 机器人的编号-------------------------------------------------------
master_nums = {
    'recv': {
        '雷达':  0x00,
        '飞机':  0x01,
        '哨兵':  0x02,
        '工程':  0x04,
        '英雄':  0x08,
        '步兵1': 0x10,
        '步兵2': 0x20,
        '步兵3': 0x40,
        'py3pc': 0x80,
        'stm32': 0x00,
    },
    'send': {
        '雷达':  0x00,
        '飞机':  0x07,
        '哨兵':  0x06,
        '工程':  0x05,
        '英雄':  0x04,
        '步兵1': 0x03,
        '步兵2': 0x02,
        '步兵3': 0x01,
        'py3pc': 0x08,
        'stm32': 0x00,
    },
    'type': {
        'UnicastTo': 0x00,
        'Multicast': 0x40,
        'Broadcast': 0x80
    },
    'flag': {
        'STM32-Only': 0x00,
        'MiniPCOnly': 0x10,
        'AllDecvies': 0x20
    }
}

# 并发配置选项-------------------------------------
# 优先级：threads > MPQueue > ShareMemory > ImgLock
# 不使用多进程的时候，无法使用图像队列/分布式图像锁
# 使用队列的时候，无法使用分布式图像锁， 只能用列表
use_threads = False              # 否-进程，是-线程
# 如果出现多进程无法使用CUDA的情况， 请开启下列选项
use_MPSpawn = True               # 是否用:线程spawn
# 是否使用MP多进程队列管理， 读写稳定平滑，但速度慢
use_MPQueue = False              # 使用MP的队列模块
# 或者用分离式数据锁，速度快,两个都不用是PY默认列表
use_ImgLock = True               # 使用分离式图片锁
# 在分离式锁操作的过程中也使用进程锁， 确保绝对安全
Img_SafeMod = False              # 是否使用安全模式
# 关闭读取加锁，有可能会导致I/O错误,但会提高I/O速度
Img_ReadMod = False              # 图像读取是否加锁
# 最新还是最旧图片，最旧的保证帧流畅 最新保证延迟低
Img_NewImgs = True               # T-取最新/ F-最旧
# 使用共享内存，需要Python版本>=3.8，需要使用View锁
ShareMemory = True               # 使用共享内存模块

# 核心参数配置-------------------------------------
master_self = '步兵1'            # 当前机器人的名称
master_sync = False              # 是否启用垂直同步
master_wait = 0.01               # 主线延时时间(秒)
master_jump = True               # 跳过获取颜色信息
master_dvce = 'minipc'           # 类型： nx/minipc
retrys_flag = True               # 进程掉线自动重启
retrys_maxs = 10                 # 最大自动重启次数
# 如果设置为nx，需要按照下方教程下载并安装模块-----
# 教程：https://github.com/TracelessLe/shared_numpy
timeout_dog = 1000                 # 多久没喂狗重启
excode_text = ["程序正常退出!!!", #程序正常退出!!-0
               "子线程异常退出!", #子线程异常退出-1
               "子线程喂狗超时!", #子线程喂狗超时-2
               "相机周期掉帧!!!", #相机周期上限!!-3
               "相机总共掉帧!!!", #相机总错误上限-4
               "相机连续掉帧!!!", #相机连续上限!!-5
               "找不到指定相机!", #找不到指定相机-6
               "相机类型不支持!", #相机类型不支持-7
               "串口无法打开!!!", #串口无法打开!!-8
]
# 串口参数设置-------------------------------------
serial_flag = True               # 串口全局开关设置
serial_port = '/dev/ttyUSB0'     # 串口物理端口配置
#serial_port = 'COM3'             # 串口物理端口配置
serial_bbps = 115200             # 串口比特率的设置
serial_wait = 0                  # 串口延时时间(秒)
serial_show = False              # 显示串口详细信息
serial_dels = False              # 自动删除过期数据
serial_uttl = True               # 用TTL,否则直接删
serial_dttl = -1                 # 串口强制TTL-数值
# 可选配置， 串口有改动才发送还是总是发送现有的数据
onedit_flag = True               # 串口修改发送标识
# 相机配置参数-------------------------------------
camera_flag = True    # 相机线程全局启用:  开关设置
camera_maxp = 10      # 最大缓存图像， 超过自动删除
camera_wait = 0       # 相机延时时间(秒)，0表示禁止
camera_type = extern.camera_types_text   # 相机类型
endure_flag = True    # 启用:最大相机容忍掉帧限制值
endure_type = False   # T-周期内达到才停,F-达到就停
endure_maxp = 3       # 相机最大容忍错误掉帧数-阈值
endure_time = 0.1     # 相机最大容忍错误掉帧数-周期
endure_line = 3       # 连续遇到多少帧图像错误-停止
rgb_filters = True    # 自动根据当前B/R自动执行滤波
# 一旦置为True， 则需要指定TYPE类型是否为打大符模式
# 识别参数设置-------------------------------------
armors_wait = 0       # 识别延时时间(秒)，0表示禁止
armors_flag = False   # 无法获取图像的时候:输出警告
svofilepath = None    # SVO路径，None表示关闭此功能
# 此处填写:装甲板识别额外参数 ---------------------
armors_info = {"track_length": 382.3,        # 厘米
               "t_range": [10., 381.],       # 厘米
               "yaw_range": [-30., 30.],     # 角度
               "pitch_range": [-50., 10.],   # 角度
               "off_x": 6,                   # 厘米
               "off_y": 7,                   # 厘米
               }
# 设备调试设置-------------------------------------
debug_imgs = False                   # 相机图像输出
debug_aimg = False                   # 识别图像输出
empty_warn = False                   # 空图像的警告
debug_tnum = False                   # 输出线程情况
debug_tfps = True                    # 输出帧率情况
debug_bimg = True                    # 输出缓存图像
debug_save = False                   # 保存录制视频
debug_lost = True                    # 掉帧警告输出
video_sfps = 30                      # 视频录制帧率
video_time = 30                      # 保存时间间隔
video_auto = True                    # 自动修改帧率
# 自定义参数---------------------------------------
# 你可以在此处增加自己的参数，在线程内用in_conf调用
""" 举个例子
    Option = {"var1":"dat1",
              "var2":"dat2",
              "var3":"dat3",
              "var4":"dat4"}
则在你的线程内部就可以通过:
       in_conf["Option"]["var1"]来读取var1参数
       in_conf["Option"]["var2"]来读取var2参数
**注意：Option是只读的，多进程中需要修改请用Record
"""  # --------------------------------------------
Option = {
    "model_dir": './inference_model/ppyolo_tiny',
    "use_gpu": 1,
    "run_mode": 'trt_fp16',
    "threshold": 0.37,
}
# 串口的参数---------------------------------------
# 在此添加要通过串口模块发送或者接收的变量数据定义
# 用法：串口变量名：[传输类型，变量类型，绑定数据]
# 直接访问是只读的，如果要修改数据必须复制Serials
# 其中：DAT1是监听变量名，在Record里面进行记录修改
# 最后的Bool表示是否开启，False-禁用则下次不会发送
# ------------------------------------------------
Serial = {
    "LOCK": False,
    "VAR1": ["P", "I", "DAT1", True],
    "VAR2": ["P", "I", "DAT2", True],
    "TEST": ["P", "I", "TEST", False],
}
# 数据的参数---------------------------------------
# 可变数据的记录，和Option不同，这里的数据可以修改
# 通过in_conf["Record"]["var1"]['d']来读取var1变量
# 直接访问是只读的，如果要修改数据必须要Shared模块
# l-同步锁定，特殊情况需要锁定此变量以免被错误更改
# c-更改标识，True表示这个变量已经被更新了需要同步
# ------------------------------------------------
Record = {
    "LOCK": False,
    # 大符模式 False-否，True-是------------------
    "TYPE": {
        "d": False,
        "l": False,
        "c": True
    },
    # 测试数据，可以删除--------------------------
    "DAT1": {
        "d": 0,
        "l": False,
        "c": True
    },
    "DAT2": {
        "d": 0,
        "l": False,
        "c": True
    },
    "TEST": {
            "d": 0,
            "l": False,
            "c": True
    },
}
# --------------------+----------------------------
# Receive是接收是变量，请勿写入，访问方式同上-----
# 直接访问是只读的，如果要修改数据必须要Shared模块
Receive = {
    "LOCK": False,
    # 如果master_jump == True，则需要手动填写颜色
    "COLO": {
        "d": "R",
        "l": False,
        "c": True,
        "t": -1
    }
}
# ComInfo是串口路由信息，请勿填写，访问方式同上---
# 直接访问是只读的，如果要修改数据必须要Shared模块
ComInfo = {

}
# 内参请勿修改-------------------------------------
master_send = master_nums['send'][master_self] | \
              master_nums['send']['py3pc']
master_recv = master_nums['recv'][master_self] | \
              master_nums['recv']['stm32']
# -------------------------------------------------
