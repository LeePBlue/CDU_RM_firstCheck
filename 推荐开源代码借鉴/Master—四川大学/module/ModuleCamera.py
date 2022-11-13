# ---------------------------------------------------------------
#                   SCURM_Vision_Module_Camera
#                       Coding By Pikachu
#                          摄像头API
#
#                     LAST_UPDATE:JUL21/2021
# ----------------------------------------------------------------
from module import ModuleConfig as config
from module import ModuleMvsdks as mvsdks, ModuleDebugs as debugs

# ZED相机自动import模块---------------
if config.camera_types_text == "ZED":
    import pyzed.sl as sl
    from utils import *

import cv2
import time
import platform
import numpy as np

debug_head = "Camera"


# ----------------------------------------------------------------------------------------------------------------------
class Camera:
    @staticmethod
    # ------------------------------------------------------------------------------------------------------------------
    #                                         列出当前设备下的所有相机
    #                           输入：in_flags:True-输出具体相机 False-不输出内容
    #                           输出： [当前设备相机数量，当前设备相机型号与编号]
    # ------------------------------------------------------------------------------------------------------------------
    def list(in_flag=True):
        if config.camera_types_text == "MV":
            camera_list_devList = mvsdks.CameraEnumerateDevice()
            camera_list_devNums = len(camera_list_devList)
            if camera_list_devNums > 0:
                debugs.Debugs(debug_head, "连接相机数量: " + str(camera_list_devNums))
            else:
                debugs.Debugs(debug_head, "没有摄像机信息!", in_level=3)
                return 0
            for i, ModuleCamera_DevInfo in enumerate(camera_list_devList):
                if in_flag:
                    debugs.Debugs(debug_head, "{}-{} {}".format(i,
                                                                ModuleCamera_DevInfo.GetPortType(),
                                                                ModuleCamera_DevInfo.GetFriendlyName()[:7], ))
                    debugs.Debugs(debug_head, "{}{}".format(ModuleCamera_DevInfo.GetFriendlyName()[10:-4],
                                                            ModuleCamera_DevInfo.GetFriendlyName()[27:]))
            return camera_list_devNums, camera_list_devList
        else:
            debugs.Debugs(debug_head, "相机类型不支持!", in_level=1)
            return None

    @staticmethod
    # ------------------------------------------------------------------------------------------------------------------
    #                                         列出当前相机的具体参数
    #                                           输入：相机实体对象
    #                                           输出：命令行的信息
    # ------------------------------------------------------------------------------------------------------------------
    def PrintCapbility(in_caps):
        for i in range(in_caps.iTriggerDesc):
            desc = in_caps.pTriggerDesc[i]
            debugs.Debugs(debug_head, "拍摄方式：{} - {}".format(desc.iIndex, desc.GetDescription()))
        for i in range(in_caps.iImageSizeDesc):
            desc = in_caps.pImageSizeDesc[i]
            debugs.Debugs(debug_head, "输出大小：{} - {}".format(desc.iIndex, desc.GetDescription()))
        for i in range(in_caps.iClrTempDesc):
            desc = in_caps.pClrTempDesc[i]
            debugs.Debugs(debug_head, "捕获色温：{} - {}".format(desc.iIndex, desc.GetDescription()))
        for i in range(in_caps.iMediaTypeDesc):
            desc = in_caps.pMediaTypeDesc[i]
            debugs.Debugs(debug_head, "输出位深：{} - {}".format(desc.iIndex, desc.GetDescription()))
        for i in range(in_caps.iFrameSpeedDesc):
            desc = in_caps.pFrameSpeedDesc[i]
            debugs.Debugs(debug_head, "快门速度：{} - {}".format(desc.iIndex, desc.GetDescription()))
        for i in range(in_caps.iPackLenDesc):
            desc = in_caps.pPackLenDesc[i]
            debugs.Debugs(debug_head, "传输包长：{} - {}".format(desc.iIndex, desc.GetDescription()))
        for i in range(in_caps.iPresetLut):
            desc = in_caps.pPresetLutDesc[i]
            debugs.Debugs(debug_head, "捕获方法：{} - {}".format(desc.iIndex, desc.GetDescription()))
        for i in range(in_caps.iAeAlmSwDesc):
            desc = in_caps.pAeAlmSwDesc[i]
            debugs.Debugs(debug_head, "曝光算法：{} - {}".format(desc.iIndex, desc.GetDescription()))
        for i in range(in_caps.iAeAlmHdDesc):
            desc = in_caps.pAeAlmHdDesc[i]
            debugs.Debugs(debug_head, "转换个数：{} - {}".format(desc.iIndex, desc.GetDescription()))
        for i in range(in_caps.iBayerDecAlmSwDesc):
            desc = in_caps.pBayerDecAlmSwDesc[i]
            debugs.Debugs(debug_head, "预设滤镜：{} - {}".format(desc.iIndex, desc.GetDescription()))
        for i in range(in_caps.iBayerDecAlmHdDesc):
            desc = in_caps.pBayerDecAlmHdDesc[i]
            debugs.Debugs(debug_head, "输出质量：{} - {}".format(desc.iIndex, desc.GetDescription()))

    # ------------------------------------------------------------------------------------------------------------------
    #                                             初始化相机模块
    #                   输入：in_nums(相机ID) in_type(相机类型MV/ZED/DH)，in_svofilepath(ZED专用:SVO路径)
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, in_nums=0, in_type='MV', in_flag=False, in_svofilepath=None):
        self.type = in_type
        if in_type == 'MV':
            try:
                camera_init_nums, camera_init_list = Camera.list(in_flag)
                if in_nums <= camera_init_nums - 1:
                    try:
                        # 初始化相机的设备------------------------------------------------
                        self.camera = mvsdks.CameraInit(camera_init_list[in_nums], -1, -1)
                        # 获取相机特性描述------------------------------------------------
                        camera_init_caps = mvsdks.CameraGetCapability(self.camera)
                        if in_flag:
                            Camera.PrintCapbility(camera_init_caps)
                        # 判断黑白彩色相机-------------------------------------------------
                        camera_init_mono = (camera_init_caps.sIspCapacity.bMonoSensor != 0)
                        # 黑白相机让ISP直接输出MONO数据，而不是扩展成R=G=B的24位灰度-----------------
                        if camera_init_mono:
                            mvsdks.CameraSetIspOutFormat(self.camera, mvsdks.CAMERA_MEDIA_TYPE_MONO8)
                        # 模式切换连续采集-----------------------------------------------------------
                        mvsdks.CameraSetTriggerMode(self.camera, 0)
                        # 设置固定增益---------------------------------------------------------------
                        if config.camera_color_sets:
                            mvsdks.CameraSetGain(self.camera,
                                                 config.camera_color_data[0],
                                                 config.camera_color_data[1],
                                                 config.camera_color_data[2])
                        # 手动设置曝光时间--------------------------------------------------------------------
                        mvsdks.CameraSetAeState(self.camera, False)
                        mvsdks.CameraSetExposureTime(self.camera, config.camera_exposure_t)
                        mvsdks.CameraSetWbMode(self.camera, config.camera_wbmod_auto)
                        # 让SDK内部取图线程开始工作-----------------------------------------------------------
                        mvsdks.CameraPlay(self.camera)
                        # 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
                        camera_init_size = camera_init_caps.sResolutionRange.iWidthMax * \
                                           camera_init_caps.sResolutionRange.iHeightMax * (
                                               1 if camera_init_mono else 3)
                        # 分配RGB buffer，用来存放ISP输出的图像
                        # 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据
                        # 如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer
                        self.buffer = mvsdks.CameraAlignMalloc(camera_init_size, 16)
                    except mvsdks.CameraException as e:
                        debugs.Debugs(debug_head, "CameraInit Fail", in_level=2)
                        debugs.Debugs(debug_head, "API错误代码:{}".format(e.error_code), in_level=2)
                        if e.error_code == -45:
                            print(mvsdks.CameraGetErrorString(e.error_code)[7:-1].replace("的","").replace("，",""))
                        else:
                            debugs.Debugs(debug_head, e.message[:8])
                        exit(6)
                else:
                    debugs.Debugs(debug_head, "相机编号不正确!", in_level=2)
            except TypeError:
                debugs.Debugs(debug_head, "找不到相机设备!", 3)
                exit(6)
        elif in_type == 'ZED':
            # ZED摄像机 -----------------------------------------------------
            self.Cameras = sl.Camera()
            input_type = sl.InputType()
            # 载入预设数据---------------------------------------------------
            if in_svofilepath is not None:
                input_type.set_from_svo_file(in_svofilepath)
            # 初始化参数-----------------------------------------------------
            init_params = sl.InitParameters(input_t=input_type)
            init_params.camera_resolution = sl.RESOLUTION.HD720
            init_params.camera_fps = 100
            init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
            init_params.coordinate_units = sl.UNIT.METER
            init_params.svo_real_time_mode = False
            init_errors = self.Cameras.open(init_params)
            debugs.Debugs(debug_head, init_errors, 4)
            # 等待相机开启----------------------------------------------------
            while init_errors != sl.ERROR_CODE.SUCCESS:
                init_errors = self.Cameras.open(init_params)
                debugs.Debugs(debug_head, init_errors, 2)
                time.sleep(1)
            # 尝试获取数据----------------------------------------------------
            self.image_mats = sl.Mat()
            self.depth_mats = sl.Mat()
            # 配置相机参数----------------------------------------------------
            self.RunTime = sl.RuntimeParameters()
            self.ImgSize = self.Cameras.get_camera_information().camera_resolution
            self.ImgSize.width = self.ImgSize.width / 2
            self.ImgSize.height = self.ImgSize.height / 2
            self.ImgSize = sl.Resolution(self.ImgSize.width, self.ImgSize.height)
        else:
            debugs.Debugs(debug_head, "相机类型设定有误！", 3)
            exit(7)

    # 获取一张图像
    def shot(self, widt=1280, high=1024):
        if self.type == "MV":
            # ----------------------------------------------------------------------------------------------------------
            try:
                if self.camera is None:
                    return None
                camera_geti_pRawDatas, camera_geti_FrameHead = mvsdks.CameraGetImageBuffer(self.camera, 2000)
                mvsdks.CameraImageProcess(self.camera, camera_geti_pRawDatas, self.buffer, camera_geti_FrameHead)
                mvsdks.CameraReleaseImageBuffer(self.camera, camera_geti_pRawDatas)
                camera_getf_buff = self.buffer
                camera_getf_head = camera_geti_FrameHead
                if platform.system() == "Windows":
                    mvsdks.CameraFlipFrameBuffer(camera_getf_buff, camera_getf_head, 1)
                # 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
                # 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
                camera_getf_data = (mvsdks.c_ubyte * camera_getf_head.uBytes).from_address(camera_getf_buff)
                camera_getf_oupt = np.frombuffer(camera_getf_data, dtype=np.uint8)
                camera_getf_oupt = camera_getf_oupt.reshape(
                    (camera_getf_head.iHeight, camera_getf_head.iWidth,
                     1 if camera_getf_head.uiMediaType == mvsdks.CAMERA_MEDIA_TYPE_MONO8 else 3))
                if config.camera_resol_tbgr:
                    camera_getf_oupt = camera_getf_oupt[..., ::-1]
                camera_getf_oupt = cv2.resize(camera_getf_oupt,
                                              (config.camera_resol_widt, config.camera_resol_high),
                                              interpolation=cv2.INTER_LINEAR)
                return camera_getf_oupt
            except mvsdks.CameraException as e:
                debugs.Debugs(debug_head, "API报告错误:{}".format(e.error_code))
                debugs.Debugs(debug_head, "{}".format(e.message))

            except TypeError:
                debugs.Debugs(debug_head, "相机获取帧错误!", 2)
                return None
            except UnboundLocalError:
                debugs.Debugs(debug_head, "相机获取帧错误!", 2)
                return None
            except AttributeError:
                debugs.Debugs(debug_head, "相机接口有异常!", 2)
                return None
        elif self.type == "ZED":
            if self.Cameras.grab(self.RunTime) == sl.ERROR_CODE.SUCCESS:
                self.Cameras.retrieve_image(self.image_mats, sl.VIEW.LEFT, resolution=self.ImgSize)
                self.Cameras.retrieve_measure(self.depth_mats, sl.MEASURE.XYZRGBA, resolution=self.ImgSize)
                camrea_tmpimg = [load_image_into_numpy_array(self.image_mats),
                                 load_depth_into_numpy_array(self.depth_mats)]
                return camrea_tmpimg
            else:
                return None
        else:
            return None

    def save(self, in_buff="", in_head="",
             in_path="./save_picture_" + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + ".bmp"):
        if self.type == "MV":
            if in_buff == "" or in_head == "":
                camera_geti_pRawDatas, camera_geti_FrameHead = mvsdks.CameraGetImageBuffer(self.camera, 2000)
                mvsdks.CameraImageProcess(self.camera, camera_geti_pRawDatas, self.buffer, camera_geti_FrameHead)
                mvsdks.CameraReleaseImageBuffer(self.camera, camera_geti_pRawDatas)
                camera_save_buff = self.buffer
                camera_save_head = camera_geti_FrameHead
            else:
                camera_save_buff = in_buff
                camera_save_head = in_head
            # 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
            status = mvsdks.CameraSaveImage(self.camera, in_path,
                                            camera_save_buff,
                                            camera_save_head,
                                            mvsdks.FILE_BMP,
                                            100)
            if status == mvsdks.CAMERA_STATUS_SUCCESS:
                debugs.Debugs(debug_head, "Save image successfully")
                debugs.Debugs(debug_head, "image_size = {}X{}".format(camera_save_head.iWidth,
                                                                      camera_save_head.iHeight))
                return True
            else:
                debugs.Debugs(debug_head, "Save image failed. err={}".format(status))
                return False
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    #                                           获取/设置色彩增益
    # 输入：（获取当前增益值）None None    /  （直接设置增益）[R, G, B]   /  （按照颜色设置）String "R" / "G" / "B"
    # 输出：  [int-R,   int-B,   int-G]    /    boolean: True  /  False   /   boolean: True  /  False / [R,  G,  B]
    # ------------------------------------------------------------------------------------------------------------------
    def gain(self, in_text=None, in_data=None):
        if in_data is None and in_text is None:
            return mvsdks.CameraGetGain(self.camera)
        if in_data is None:
            in_data = [100, 100, 100]
        if self.type == "MV":
            try:
                if in_text is None:
                    mvsdks.CameraSetGain(self.camera, in_data[0], in_data[1], in_data[2])
                elif in_text in config.camera_gain_color:
                    mvsdks.CameraSetGain(self.camera,
                                         config.camera_gain_color[in_text][0],
                                         config.camera_gain_color[in_text][1],
                                         config.camera_gain_color[in_text][2])
                    return config.camera_gain_color[in_text]
            except AttributeError:
                debugs.Debugs(debug_head, "相机接口有异常!", 2)
                return False
            else:
                return False
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    #                                           获取/设置曝光时间
    #                           输入：None-获取曝光时间 / Data-设置曝光时间
    #                           输出：当前曝光时间(None)/ TrueFalse设置结果
    # ------------------------------------------------------------------------------------------------------------------
    def time(self, in_data=None):
        if self.type == "MV":
            if in_data is None:
                return mvsdks.CameraGetExposureTime(self.camera)
            else:
                mvsdks.CameraSetExposureTime(self.camera, in_data)
                return True
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    #                                             关闭相机
    # ------------------------------------------------------------------------------------------------------------------
    def exit(self):
        try:
            return mvsdks.CameraUnInit(self.camera)
        except AttributeError:
            debugs.Debugs(debug_head, "相机接口有异常!", 2)
            return False
