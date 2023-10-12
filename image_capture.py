import pyrealsense2 as rs
import numpy as np
import cv2
import os

# 初始化RealSense相机
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)

image_path = 'data/images'
depth_path = 'data/depth_filtered'

# 创建保存图像的文件夹
if not os.path.exists(image_path):
    os.makedirs(image_path)
if not os.path.exists(depth_path):
    os.makedirs(depth_path)

frame_number = 0

# 创建深度到颜色对齐的对象
align = rs.align(rs.stream.color)

try:
    while True:
        frames = pipeline.wait_for_frames()

        # 使用对齐对象将深度帧和颜色帧对齐
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        # 获取RGB图像
        color_image = np.asanyarray(color_frame.get_data())

        # 获取深度图像
        depth_image = np.asanyarray(depth_frame.get_data())

        # 显示RGB图像
        cv2.imshow('RGB Image', color_image)

        # 显示深度图像
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        cv2.imshow('Depth Image', depth_colormap)

        # 检测是否按下 "s" 键，如果是则保存图像
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            color_image_path = f'{image_path}/img{frame_number}.png'
            depth_image_path = f'{depth_path}/depth{frame_number}.png'
            cv2.imwrite(color_image_path, color_image)
            cv2.imwrite(depth_image_path, depth_colormap)
            frame_number += 1
        elif key & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
