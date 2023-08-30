#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/16 17:19
# @Author  : Scott Yang
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# https://huggingface.co/keremberke/yolov8m-table-extraction
import cv2
from PIL import Image
from ultralyticsplus import YOLO, render_result

# load model
model = YOLO('keremberke/yolov8m-table-extraction')
# model = YOLO('yolov8n.pt')

# set model parameters
model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # maximum number of detections per image

# set image
image = './adidas_1.jpg'
# img = Image.open('./adidas_1.jpg')
# perform inference
results = model.predict(image)

# observe results
print(results[0].boxes)

img = render_result(model=model, image=image, result=results[0])
# # render.show()
img.save("table_detect.png")

# img = cv2.imread(image)

xyxy_list = results[0].boxes.xyxy.tolist()
single_tbs = []  # [(tb_y1, tb_y2)]
tb_images = []
for x1, y1, x2, y2 in xyxy_list:
    print(f'y: {y1}, h:{y2 - y1}, w:{x2 - x1}')
    # skip overlapping table
    over = False
    for sig_y1, sig_y2 in single_tbs:
        if sig_y1 < y1 < sig_y2 or sig_y1 < y2 < sig_y2:
            over = True
            break

    if over:
        continue

    single_tbs.append((y1, y2))
    tb_img = img.crop((x1, y1, x2, y2))
    tb_img.save(f'./extract_table/{y1}.jpg')



