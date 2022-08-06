import cv2 as cv
import numpy as np
from skimage.measure.entropy import shannon_entropy
import matplotlib.pyplot as plt
from scipy.io import savemat
from os import listdir
import pandas as pd
from pathlib import Path
from crop import crop
from image_similarity_measures.quality_metrics import rmse, psnr, ssim, fsim, issm
from OSU_IQAs import obj_size_IQA, brtness, brisq, cpbd, edge_entropy, gray_entropy, contrast
import imquality.brisque as brisque
from IQA_metrics import brightness, Obj_size
import cpbd

Img_Dir = 'Images'
GT_Dir = 'GT'

Img = 'Images_resized'
GT = 'GT_resized'

IoUs = pd.DataFrame(columns = ['File Name','RMSE','PSNR','SSIM','FSIM','ISSM','BRISQUE','BRIGHTNESS','OBJ_SIZE','CPBD','Edge Entropy','Grayscale Entropy','Contrast'])

files_img = listdir(Img_Dir)
files_GT = listdir(GT_Dir)

# Resizing the image files
for file in files_img:
	split = file.split('.')
	f_name = split[0]
	image = cv2.imread("Images/" + file, cv2.IMREAD_COLOR)
	image = crop(image)
	image = cv2.imwrite("Images_resized/" + f_name + ".jpg", image)

# Resizing the ground truth files
for file in files_GT:
	split = file.split('.')
	f_name = split[0]
	image = cv2.imread("GT/" + file, cv2.IMREAD_COLOR)
	image = crop(image)
	image = cv2.imwrite("GT_resized/" + f_name + ".jpg", image)
	

files_img = listdir(Img)
files_GT = listdir(GT)

# To check if ground truth exists for every image file, if not then delete the image file
for file in files_img:
	split = file.split('.')
	f_name = split[0]
	gt_name = f_name+'_GT'
	gt_img = Path('GT_resized/'+g_name+'.jpg')
	
    if not(gt_img.exists()):
	print('No groud truth found for '+ f_name)
	img_files.remove(file)
	continue

	img = cv2.imread('Images_resized/' + file ,cv2.IMREAD_COLOR)	
	img_GT = cv2.imread(gt_img ,cv2.IMREAD_COLOR)
	
	# Finding the various image properties
	r  = 1-rmse(img,img) # Root mean squared
	p  = psnr(img,img)/100 # Peak signal to noise ratio
	s  = ssim(img,img) # Structural similarity metrics
	f  = fsim(img,img) # Feature structural similarity metrics
	i = 0 # isim is neglected
	brq  = brisque.score(img) # Brisque score
	brt  = brightness(img) # Brightness, Gives average pixel brightness
	siz  = Obj_size(img_GT) # Object size
	c = cpbd(img) # Cumulative Probability of Blur Detection, Credits: Copyright (c) 2009-2010 Arizona Board of Regents.  All Rights Reserved.
	ee = edge_entropy(img) # This is convertion to binary image and then canny edge detection
	ge = shannon_ent(img) # A Shannon entropy 
	cts = contrast(img) # Standard deviation of the pixel brightness
	
	
	IoUs.loc[idx] = [f_name]+list([r,p,f,s,i,brq,brt,siz,c,ee,ge,cts])
	idx = idx + 1
	
	
# Saving the IQAs
IoUs.to_csv('IoUs.csv',index=False)
