##
#Author: Joshua Gardner
#Loads model and classes to detect pea objects in images
##
import os
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import argparse
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

CLASSES_FILE = "classes.csv"
#sorts through snapshot folder to find latest trained model
model_path = os.path.join('snapshots', sorted(os.listdir('snapshots'),reverse=True)[0])
model = models.load_model(model_path,backbone_name ="resnet50")
model = models.convert_model(model)
labels_to_name = pd.read_csv(CLASSES_FILE, header= None).T.loc[0].to_dict()

THRES_SCORE = 0.6
#prepares image for detection model, draws boxes and predicition scores and saves the image
def detect_objects(aImg):
    imgName = aImg
    image = read_image_bgr(os.path.join(path,aImg + ".png"))
    draw = image.copy()
    draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
    image = preprocess_image(image)
    image, scale = resize_image(image)
    boxes, scores, labels = model.predict_on_batch(np.expand_dims(image,axis=0))
    boxes /=scale
    for box, score, label in zip(boxes[0], scores[0], labels[0]):
        if score < THRES_SCORE:
            break
        color = label_color(label)
        b = box.astype(int)
        draw_box(draw, b, color=color)
        caption = "{} {:.3f}".format(labels_to_name[label], score)
        draw_caption(draw, b , caption)
    cv2.imwrite(os.path.join("Data","Detected",imgName+".png"),draw)

path = "Data/Slices/train"
for img in os.listdir(path):
    if img[-4:] == ".png" and img[:1] == "R":
        detect_objects(img[:-4])
