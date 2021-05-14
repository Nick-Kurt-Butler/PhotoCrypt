# This file is a rudimentary Stenanography script to encode
# and decode images.  I recommend using more complex encryption
# algorithms the require the same arguments and return the same
# as the functions below.

# A small code to test whether you encode-decode function works
# use this simple code and check if msg remains the same

# from PIL import Image
# im = Image.open("your_image.png")
# msg = "Your message"
# im = encode(im,msg)
# new_msg = decode(im)
# assert new_msg == msg

import numpy as np

def encode(im,msg):
	# Takes an image array and string message
	# returns an encryted image array
	im = np.array(im)
	h,w,_ = im.shape

	def alter_pixel(x,y,z,num):
		# num must be between 0 and 255
		im[y,x,z] = num

	l = len(msg)
	y0 = int(l/w)
	x0 = l-y0*w
	alter_pixel(x0,y0,0,0)
	for i in range(l):
		y = int(i/w)
		x = i-y*w
		alter_pixel(x,y,0,ord(msg[i]))

	return im

def decode(im):
	# Takes an image array
	# returns a decode message string
	im = np.array(im)
	h,w,_ = im.shape

	def get_info(x,y,z):
		return chr(im[y,x,z])

	msg = ""
	for j in range(w):
		for i in range(h):
			c = get_info(i,j,0)
			if c == '\0':
				return msg
			msg += c
	return msg
