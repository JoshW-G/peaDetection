##
#Author: Josh Gardner
#Parses XML data into a pandas DataFrame to be saved in a csv 
#
##
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import argparse
import csv

def xml_to_csv(path):
    #function to parse xml files and extract the data to a dataframe
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('path').text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text),
                     member[0].text
                     )
            xml_list.append(value)
    column_name = ['path', 'x1', 'y1', 'x2', 'y2', 'class']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

path = "Data/Slices/train"
xml_df = xml_to_csv(path)
xml_df.to_csv('train_labels.csv', index=None)
with open("classes.csv", mode='w', newline='') as class_file:
    class_writer = csv.writer(class_file,delimiter=",",quotechar='"',quoting=csv.QUOTE_MINIMAL)
    class_writer.writerow(["pea", 0])

print('Successfully converted xml to csv.')



