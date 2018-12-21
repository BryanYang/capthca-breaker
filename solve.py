from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import imutils
import cv2
import pickle
import matplotlib.pyplot as plt
from PIL import Image
from denoise import denoise


MODEL_FILENAME = "captcha_model1.hdf5"
MODEL_LABELS_FILENAME = "model_labels1.dat"
CAPTCHA_IMAGE_FOLDER = "origin5"


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
    image = denoise(image)
    predictions = []
    rows, cols, = image.shape[0:2] # 获得行数和列数
    r1, r2 =  [0, rows] #初始化r1, r2
    c1 = 0
    c2 = int(cols / 4)

    while c2 <= cols:
      letter_image = image[r1 : r2, c1 : c2]

      # Turn the single image into a 4d list of images to make Keras happy
      letter_image = np.expand_dims(letter_image, axis=2)
      letter_image = np.expand_dims(letter_image, axis=0)

      # Ask the neural network to make a prediction
      prediction = model.predict(letter_image)

      # Convert the one-hot-encoded prediction back to a normal letter
      letter = lb.inverse_transform(prediction)[0]
      predictions.append(letter)

      # draw the prediction on the output image
      # cv2.putText(output, letter, (c2, 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
      
      c1 = c2
      c2 += int(cols / 4)

    # Print the captcha's text
    captcha_text = "".join(predictions)
    print("CAPTCHA text is: {}".format(captcha_text))

    # Show the annotated image
    cv2.imshow("Output", output)
    cv2.waitKey(0)