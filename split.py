import cv2
import glob
import os

CAPTCHA_IMAGE_FOLDER = "px_captcha"
OUTPUT_FOLDER = "extracted_letter_images1"

counts = {}

def make_neg(path):
    filename = os.path.basename(path)
    captcha_correct_text = os.path.splitext(filename)[0]
    k = 0 # 图片计数用的变量
    image = cv2.imread(path) # 读取图片
    rows, cols, = image.shape[0:2] # 获得行数和列数
    r1, r2 =  [0, rows] #初始化r1, r2
    c1 = 0
    c2 = int(cols / 4)
    while c2 <= cols:
      # 截取图片
      letter_image = image[r1 : r2, c1 : c2] 
      # Get the folder to save the image in
      letter_text = captcha_correct_text[k]
      save_path = os.path.join(OUTPUT_FOLDER, letter_text)
      
      # if the output directory does not exist, create it
      if not os.path.exists(save_path):
        os.makedirs(save_path)

      # write the letter image to a file
      count = counts.get(letter_text, 500)
      p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))
      cv2.imwrite(p, letter_image)

      # increment the count for the current key
      counts[letter_text] = count + 1

      c1 = c2
      c2 += int(cols / 4)
      k += 1

if __name__ == "__main__":
  captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*"))
  for (i, captcha_image_file) in enumerate(captcha_image_files):
    print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))
    make_neg(captcha_image_file)
