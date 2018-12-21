### Before you get started

To run these scripts, you need the following installed:

1. Python 3
2. OpenCV 3 w/ Python extensions
 - I highly recommend these OpenCV installation guides: 
   https://www.pyimagesearch.com/opencv-tutorials-resources-guides/ 
3. The python libraries listed in requirements.txt
 - Try running "pip3 install -r requirements.txt"


Run 
```
./bin/download_img.sh 
```
Download images into the dir 'origin'

### Step 1: Extract single letters from CAPTCHA images

Run:

python3 denoise2.py

denoies the captcha images. by this, the capacity will be better.

Run:

python3 split2.py

The results will be stored in the "extracted_letter_images" folder.


### Step 2: Train the neural network to recognize single letters

Run:

python3 train_model2.py

This will write out "captcha_model2.hdf5" and "model_labels2.dat"


### Step 3: Use the model to solve CAPTCHAs!

Run: 

python3 slove2.py

有2套模型，一套基于大小split. 一套基于颜色抓取。 