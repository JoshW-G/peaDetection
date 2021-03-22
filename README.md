Author: Joshua Gardner
Date: 28/04/2020

This is the code to my Dissertation project: "Detecting specific foods in MRI scans using TensorFlow and RetinaNet implemented in Python".
Note: this project was reimplemented into a published paper "Recognising Specific Foods in MRI Scans Using CNN and Visualisation" presented at CGVC 2020 avaialble here
https://diglib.eg.org/handle/10.2312/cgvc20201145
***IMPORTANT***
Required/Versions used:

Python v3.7.7
Tensorflow GPU v1.15
Keras RetinaNet (https://github.com/fizyr/keras-retinanet)
resnet50_coco_best_v2.1.0.h5 pretrained model(https://github.com/fizyr/keras-retinanet/releases)
LabelImg (https://pypi.org/project/labelImg/)
opencv-python (https://pypi.org/project/opencv-python/)
matplotlib(https://pypi.org/project/matplotlib/)
pandas(https://pypi.org/project/pandas/)
numpy(https://pypi.org/project/numpy/)

For Tensorflow to utilize the GPU correctly we require
Nvidia CUDA V10.0
Nvidia cuDNN v7.6.5 for CUDA V10.0
As well as a GPU capable enough for the CUDA toolkit (for example I used a GTX 1050)
***************

To reproduce the results we need to extract and prepare the data
using the commandline in the working directory:

python prepareData.py --dir Peas --newDir Data

Using pea_locator.py we can use the locations of the peas in each Region of interest(ROI) image using the .tsv
python pea_locator.py --dir Data/Slices/train
this will show where the peas are located on the images.

Now using LabelImg we can access those ROI images and label each pea manually which will produce xml files with each bounding box of the peas.(The current XML&csv files have a different path for the images which could be easily changed using a script)

Now using xml_to_csv.py we can extract all the information from the XML files so that RetinaNet can use it to train the model
We first need to delete the first row in the train_labels.csv so the data can be utilized without the headers.

Then using RetinaNets train.py we can then train the model
python retinanet\keras_retinanet\bin\train.py --freeze-backbone --random-transform --weights resnet50_coco_best_v2.1.0.h5 --batch-size 8 --steps 100 --epochs 10 csv train_labels.csv classes.csv

This step is very intensive and will take a long time.

now running detectPeas.py we can display the predictions made by the model. I have included the model I have trained. This model could be tweaked to improve better results and include more data from the datasets to improve accuracy
(The final snapshot of the model is included due to file size restrictions and that version is only needed)
python detectPeas.py --dir Data/Slices/test

We can the compare results with displayResults.py to the actual locations
