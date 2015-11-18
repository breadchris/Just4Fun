#!/usr/bin/env python

import os
import sys
import socket

from PIL import Image
from PIL.ExifTags import TAGS

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

IP = '127.0.0.1'
PORT = 45454

s = socket.socket()
s.connect((IP, PORT))

print s.recv(1024)

tmp = ''
cnt = 1
while 'flag' not in tmp:
	tmp = s.recv(1024).strip()
	print '[{}] Img: {}'.format(cnt, tmp)
	cnt += 1
	img, tag = tmp.split(': ')
	img = img.replace('http://127.0.0.1/', '')
	exif = retrieveExif(Image.open(os.path.join('_imgs', img)))
	ans = exif[tag]
	print '[+] Ans: {}'.format(ans)
	s.send('{}\n'.format(ans))
	tmp = s.recv(1024).strip()
	print '[X] Junk: {}'.format(tmp)
print tmp
