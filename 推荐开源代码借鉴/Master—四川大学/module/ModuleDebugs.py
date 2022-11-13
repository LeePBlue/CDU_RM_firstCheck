# ----------------------------------------------
#           SCURM_Vision_Module_Debugs
#               Coding By Pikachu
#                  调试信息输出
#
#            LAST_UPDATE:OCT30/2020
# ----------------------------------------------
import time
from module import ModuleConfig as config

# ----------------------------------------------------------------------------------------------------------------------
debug_dat = ['INFOS', 'WARNS', 'ERROR', 'PANIC', 'SUCCS']
global debug_lock
debug_lock = False


# ----------------------------------------------------------------------------------------------------------------------
def Debugs(in_heads="UNKONWS",             # 调试输出标题
           in_texts="---------------",     # 调试输出内容
           in_level=0,                     # 调试信息等级
           in_lines="\n",                  # 调试输出结尾
           in_datas=None,
           in_write=True):
    global debug_lock
    while not config.disable_logs_sync and debug_lock:
        time.sleep(0.001)
    debug_lock = True
    if config.global_debug_flag:
        debug_log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if in_datas is None:
            debug_log_text = ""
            debug_log_text = debug_log_text + "[" + debug_log_time + "]"
            debug_log_text = debug_log_text + "[" + debug_dat[in_level % 5] + "]"
            debug_log_text = debug_log_text + "[" + in_heads.ljust(6, '-') + "]"
            debug_log_text = debug_log_text + " " + in_texts
        else:
            debug_log_text = in_datas
        print(debug_log_text, end=in_lines)
        if config.debugs_write_flag and in_write:
            with open(config.debugs_write_file, 'a') as file:
                try:
                    file.write(debug_log_text + "\n")
                except UnicodeError or BaseException:
                    Debugs("DEBUGS", "ERROR OUTPUT", 2)
        debug_lock = False
        return True
    debug_lock = False
    return False
