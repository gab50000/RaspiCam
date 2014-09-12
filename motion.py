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

PIC_DIR = "/shared/"

def shoot_pics(number, resolution, delay_sec):
	resolution_init = camera.resolution
	camera.resolution = resolution 
	print ""
	while number > 0:
		date = datetime.datetime.now()
		directory = "{}_{:02d}_{:02d}".format(date.year, date.month, date.day)
		if not os.path.exists(os.path.join(PIC_DIR, directory)):
			os.mkdir(os.path.join(PIC_DIR, directory))
		filename = "{:02d}{:02d}{:02d}.jpg".format(date.hour, date.minute, date.second)
		print "Active! Writing to {}/{}/{}".format(PIC_DIR, directory, filename), "\r",
		camera.capture(os.path.join(PIC_DIR, directory, filename), format="jpeg", use_video_port=True)
		number -= 1
		time.sleep(delay_sec)
	camera.resolution = resolution_init


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

		if difference > 5 and counter > 20:
			shoot_pics(5, (640,480), 1)
			counter = 0
			start_time = time.time()

		if counter == 1000:
			counter = 0


		
