#!/usr/bin/python
#TODO: opencv benutzen! -> img direkt nach numpy array?

import cStringIO as StringIO
import Image 
import picamera
import numpy as np
import time
import pdb

camera = picamera.PiCamera()
image_data = StringIO.StringIO()
camera.capture(image_data, format="bmp", use_video_port=True)
print len(image_data.getvalue())
image_data.reset()
im = Image.open(image_data)
image_data.reset()
#image_data.truncate()
imarr1 = np.array(im)
pdb.set_trace()

while 1:
	image_data = StringIO.StringIO()
	camera.capture(image_data, format="bmp", use_video_port=True)
	image_data.seek(0)
	im = Image.open(image_data)
	imarr2 = np.array(im)
#	pdb.set_trace()
	print float(((imarr1-imarr2).sum(axis=2)**2).sum())/(imarr1.sum(axis=2)**2).sum()
	imarr1 = imarr2
#	time.sleep(1)
	
