def crop(image):
	
	# Resizing the image to required dimensions
	dim = (416, 416)
	image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) # using INTER_AREA – resampling using pixel area relation
	
return image
