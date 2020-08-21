##
#Author: Josh Gardner
#Script to parse dataset files, extracting and renaming them
#
##
import argparse # To process the command line arguments
import os       # To parse the filesystem and create directories
import sys      # To print the standard output of errors
import numpy as np # to load txt files
import cv2
import errno    # To handles errors when file are copied and directories created
import shutil   # To copy files

def createDir(aDirectory):
    try:
        os.mkdir(aDirectory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print ("Creation of the directory %s failed" % aDirectory, file=sys.stderr)
            raise
#moves tsv files and renames them according to related image file
def moveTSV(aName, aDir, aType):
    tsv_name = str(aName[:-4] + ".tsv")
    print(tsv_name)
    shutil.copyfile(aDir,os.path.join(args.newDir[0],"Slices",aType,tsv_name))

def prepare_data(aSource, aDir):
    pos_count = 0
    neg_count = 0
    slice_count = 0
    for dataset in os.listdir(aSource):
    #loops through all path directories extracting the data into correct directories to be used
        if os.path.isdir(os.path.join(aSource,dataset)):
            if dataset[:7] == "DATASET":
                dataset_id = dataset[7:]
                dataset_path = os.path.join(aSource,dataset)
                for slices in os.listdir(dataset_path):
                    if os.path.isdir(os.path.join(dataset_path,slices)):
                        if slices[:6] == "slice_":
                            slice_id = slices[6:]
                            slice_path = os.path.join(dataset_path,slices)
                            for labels in os.listdir(slice_path):
                                if (labels[:6] == "slice_" or labels[:3]=="ROI") and labels[-4:] == ".png":
                                    slice_count+=1
                                    if (int(dataset[7:])%2)==0: #splits data into training and data sets
                                        shutil.copyfile(os.path.join(slice_path,labels), os.path.join(aDir,"Slices","train",labels))
                                        if labels[:3] == "ROI" and os.path.exists(os.path.join(slice_path,labels,"pos","pos.tsv")) == True:
                                            moveTSV(labels,os.path.join(slice_path,labels,"pos","pos.tsv"),"train")
                                    else:
                                        shutil.copyfile(os.path.join(slice_path,labels), os.path.join(aDir,"Slices","test",labels))
                                        if labels[:3] == "ROI" and os.path.exists(os.path.join(slice_path,labels,"pos","pos.tsv")) == True:
                                            moveTSV(labels,os.path.join(slice_path,labels,"pos","pos.tsv"),"test")
                                #moves and renames images of peas
                                elif os.path.isdir(os.path.join(slice_path, labels)):
                                    if labels == "pos" or labels == "neg":
                                        labels_path = os.path.join(slice_path, labels)
                                        for img in os.listdir(labels_path):
                                            if  img[-4:] == ".png":
                                                if labels == "pos":
                                                    pos_count+=1
                                                    image = cv2.cvtColor(cv2.imread(os.path.join(labels_path, img)), cv2.COLOR_BGR2GRAY)
                                                    imgName="Pea_"+str(pos_count)+".png"
                                                    if (int(dataset[7:])%2)==0:
                                                        cv2.imwrite(os.path.join(aDir,"Peas","train",imgName),image)
                                                    else:
                                                        cv2.imwrite(os.path.join(aDir,"Peas","test",imgName),image)
                                                elif labels == "neg":
                                                    neg_count+=1
                                                    image = cv2.cvtColor(cv2.imread(os.path.join(labels_path, img)), cv2.COLOR_BGR2GRAY)
                                                    imgName="neg_"+str(neg_count)+".png"
                                                    cv2.imwrite(os.path.join(aDir,"Neg",imgName),image)

    print("Prepared and Moved", pos_count, "images and moved", neg_count, "negative images")
    print("Moved", slice_count, "Slices")


parser = argparse.ArgumentParser(description='Prepare and Copy images to new directory')
parser.add_argument('--dir', help='Where the data to copy is',      nargs=1, type=str, required=True)
args = parser.parse_args()
newPath = "Data"
createDir(newPath)
createDir(os.path.join(newPath,"Peas"))
createDir(os.path.join(newPath,"Neg"))
createDir(os.path.join(newPath,"Slices"))
createDir(os.path.join(newPath,"Detected"))
createDir(os.path.join(newPath,"Located_Peas"))
createDir(os.path.join(newPath,"Located_Peas","train"))
createDir(os.path.join(newPath,"Located_Peas","test"))         
createDir(os.path.join(newPath,"Peas","train"))
createDir(os.path.join(newPath,"Peas","test"))
createDir(os.path.join(newPath,"Slices","train"))
createDir(os.path.join(newPath,"Slices","test"))
prepare_data(args.dir[0],newPath)
