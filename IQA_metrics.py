def brightness(im_file): # Calculate the image brightness using mean of all the pixel values.
	im_file = Image.open(im_file).convert('L')
	stat = ImageStat.Stat(im_file)
	return stat.mean[0]
   
def Obj_size(img): # Calculating the object size by finding out the number of pixels the object occupies for Ground truth Image.
	
	counter = 0
	for i in img:
		if i==0:
			counter = counter + 1	
		
	obj_size = counter/(416*416)
	
	return obj_size
	
def edge_entropy(img_file): # Finding the edge using Canny detection.
	ret, img = cv.threshold(img_file,127,255,cv.THRESH_BINARY) # Converting all pixel values above 127 to white.
	edge = cv2.Canny(img, 30, 200)
	return edge

def shannon_ent(img_file):
	img = shannon_entropy(img_file)
	return img
	
def contrast(img_file): # Contrast using standard deviation of gray scale image.
	img = cv2.cvtColor(img_file, cv2.COLOR_BGR2GRAY)
	contrast = img_grey.std()
	return contrast
