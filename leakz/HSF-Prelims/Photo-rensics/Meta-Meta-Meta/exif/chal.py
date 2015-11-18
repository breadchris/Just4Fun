#!/usr/bin/env python
'''
Running instructions.
 sockets are insecure. We do not implement any socket behaviour in this
 file.
 Please make this file +x and run with socat:
	socat TCP-LISTEN:45454,reuseaddr,fork EXEC:./chal.py,pty,stderr,echo=0

Debugging:
 Just execute chal.py and play on terminal, no need to run socat
'''

import os
import sys
import time
import random

from PIL import Image
from PIL.ExifTags import TAGS

from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
	pass

def timeout(seconds=30, error_message=os.strerror(errno.ETIME)):
	def decorator(func):
		def _handle_timeout(signum, frame):
			print 'Connection Timeout'
			sys.exit()

		def wrapper(*args, **kwargs):
			signal.signal(signal.SIGALRM, _handle_timeout)
			signal.alarm(seconds)
			try:
				result = func(*args, **kwargs)
			finally:
				signal.alarm(0)
			return result

		return wraps(func)(wrapper)

	return decorator

def retrieveExif(img):
	exif = {}
	try:
		info = img._getexif()
		for tag, value in info.items():
			decoded = TAGS.get(tag, tag)
			exif[decoded] = '{}'.format(value).strip()
	except Exception, e:
		exif = exif
	return exif

@timeout(30)
def chal():
	flag = open('flag.txt', 'r').read().strip()

	# Populate the following files if you want to cycle the messages being returned
	slow  = open('slow.txt' , 'r').read().split('\n')
	wrong = open('wrong.txt', 'r').read().split('\n')
	right = open('right.txt', 'r').read().split('\n')

	if len(slow) == 1 and slow[0] == '':
		slow = ['Uh-oh, too long']
	if len(wrong) == 1 and wrong[0] == '':
		wrong = ['That doesn\'t look right. Sorry']
	if len(right) == 1 and right[0] == '':
		right = ['Good job. Try the next one']

	TIME_LIMIT = 2.0
	THRESHOLD  = 50

	print 'Meta meta meta... Lets play a game'
	time.sleep(.5)

	cnt = 0
	used = []

	url = 'http://127.0.0.1/{img}'
	imgs = [
	 'img_001.JPG',
	 'img_002.JPG',
	 'img_003.JPG',
	 'img_004.JPG',
	 'img_005.JPG',
	 'img_006.JPG',
	 'img_007.JPG',
	 'img_008.JPG',
	 'img_009.JPG',
	 'img_010.JPG',
	 'img_011.JPG',
	 'img_012.JPG',
	 'img_013.JPG',
	 'img_014.JPG',
	 'img_015.JPG',
	 'img_016.JPG',
	 'img_017.JPG',
	 'img_018.JPG',
	 'img_019.JPG',
	 'img_020.JPG',
	 'img_021.JPG',
	 'img_022.JPG',
	 'img_023.JPG',
	 'img_024.JPG',
	 'img_025.JPG',
	 'img_026.JPG',
	 'img_027.JPG',
	 'img_031.JPG',
	 'img_032.JPG',
	 'img_033.JPG',
	 'img_034.JPG',
	 'img_035.JPG',
	 'img_036.JPG',
	 'img_037.JPG',
	 'img_038.JPG',
	 'img_039.JPG']

	tags = ['LightSource', 'YResolution', 'ResolutionUnit', 'FocalPlaneYResolution', 'Copyright', 'Sharpness', 'Make', 'Flash', 'SceneCaptureType', 'DateTime', 'MeteringMode', 'XResolution', 'ExposureProgram', 'ColorSpace', 'ExifImageWidth', 'DateTimeDigitized', 'DateTimeOriginal', 'Software', 'SubjectDistanceRange', 'WhiteBalance', 'CompressedBitsPerPixel', 'SensingMethod', 'FNumber', 'CustomRendered', 'ApertureValue', 'FocalLength', 'ExposureMode', 'FocalPlaneXResolution', 'ExifOffset', 'ExifImageHeight', 'ISOSpeedRatings', 'Model', 'Orientation', 'ExposureTime', 'MaxApertureValue', 'FlashPixVersion', 'FocalPlaneResolutionUnit', 'ExifVersion']

	while True:
		if len(imgs) == 0:
			imgs = used
			used = []
		img = random.choice(imgs)
		imgs.remove(img)
		used.append(img)
		exif = retrieveExif(Image.open(os.path.join('_imgs', img)))
		key = random.choice(tags)
		s = time.time()
		u = url.format(img=img)
		print '{}: {}'.format(u, key)
		ans = exif[key]
		try:
			inp = sys.stdin.readline().strip()
			if time.time() - s >= TIME_LIMIT:
				print 'Uh-oh, too long'
				sys.exit()
			if inp != ans:
				print 'That doesn\'t look right. Sorry'
				sys.exit()
			else:
				cnt += 1
				if cnt >= THRESHOLD:
					print 'FINE! You win this time. {}'.format(flag)
					sys.exit()
				print 'Good job. Try the next one'
				time.sleep(.5)
		except Exception, e:
			print 'Exception: {}'.format(e)

chal()
