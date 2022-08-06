import numpy as np
import pandas as pd
import cv2
from os import listdir

GT_box = pd.DataFrame(columns = ['File Name','x','y','w','h'])

img_files = listdir(GT_resized)

indeces_x = []
indeces_y = []
idx = 0
cc = 0

for file in img_files:
	f = file.split('.')
	f_name = f[0]
	GT_name = f_name + '_GT'
	image = cv2.imread(GT_name + '.jpg')
	
	# Finding the bouding box by getting the min and max values of index of the GT image array. For black pixels pixel value is 0
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			if image[i][j] == 0:
				indeces_x[idx] = i
				indeces_y[idx] = j
				idx += 1
	
	x = min(indeces_x)
	y = max(indeces_y)
	w = max(indeces_x) - min(indeces_x)
	h = max(indeces_y) - min(indeces_y)
	
	GT_box.loc[cc] = [f_name] + list([x,y,w,h])
	cc += 1
	
GT_box.to_csv('GT_BoundingBox.csv',index=False)
