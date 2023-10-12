# import pyrealsense2 as rs
# import numpy as np
# import cv2
# import os
# import time
#
# # 初始化RealSense相机
# pipeline = rs.pipeline()
# config = rs.config()
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# pipeline.start(config)
#
# # 创建保存图像的文件夹
# if not os.path.exists('data/images'):
#     os.makedirs('data/images')
# if not os.path.exists('data/depth_filtered'):
#     os.makedirs('data/depth_filtered')
#
# try:
#     frame_number = 0
#     frame_rate = 2  # 目标帧率（每秒一对图像）
#     last_frame_time = time.time()
#
#     while True:
#         frames = pipeline.wait_for_frames()
#         color_frame = frames.get_color_frame()
#         depth_frame = frames.get_depth_frame()
#
#         if not color_frame or not depth_frame:
#             continue
#
#         current_time = time.time()
#
#         # 计算与上一帧的时间间隔
#         frame_interval = current_time - last_frame_time
#
#         if frame_interval >= 1.0 / frame_rate:
#             last_frame_time = current_time
#
#             # 获取RGB图像
#             color_image = np.asanyarray(color_frame.get_data())
#
#             # 获取深度图像，并将数据类型更改为8位整数
#             depth_image = np.asanyarray(depth_frame.get_data(), dtype=np.uint8)
#
#             # 显示RGB图像
#             cv2.imshow('RGB Image', color_image)
#
#             # 显示深度图像
#             depth_colormap = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
#             cv2.imshow('Depth Image', depth_colormap)
#
#             # 将RGB图像保存为PNG
#             color_image_path = f'images/img{frame_number}.png'
#             cv2.imwrite(color_image_path, color_image)
#
#             # 将深度图像保存为PNG
#             depth_image_path = f'depth_filtered/depth{frame_number}.png'
#             cv2.imwrite(depth_image_path, depth_colormap)
#
#             frame_number += 1
#
#         key = cv2.waitKey(1)
#         if key & 0xFF == ord('q'):
#             break
#
# except KeyboardInterrupt:
#     pass
# finally:
#     cv2.destroyAllWindows()
#     pipeline.stop()


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

# 创建存储图像的文件夹
if not os.path.exists("images"):
    os.makedirs("images")
if not os.path.exists("depth_filtered"):
    os.makedirs("depth_filtered")

# 计数器，用于给图像文件命名
count = 0

try:
    align_to = rs.stream.color
    align = rs.align(align_to)

    while True:
        # 等待新的帧
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        # 转换深度图像为伪彩色
        colorizer = rs.colorizer()
        colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())

        # 保存RGB图像和深度图像
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imwrite(f"images/img{count}.png", color_image)
        cv2.imwrite(f"depth_filtered/depth{count}.png", colorized_depth)

        count += 1

        # 每秒保存两对图像
        if count % 2 == 0:
            print(f"Saved images {count-2} and {count-1}")

except KeyboardInterrupt:
    pass
finally:
    pipeline.stop()

