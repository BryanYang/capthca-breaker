import cv2
import glob
import os
import numpy as np

CAPTCHA_IMAGE_FOLDER = "t1"
OUT_FOLDER = "t2"


img = cv2.imread('t2/2QGP.png') # 读取图片
rows, cols, = img.shape[0:2] # 获得行数和列数

split_line=[14, 30, 46, 60]

for i in split_line:
  image = img.copy()
  list=[];
  line = image[0: rows, i]
  for p in line:
    if min(p) != 255:
      list.append(p)


  color=np.mean(np.asarray(list), axis=0)
  print(i)
  print(color)
  for r in range(rows):
    for c in range(cols):
      if np.amax(np.absolute(np.subtract(image[r][c], color))) > 15:
        image[r][c] = 255
      if abs(c-i) > 10:
        image[r][c] = 255

  cv2.imshow("image", image)
  cv2.waitKey(0)