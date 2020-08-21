##
# Author: Josh Gardner
# Displays and saves locations of peas in an image
##
import matplotlib.pyplot as plt
import cv2
import csv
import argparse
import os

#reads tsv file to get pea coordinates and displays them on the image.
def locatePea(name):
    img=name + ".png"
    tsv=name +  ".tsv"
    im = plt.imread(os.path.join(path,img))
    plt.imshow(im)
    with open(os.path.join(path,tsv)) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        next(reader)
        for row in reader:
            x = int(row[1])
            y = int(row[2])
            plt.scatter([x], [y])
    return im

parser = argparse.ArgumentParser(description='Display the locations of peas on ROI')
parser.add_argument('--dir', help='Where the images are',      nargs=1, type=str, required=True)
args = parser.parse_args()
path = args.dir[0]
#see if new folder path is test or train
if path[-5:] == "train":
    targ = path[-5:]
else:
    targ = path[-4:]
for img in os.listdir(path):
    if img[:3] == "ROI" and img[-4:] == ".png":
        im = locatePea(img[:-4])
        plt.axis('off')
        plt.savefig(os.path.join("Data","Located_Peas",targ,img))
        plt.title(img[:-4])
        plt.show()
        
        
