#!/usr/bin/python -u

import cStringIO as StringIO
#import Image 
import cv2
import picamera
import numpy as np
import time
import datetime
import os
import sys
import subprocess

PIC_DIR = "/home/pi/fotos/"
log_filename = "/home/pi/motion_log"

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
	print ""

#specify time in minutes
if len(sys.argv) > 1:
	print "time specified. running for {} minutes.".format(sys.argv[1])
	max_time = int(sys.argv[1])*60
	infinite = False
else:
	print "no time specified. running forever."
	infinite = True

with picamera.PiCamera() as camera:
	image_data = StringIO.StringIO()
	camera.resolution = (160, 120)
	camera.capture(image_data, format="bmp", use_video_port=True)
	data = np.fromstring(image_data.getvalue(), dtype=np.uint8)
	imarr1 = cv2.imdecode(data, 1).sum(axis=2)/3
	image_data.reset()
	counter = 0
	active = 0
	shooting_stop = 20
	light_stop = 0
	last_log = 0
	light = False
	start_time = time.time()
	
	with open(log_filename, "aw") as f:
		print >> f, "#Start at {}".format(datetime.datetime.now())

	while infinite == True or time.time()-start_time < max_time:
		image_data = StringIO.StringIO()
		camera.capture(image_data, format="bmp", use_video_port=True)
		data = np.fromstring(image_data.getvalue(), dtype=np.uint8)
		imarr2 = cv2.imdecode(data, 1).sum(axis=2)/3
		difference = 100*float(((imarr2-imarr1)**2).sum())/(imarr1**2).sum()
		brightness = 100*float(imarr2.sum())/(255*imarr2.shape[0]*imarr2.shape[1])
		print "Difference: {:6.2f}%".format(difference), 
		print "Brightness: {:6.2f}%".format(brightness),
		print "{:6.2f} fps".format(float(counter)/(time.time()-start_time)), "\r",
		imarr1 = imarr2
		counter += 1
		time_now = time.time()
		
		if time_now > light_stop:
			if (difference > 0.3 and brightness > 15) or (difference > 0.9 and brightness > 5):
				subprocess.call("rcsend 11111 4 1".split())
				light = True
				light_stop = time_now + 5 
				shooting_stop = time_now + 1

		if difference > 0.9 and brightness > 10 and time_now > shooting_stop:
			shoot_pics(5, (640,480), 1)
			shooting_stop = time_now + 20
			light_stop = time_now + 20
			light = True

		if time_now > light_stop and light == True:
			subprocess.call("rcsend 11111 4 0".split())
			light = False
			light_stop = time_now + 1 
			shooting_stop = time_now + 1 
		if time_now % 60 == 0 and time_now > last_log: 
			with open(log_filename, "aw") as f:
				print >> f, datetime.datetime.now().hour*60+datetime.datetime.now().minute, brightness
 


		if counter == 1000:
			counter = 0


		
