import sys
from PIL import ImageFilter
from PIL import Image
import os
import os.path
import glob
import cv2

CAPTCHA_IMAGE_FOLDER = "origin"
OUT_FOLDER = "px_captcha2"

# CAPTCHA_IMAGE_FOLDER = "t1"
# OUT_FOLDER = "t2"


def denoise(image):
  imageBGR = image.copy() 
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  rows, cols, = image.shape[0:2] # 获得行数和列数
  # 底色变白
  for r in range(rows):
    for c in range(cols):
      if image[r][c] > 200:
        image[r][c] = 255

  # 去杂线
  for r in range(rows):
    for c in range(cols):
      up = image[r-1,c] if r > 0 else 255
      dw = image[r+1, c] if r < rows-1 else 255
      lt = image[r, c-1] if c > 0 else 255
      rt = image[r, c+1] if c < cols-1 else 255
      if up == 255 and dw == 255:
        image[r][c] = 255
      if lt == 255 and rt == 255:
        image[r][c] = 255

  # 去杂块横向
  for r in range(rows):
    for c in range(cols):
      if r > 0 and c > 0 and r < rows-2 and c < cols-2 and image[r][c] != 255 and image[r][c+1] != 255:
        up = image[r-1,c]
        dw = image[r+1, c]
        lt = image[r, c-1]
        rt = image[r, c+1]

        list = [up, dw, lt, image[r-1,c+1], image[r+1][c+1], image[r][c+2]]
        if list.count(255) >= 4:
          image[r][c] = 254
          image[r][c+1] = 254


  # 去杂块纵向
  for r in range(rows):
    for c in range(cols):
      if r > 0 and c > 0 and r < rows-1 and c < cols-1 and image[r][c] != 255 and image[r+1][c] != 255:
        up = image[r-1,c]
        dw = image[r+1, c]
        lt = image[r, c-1]
        rt = image[r, c+1]
        list = [up, image[r+2][c] if r < rows-2 else 255 ]
        if list.count(255) == 2:
          image[r][c] = 254
          image[r+1][c] = 254 

  # 底色转白2
  for r in range(rows):
    for c in range(cols):
      if image[r][c] == 254:
        image[r][c] = 255

  # 去杂线
  for r in range(rows):
    for c in range(cols):
      up = image[r-1,c] if r > 0 else 255
      dw = image[r+1, c] if r < rows-1 else 255
      lt = image[r, c-1] if c > 0 else 255
      rt = image[r, c+1] if c < cols-1 else 255
      if up == 255 and dw == 255:
        image[r][c] = 255
      if lt == 255 and rt == 255:
        image[r][c] = 255
 
  # 回填后yetian
  for r in range(rows):
    for c in range(cols):
      if image[r][c] == 255:
        imageBGR[r][c] = [255, 255, 255]

  return imageBGR


if __name__=="__main__":
    captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*"))
    for (i, captcha_image_file) in enumerate(captcha_image_files):
      print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))
      filename = os.path.basename(captcha_image_file)
      captcha_correct_text = os.path.splitext(filename)[0]
      image = cv2.imread(captcha_image_file)
      img = denoise(image)
      output_path = OUT_FOLDER + '/' + captcha_correct_text + '.png'
      cv2.imwrite(output_path, img)