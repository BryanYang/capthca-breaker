import cv2
import glob
import os
import numpy as np

CAPTCHA_IMAGE_FOLDER = "px_captcha2"
OUTPUT_FOLDER = "extracted_letter_images2"
SPLIT_LINE=[14, 30, 46, 60]
COLOR_DISTANCE = 30
RANGE=9


counts = {}

def make_neg(path):
    filename = os.path.basename(path)
    captcha_correct_text = os.path.splitext(filename)[0]
    k = 0 # 图片计数用的变量
    img = cv2.imread(path) # 读取图片
    rows, cols, = img.shape[0:2] # 获得行数和列数
    for i in SPLIT_LINE:
      image = img.copy()
      list=[];
      line = image[0: rows, i]
      for p in line:
        if min(p) != 255:
          list.append(p)
      color=np.mean(np.asarray(list), axis=0)
  
      for r in range(rows):
        for c in range(cols):
          if np.amax(np.absolute(np.subtract(image[r][c], color))) > COLOR_DISTANCE:
            image[r][c] = 255
          if abs(c-i) > RANGE:
            image[r][c] = 255
      
      letter_image = image[0:26, i-8:i+8]
      # Get the folder to save the image in
      letter_text = captcha_correct_text[k]
      save_path = os.path.join(OUTPUT_FOLDER, letter_text)
      
      # if the output directory does not exist, create it
      if not os.path.exists(save_path):
        os.makedirs(save_path)

      # write the letter image to a file
      count = counts.get(letter_text, 0)
      p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))
      cv2.imwrite(p, letter_image)

      # increment the count for the current key
      counts[letter_text] = count + 1
      k+=1
   

if __name__ == "__main__":
  captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*"))
  for (i, captcha_image_file) in enumerate(captcha_image_files):
    print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))
    make_neg(captcha_image_file)
