##
# Author: Josh Gardner
# Displays detected results against actual locations in the images
##
import matplotlib.pyplot as plt
import os

detectPath = "Data/Detected"
locPath = "Data/Located_Peas/test"
#Display images of detected objects along side actual locations
for img in os.listdir(detectPath):
    if os.path.isfile(os.path.join(detectPath, img)):
        imgName = img[:-4]  
        im1 = plt.imread(os.path.join(detectPath, img))
        im2 = plt.imread(os.path.join(locPath, imgName+".png"))
        fig = plt.figure()
        a = fig.add_subplot(1, 2, 1)
        imgplt = plt.imshow(im1)
        plt.axis('off')
        a.set_title("Detected peas")
        a = fig.add_subplot(1,2,2)
        imgplot = plt.imshow(im2)
        plt.axis('off')
        plt.show()
    
