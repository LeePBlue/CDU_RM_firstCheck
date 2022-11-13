# ----------------------------------------------
#           SCURM_Vision_Global_Config
#               Coding By Pikachu
#                  全局配置信息
#
#            LAST_UPDATE:MAY25/2021
# ----------------------------------------------
global_debug_flag = True   # 全局调试输出
# Camera模块配置项-----------------------
camera_resol_high = 1024   # 设定图像高度
camera_resol_widt = 1280   # 设定图像宽度
camera_resol_sfps = 100    # 设定曝光帧率
camera_types_text = "MV"   # 相机类型设定
# 若是Linux，BR输出需要反向，应设置为True
camera_resol_tbgr = False  # 反转B和R通道
# 仅作用于MV 摄像头----------------------
camera_exposure_t =  9999  # 相机曝光时间
camera_wbmod_auto = True   # 硬自动白平衡
camera_wbmod_info = 0      # 硬白平衡色温
camera_color_sets = True   # 静态色温增益
camera_color_data = [255, 255, 255] # RGB
# 预设颜色增益参数-----------------------
camera_gain_color = {
    "R": [100, 100, 100],
    "G": [100, 100, 100],
    "B": [100, 100, 100],
}
# ---------------------------------------
serial_debug_flag = True   # 串口调试输出
serial_debug_data = False  # 输出串口内容
serial_verify_md5 = False  # 验证-MD5数据
serial_comst_head = [255, 255]   # 分隔符
# Shared模块配置-------------------------
shared_debug_flag = True   # 输出失败信息
shared_detail_inf = True   # 输出警告信息
shared_openmaxtry = 10     # 解锁最大次数
# Debugs模块配置-------------------------
debugs_write_flag = False  # 调试写入文件
debugs_write_file = 'scurm.txt'
disable_logs_sync = True   # 关闭输出同步
# 相机校准配置---------------------------
define_set_colors = ['R','B']  # 校准颜色
color_l = {'R': "  Red", 'B': " Blue"}
define_all_maxtry = 2000   # 最大迭代次数
define_iso_target = 0xe0   # 目标颜色阈值
define_iso_others = 0x90   # 其他颜色阈值
define_iso_setadd = 5      # 单次迭代增幅
define_rgb_target = 0xfa   # 目标颜色阈值
define_rgb_others = 0x20   # 其他颜色阈值
define_rgb_setadd = 2      # 单次迭代增幅
define_wbr_target = 150    # 白平衡色差距
define_wbr_setadd = 2      # 单次迭代增幅
# ---------------------------------------

