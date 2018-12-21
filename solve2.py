from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import imutils
import cv2
import pickle
import matplotlib.pyplot as plt
from PIL import Image
from denoise2 import denoise


MODEL_FILENAME = "captcha_model2.hdf5"
MODEL_LABELS_FILENAME = "model_labels2.dat"
CAPTCHA_IMAGE_FOLDER = "origin6"

SPLIT_LINE=[14, 30, 46, 60]
COLOR_DISTANCE = 40
RANGE=8

# Load up the model labels (so we can translate model predictions to actual letters)
with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)

# Load the trained neural network
model = load_model(MODEL_FILENAME)

# Grab some random CAPTCHA images to test against.
# In the real world, you'd replace this section with code to grab a real
# CAPTCHA image from a live website.
captcha_image_files = list(paths.list_images(CAPTCHA_IMAGE_FOLDER))
captcha_image_files = np.random.choice(captcha_image_files, size=(10,), replace=False)

# loop over the image paths
for image_file in captcha_image_files:
    # Load the image and convert it to grayscale
    image = cv2.imread(image_file)
    # Create an output image and a list to hold our predicted letters
    output = cv2.merge([image])
    img = denoise(image)
    predictions = []
    rows, cols, = image.shape[0:2] # 获得行数和列数
    r1, r2 =  [0, rows] #初始化r1, r2

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
      letter_image = cv2.cvtColor(letter_image, cv2.COLOR_BGR2GRAY)
      # cv2.imshow("Output", letter_image)
      # cv2.waitKey(0)

      # Turn the single image into a 4d list of images to make Keras happy
      letter_image = np.expand_dims(letter_image, axis=2)
      letter_image = np.expand_dims(letter_image, axis=0)

      # Ask the neural network to make a prediction
      prediction = model.predict(letter_image)

      # Convert the one-hot-encoded prediction back to a normal letter
      letter = lb.inverse_transform(prediction)[0]
      predictions.append(letter)

    # Print the captcha's text
    captcha_text = "".join(predictions)
    print("CAPTCHA text is: {}".format(captcha_text))

    # Show the annotated image
    cv2.imshow("Output", output)
    cv2.waitKey(0)