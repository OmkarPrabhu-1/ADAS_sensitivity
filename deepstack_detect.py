import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import numpy as np
from os import listdir
import pandas as pd
import csv
import glob
import os
from Compute_IOUs import compute_IoU

i = 0
IoU = 0
x = 0
y = 0
w = 0
h = 0

GT = pd.read_csv("GT_BoundingBox.csv")
img_files = listdir('Images_Resized')
Deepstack_results = pd.DataFrame(columns = ['File Name','Confidence', 'IoU', 'Composite'])


for file in img_files:
	split_name = file.split('.')
	f_name = split_name[0]
	
	car_no = 0
	
	image_data = open('Images_Resized'+'/'+file,"rb").read()
	response = requests.post("http://localhost:80/v1/vision/detection",files={"image":image_data}).json() # using port 80
	# Checking if the image contains a car
	
	for object in response["predictions"]:
		if object['label'] == 'car' or object['label'] == 'Car':
			car_no += 1 
			
	for object in response["predictions"]:
		con_value = 0 # Resetting the confidence value every iteration
		
		if object['label'] == 'car' and car_no != 0:
			startX = object["x_min"]
			endX = object["x_max"]
			startY = object["y_min"]
			endY = object["y_max"]
			conf = object["confidence"]
			x = startX  # X of top left
			y = startY  # Y of top left
			w = abs(startX - endX)
			h = abs(startY - endY)
			con_value = conf
			
			image = cv2.imread("Images_resized/" + file, cv2.IMREAD_COLOR)
			cv2.rectangle(image, (startX, startY), (endX, endY), (255,255,255), 2)
			image = cv2.putText(image, 'Confidence : '+ str(conf), (x-5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 255), 1, cv2.LINE_AA)
			cv2.imwrite("Images_boxed/" + f_name + "_box" + ".jpg", image)
			
			a = [x,y,x+w,y+h]
			b = [gt_x,gt_y,gt_x+gt_w,gt_y+gt_h]
			IoU= compute_IoU(a,b)
			composite = (con_value+IoU)/2
			
		elif car_no == 0: # If a car is not detected
			x = 0  # X of top left
			y = 0  # Y of top left
			w = 0
			h = 0
			con_value = 0
			con_value = int(con_value)
			image = cv2.imread("Images_resized/" + file, cv2.IMREAD_COLOR)
			gt_x = GT.loc[counter].iat[1]
			gt_y = GT.loc[counter].iat[2]
			gt_w = GT.loc[counter].iat[3]
			gt_h = GT.loc[counter].iat[4]
			a = [x,y,x+w,y+h]
			b = [gt_x,gt_y,gt_x+gt_w,gt_y+gt_h]
			IoU= compute_IoU(a,b)
			break;
			
	if not response["predictions"]: # If no object is detected in the image
		image = cv2.imread("Images_resized/" + file, cv2.IMREAD_COLOR)
		x = 0  # X of top left
		y = 0  # Y of top left
		w = 0
		h = 0
		con_value = 0
		con_value = int(con_value)
		gt_x = GT.loc[counter].iat[1]
		gt_y = GT.loc[counter].iat[2]
		gt_w = GT.loc[counter].iat[3]
		gt_h = GT.loc[counter].iat[4]
		a = [x,y,x+w,y+h]
		b = [gt_x,gt_y,gt_x+gt_w,gt_y+gt_h]
		IoU= compute_IoU(a,b)
		
	composite = (con_value+IoU)/2
	Deepstack_results.loc[i] = [f_name] + list([con_value, IoU, composite, x, y, w, h])
	
Deepstack_results.to_csv('Deepstack_Results.csv',index=False)
