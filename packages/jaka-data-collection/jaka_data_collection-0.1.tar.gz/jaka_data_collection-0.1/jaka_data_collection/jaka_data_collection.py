import multiprocessing as mp  # 导入多进程模块
from multiprocessing import Process  # 导入进程类
from sys import stderr
import time  # 导入时间模块
from pathlib import Path  # 导入路径模块
from warnings import warn  # 导入警告模块
import pyrealsense2 as rs  # 导入RealSense模块skse
import cv2  # 导入OpenCV模块
import numpy as np  # 导入NumPy模块
from tqdm import tqdm  # 导入进度条模块
import keyboard
import os
from multiprocessing import Pool


class Data_Collection:
    """ 
    数据采集类, 用于控制JAKA机械臂进行采集数据, 保存数据

    Attributes:
        CAMERA_DEVICE_NUM: 摄像头设备数量
        VIDEO_NUM: 视频数量
        MAX_FRAMES: 最大帧数
        HEIGHT: 图像高度
        WIDTH: 图像宽度
        CHANNELS: 图像通道数
        TASK_PATH: 任务路径
        TASK_NAME: 任务名称
        REALSENSE_COLOR_INDEX: realsense color 在RGB共享内存数组中的索引
        REALSENSE_DEPTH_INDEX: realsense depth 在深度共享内存数组中的索引
        WRIST_COLOR_INDEX: wrist color 在RGB共享内存数组中的索引
        CHEST_COLOR_NAME: chest color 名称
        WRIST_COLOR_NAME: wrist color 名称
        CHEST_DEPTH_NAME: chest depth 名称
        VIDEO_NAMES: 视频名称列表
    """
    def __init__(self, CAMERA_DEVICE_NUM = 2, VIDEO_NUM = 3, MAX_FRAMES = 1000, HEIGHT = 480, WIDTH = 640, CHANNELS = 3, 
                 TASK_PATH = "E:\\jaka_data", TASK_NAME = "task_77", REALSENSE_COLOR_INDEX = 1, REALSENSE_DEPTH_INDEX = 0, 
                 WRIST_COLOR_INDEX = 0, CHEST_COLOR_NAME = 'chest_color', WRIST_COLOR_NAME = 'wrist_down_color', CHEST_DEPTH_NAME = 'chest_depth') -> None:
        self.CAMERA_DEVICE_NUM = CAMERA_DEVICE_NUM
        self.VIDEO_NUM = VIDEO_NUM
        self.MAX_FRAMES = MAX_FRAMES
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.CHANNELS = CHANNELS
        self.TASK_PATH = TASK_PATH
        self.TASK_NAME = TASK_NAME
        self.REALSENSE_COLOR_INDEX = REALSENSE_COLOR_INDEX
        self.REALSENSE_DEPTH_INDEX = REALSENSE_DEPTH_INDEX
        self.WRIST_COLOR_INDEX = WRIST_COLOR_INDEX
        self.CHEST_COLOR_NAME = CHEST_COLOR_NAME
        self.WRIST_COLOR_NAME = WRIST_COLOR_NAME
        self.CHEST_DEPTH_NAME = CHEST_DEPTH_NAME
        self.VIDEO_NAMES = [CHEST_COLOR_NAME, WRIST_COLOR_NAME, CHEST_DEPTH_NAME]

        # assert VIDEO_NUM == CAMERA_DEVICE_NUM, "video name length must equal to CAMERA_DEVICE_NUM"s



    # def get_host_time():
    #     response = requests.get(HOST_URL)  # 发送GET请求获取主机时间
    #     result = response.json()  # 解析响应数据
    #     return result['timestamp']  # 返回时间戳


    # def signal_handler(sig, frame):
    #     global stop_capture
    #     stop_capture.value = 1


    def start_collection(self):
        """
        按键s控制开始采集数据
        """
        global start_collection_flag
        global fileio_flag

        if fileio_flag.value == 1:
            print("Writing buffer to disk now.")
            return

        start_collection_flag.value = 1
        end_collection_flag.value = 0
        kill_collection_flag.value = 0
        print('\033[91m' + "Start collection." + '\033[0m')


    def end_collection(self):
        """
        按键e控制结束采集数据，并输出已经采集的数据的数量
        """
        global end_collection_flag

        end_collection_flag.value = 1
        start_collection_flag.value = 0
        fileio_flag.value = 1
        folder_path = Path(f'{self.TASK_PATH}/data/{self.TASK_NAME}')
        folder_path.mkdir(exist_ok=True, parents=True)
        num_folders = len([name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))])+1
        print(f"End collection. {num_folders} collected.")

    def kill_collection(self):
        """
        按键k控制结束采集数据，并不保存任何数据
        """
        global kill_collection_flag

        end_collection_flag.value = 1
        kill_collection_flag.value = 1
        start_collection_flag.value = 0
        print("Kill collection.")

    def save_image(self, image, image_name, image_path):
        """
        在文件路径下保存图片

        Args:
            image: 图片
            image_name: 图片名称
            image_path: 图片路径
        """
        save_path = image_path / f'{image_name}.png'
        cv2.imwrite(save_path.as_posix(), image)

    def save_video(self, video, timestamp, video_length, episode_name, video_name):
        """
        在文件路径下保存视频，使用多进程来并行处理图片保存，并命名为时间戳

        Args:
            video: 要保存的视频
            timestamp: 时间戳
            video_length: 视频长度
            episode_name: 轨迹数量名称
            video_name: 视频名称
        """
        
        video_dir = Path(f'{self.TASK_PATH}/data/{self.TASK_NAME}/{episode_name}/{video_name}')
        video_dir.mkdir(exist_ok=True, parents=True)

        video_frame = video[:video_length]
        timestamp_frame = timestamp[:video_length]

        # 使用multiprocessing的Pool来并行处理图片保存
        num_processes = os.cpu_count()  # 获取可用CPU核心数
        with Pool(processes=num_processes) as pool:
            pool.starmap(self.save_image, [(video_frame[i], timestamp_frame[i], video_dir) for i in range(video_length)])
        print(f'{video_name} saved with {video_length} frames.')

    def save_episode(self, RGB_shared_frames, depth_shared_frames, shared_timestamps, frame_nums_share):
        """
        保存一条轨迹的数据
        
        Args:
            RGB_shared_frames: RGB图像共享内存
            depth_shared_frames: 深度图像共享内存
            shared_timestamps: 时间戳共享内存
            frame_nums_share: 每个相机已经采集的帧数共享内存
        """
        
        frame_nums = [i.value for i in frame_nums_share]
        print("frame_nums:", frame_nums)

        # 确定已经采集了多少条数据
        folder_path = Path(f'{self.TASK_PATH}/data/{self.TASK_NAME}')
        folder_path.mkdir(exist_ok=True, parents=True)
        num_folders = len([name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))])
        episode_name = f'{self.TASK_NAME}_{num_folders}'

        for video_name in self.VIDEO_NAMES:
            if video_name == self.CHEST_DEPTH_NAME:
                frames_np = np.frombuffer(depth_shared_frames[self.REALSENSE_DEPTH_INDEX].get_obj(), dtype=np.uint16).reshape((self.MAX_FRAMES, self.HEIGHT, self.WIDTH))
                timestamps_np = np.frombuffer(shared_timestamps[self.REALSENSE_COLOR_INDEX].get_obj(), dtype='int64').reshape((self.MAX_FRAMES,))
                frame_num = frame_nums[self.REALSENSE_COLOR_INDEX]
            elif video_name == self.CHEST_COLOR_NAME:
                frames_np = np.frombuffer(RGB_shared_frames[self.REALSENSE_COLOR_INDEX].get_obj(), dtype=np.uint8).reshape(
                    (self.MAX_FRAMES, self.HEIGHT, self.WIDTH, self.CHANNELS))
                timestamps_np = np.frombuffer(shared_timestamps[self.REALSENSE_COLOR_INDEX].get_obj(), dtype='int64').reshape((self.MAX_FRAMES,))
                frame_num = frame_nums[self.REALSENSE_COLOR_INDEX]
            elif video_name == self.WRIST_COLOR_NAME:
                frames_np = np.frombuffer(RGB_shared_frames[self.WRIST_COLOR_INDEX].get_obj(), dtype=np.uint8).reshape(
                    (self.MAX_FRAMES, self.HEIGHT, self.WIDTH, self.CHANNELS))
                timestamps_np = np.frombuffer(shared_timestamps[self.WRIST_COLOR_INDEX].get_obj(), dtype='int64').reshape((self.MAX_FRAMES,))
                frame_num = frame_nums[self.WRIST_COLOR_INDEX]
            else:
                stderr('VIDEO NAME ERROR!')
            
            self.save_video(video=frames_np, timestamp=timestamps_np, video_length=frame_num, episode_name=episode_name, video_name=video_name)
            


    def capture_frames(
            self, 
            video_index,
            RGB_shared_frames,
            timestamps,
            frame_num_return,
            CAMERA_DEVICE_NUM,
            start_capture,
            stop_capture,
            start_collection_flag,
            end_collection_flag
            ):
        """
        控制wrist_down摄像头捕获视频帧
        
        Args:
            video_index: wrist_down摄像头在共享内存数组中的索引
            RGB_shared_frames: RGB图像共享内存
            timestamps: 时间戳共享内存
            frame_num_return: 每个相机已经采集的帧数共享内存
            CAMERA_DEVICE_NUM: 相机数量
            start_capture: 开始捕获计数标志
            stop_capture: 停止捕获标志
            start_collection_flag: 开始采集标志
            end_collection_flag: 结束采集标志
        """
        cap = cv2.VideoCapture(video_index)
        cap.set(cv2.CAP_PROP_FRAME_self.WIDTH, self.WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_self.HEIGHT, self.HEIGHT)

        frame_exists, frame = cap.read()  # 读取视频帧
        start_capture.value += 1  # 增加开始捕获计数
        while start_capture.value < self.CAMERA_DEVICE_NUM:  # 等待所有视频开始捕获
            pass

        frame_num = 0  # 帧计数器
        while not stop_capture.value:  # stop capture值变为1时，停止该摄像头的记录
            while not start_collection_flag.value:
                frame_num = 0
            while frame_num < self.MAX_FRAMES and not end_collection_flag.value:
                # st = time.time()  # 记录开始时间
                frame_exists, frame = cap.read()  # 读取视频帧

                if not frame_exists:
                    warn(f"Video {video_index} failed to capture.")  # 发出警告，视频捕获失败
                    continue

                # 记录时间戳
                time_nanosec = time.time_ns()  # 获取当前时间的纳秒级时间戳
                timestamps_np = np.frombuffer(timestamps.get_obj(), dtype='int64').reshape((self.MAX_FRAMES,))
                timestamps_np[frame_num] = time_nanosec

                if frame_num == 0:
                    print("Video Captured.")  # 打印视频已捕获

                # 将帧保存到共享内存缓冲区
                RGB_shared_frames_np = np.frombuffer(RGB_shared_frames.get_obj(), dtype=np.uint8).reshape(
                    (self.MAX_FRAMES, self.HEIGHT, self.WIDTH, self.CHANNELS))
                RGB_shared_frames_np[frame_num] = frame  # 记录捕获的帧
                frame_num += 1  # 更新帧计数器
                frame_num_return.value = frame_num  # 记录已捕获帧的数量

                # time.sleep(max(0, TIME_INTERVAL - (time.time() - st)))  # 控制帧捕获间隔

        cap.release()  # 释放视频捕获设备


    def capture_realsense(
            self, 
            RGB_shared_frames,
            timestamps,
            frame_num_return,
            depth_shared_frames,
            CAMERA_DEVICE_NUM,
            start_capture,
            stop_capture,
            start_collection_flag,
            end_collection_flag
            ):
        """
        控制realsense摄像头捕获视频帧

        Args:
            RGB_shared_frames: RGB图像共享内存
            timestamps: 时间戳共享内存
            frame_num_return: 每个相机已经采集的帧数共享内存
            depth_shared_frames: 深度图像共享内存
            CAMERA_DEVICE_NUM: 相机数量
            start_capture: 开始捕获计数标志
            stop_capture: 停止捕获标志
            start_collection_flag: 开始采集标志
            end_collection_flag: 结束采集标志
        """
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, self.WIDTH, self.HEIGHT, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, self.WIDTH, self.HEIGHT, rs.format.z16, 30)
        profile = pipeline.start(config)
        align_to = rs.stream.color
        align = rs.align(align_to)

        frames = pipeline.wait_for_frames()  # 等待管道中的帧
        start_capture.value += 1  # 增加开始捕获计数
        while start_capture.value < self.CAMERA_DEVICE_NUM:  # 等待所有视频开始捕获
            pass

        frame_num = 0  # 帧计数器
        while not stop_capture.value:  # stop capture值变为1时，停止该摄像头的记录
            while not start_collection_flag.value:
                frame_num = 0
            while frame_num < self.MAX_FRAMES and not end_collection_flag.value:
                # st = time.time()  # 记录开始时间
                frames = pipeline.wait_for_frames()  # 等待管道中的帧

                aligned_frames = align.process(frames)  # 对齐深度和彩色图像帧
                # 获取RGB图像
                color_frame = aligned_frames.get_color_frame()
                color_image = np.asanyarray(color_frame.get_data())
                # 获取深度图像
                depth_frame = aligned_frames.get_depth_frame()
                depth_image = np.asanyarray(depth_frame.get_data())

                # 记录时间戳
                time_nanosec = time.time_ns()  # 获取当前时间的纳秒级时间戳
                timestamps_np = np.frombuffer(timestamps.get_obj(), dtype='int64').reshape((self.MAX_FRAMES,))
                timestamps_np[frame_num] = time_nanosec

                if frame_num == 0:
                    print("Realsense Captured.")  # 打印RealSense已捕获

                # 将帧保存到共享内存缓冲区
                RGB_shared_frames_np = np.frombuffer(RGB_shared_frames.get_obj(), dtype=np.uint8).reshape(
                    (self.MAX_FRAMES, self.HEIGHT, self.WIDTH, self.CHANNELS))
                RGB_shared_frames_np[frame_num] = color_image

                depth_shared_frames_np = np.frombuffer(depth_shared_frames.get_obj(), dtype=np.uint16).reshape((self.MAX_FRAMES, self.HEIGHT, self.WIDTH))
                depth_shared_frames_np[frame_num] = depth_image

                frame_num += 1  # 更新帧计数器

                frame_num_return.value = frame_num  # 记录已捕获帧的数量

                # time.sleep(max(0, TIME_INTERVAL - (time.time() - st)))  # 控制帧捕获间隔

        pipeline.stop()  # 停止视频捕获设备


    def start(self):
      """
      开始数据收集流程
      """
      # 初始化标志
      start_capture = mp.Value('i', 0)
      stop_capture = mp.Value('i', 0)
      start_collection_flag = mp.Value('i', 0)
      end_collection_flag = mp.Value('i', 0)
      kill_collection_flag = mp.Value('i', 0)
      fileio_flag = mp.Value('i', 0)

      # 为每个按键绑定一个对应函数
      keyboard.add_hotkey('s', self.start_collection)
      keyboard.add_hotkey('e', self.end_collection)
      keyboard.add_hotkey('k', self.kill_collection)


      # 与时间服务器对齐时间
      local_time = time.time()  # 获取本地时间

      # 初始化存储数组

      color_video_size = self.MAX_FRAMES * self.HEIGHT * self.WIDTH * self.CHANNELS  # RGB视频形状
      depth_video_size = self.MAX_FRAMES * self.HEIGHT * self.WIDTH * 2  # 深度视频形状

      RGB_shared_frames = [mp.Array('B', color_video_size) for _ in range(self.CAMERA_DEVICE_NUM)]  # 每个RGB视频输入一个共享内存数组
      depth_shared_frames = [mp.Array('B', depth_video_size)]  # 每个深度视频输入一个共享内存数组

      timestamps_size = self.MAX_FRAMES  # 时间戳形状
      shared_timestamps = [mp.Array('d', timestamps_size) for _ in range(self.CAMERA_DEVICE_NUM)]  # 每个摄像头设备的时间戳输入一个共享内存数组

      frame_nums_share = [mp.Value('i', 0) for _ in range(self.CAMERA_DEVICE_NUM)]  # 每个摄像头设备的视频长度输入一个共享内存数组

      # wrist摄像头设备进行捕获
      procs = []
      proc = Process(target=self.capture_frames, args=(
              self.WRIST_COLOR_INDEX,
              RGB_shared_frames[self.WRIST_COLOR_INDEX],
              shared_timestamps[self.WRIST_COLOR_INDEX],
              frame_nums_share[self.WRIST_COLOR_INDEX],
              self.CAMERA_DEVICE_NUM,
              start_capture,
              stop_capture,
              start_collection_flag,
              end_collection_flag
              ))
      procs.append(proc)
      proc.start()
      # realsense摄像头设备进行捕获
      proc = Process(target=self.capture_realsense, args=(
              RGB_shared_frames[self.REALSENSE_COLOR_INDEX],
              shared_timestamps[self.REALSENSE_COLOR_INDEX],
              frame_nums_share[self.REALSENSE_COLOR_INDEX],
              depth_shared_frames[self.REALSENSE_DEPTH_INDEX],
              self.CAMERA_DEVICE_NUM,
              start_capture,
              stop_capture,
              start_collection_flag,
              end_collection_flag
              ))
      procs.append(proc)
      proc.start()

      #摄像头视频记录
      while stop_capture.value == 0:
          while end_collection_flag.value == 0:
              pass
              
          # 确保各线程保存了当前最后一帧数据
          time.sleep(0.1)

          # 等待所有视频开始捕获
          while start_capture.value < self.CAMERA_DEVICE_NUM:
              print("Waiting for videos to be captured.", flush=True)

          if kill_collection_flag.value == 0:
              
              self.save_episode(RGB_shared_frames=RGB_shared_frames, depth_shared_frames=depth_shared_frames, shared_timestamps=shared_timestamps, frame_nums_share=frame_nums_share)

          print('\033[91m' + 'file io done.' + '\033[0m')
          fileio_flag.value = 0
          end_collection_flag.value = 0

      for proc in procs:
          proc.join()
