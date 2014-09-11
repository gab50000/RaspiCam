#!/usr/bin/python
#TODO: opencv benutzen! -> img direkt nach numpy array?

import cStringIO as StringIO
#import Image 
import cv2
import picamera
import numpy as np
#import time
#import ipdb

with picamera.PiCamera() as camera:
	image_data = StringIO.StringIO()
	camera.resolution = (160, 120)
	camera.capture(image_data, format="bmp", use_video_port=True)
	data = np.fromstring(image_data.getvalue(), dtype=np.uint8)
	imarr1 = cv2.imdecode(data, 1)
	image_data.reset()

	while 1:
		image_data = StringIO.StringIO()
		camera.capture(image_data, format="bmp", use_video_port=True)
		data = np.fromstring(image_data.getvalue(), dtype=np.uint8)
		imarr2 = cv2.imdecode(data, 1)
		print float(((imarr2-imarr1)**2).sum())/(imarr1**2).sum()
		imarr1 = imarr2
	#	time.sleep(1)
		
