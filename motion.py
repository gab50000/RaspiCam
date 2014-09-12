#!/usr/bin/python -u

import cStringIO as StringIO
#import Image 
import cv2
import picamera
import numpy as np
import time
import datetime
import os
#import ipdb

with picamera.PiCamera() as camera:
	image_data = StringIO.StringIO()
	camera.resolution = (160, 120)
	camera.capture(image_data, format="bmp", use_video_port=True)
	data = np.fromstring(image_data.getvalue(), dtype=np.uint8)
	imarr1 = cv2.imdecode(data, 1)
	image_data.reset()

	counter = 0
	active = 0
	start_time = time.time()
	while 1:
		image_data = StringIO.StringIO()
		camera.capture(image_data, format="bmp", use_video_port=True)
		data = np.fromstring(image_data.getvalue(), dtype=np.uint8)
		imarr2 = cv2.imdecode(data, 1)
		difference = 100*float(((imarr2-imarr1)**2).sum())/(imarr1**2).sum()
		brightness = 100*float(imarr2.sum())/(255*imarr2.shape[0]*imarr2.shape[1]*3)
		print "Difference: {:6.2f}%".format(difference), 
		print "Brightness: {:6.2f}%".format(brightness),
		print "{:6.2f} fps".format(float(counter)/(time.time()-start_time)), "\r",
		imarr1 = imarr2
		counter += 1
		if brightness > 50 or difference > 20:
			print ""
			active = 5 
			while active > 0:
				date = datetime.datetime.now()
				directory = "{}_{:02d}_{:02d}".format(date.year, date.month, date.day)
				if not os.path.exists(directory):
					os.mkdir(directory)
				filename = "{:02d}{:02d}{:02d}.jpg".format(date.hour, date.minute, date.second)
				print "Active! Writing to {}/{}".format(directory, filename), "\r",
				camera.capture(os.path.join(directory, filename), format="jpeg", use_video_port=True)
				active -= 1
				time.sleep(1)

		
