import pyexiv2
import random

random_key = lambda n: ''.join([chr(random.randint(0,255)) for i in xrange(n)])

def encode_into_image(img, msg, r_img):
	'''
	description - given 2 images and a msg, hides msg into the images
	@img,r_img - two filenames of images
	@msg - message to encode across files
	'''
	rkey = random_key(len(msg))
	comment = ''.join([chr(ord(msg[i]) ^ ord(rkey[i])) for i in range(len(msg))])
	metadata = pyexiv2.ImageMetadata(img)
	metadata.read()
	metadata['Exif.Photo.UserComment'] = pyexiv2.ExifTag('Exif.Photo.UserComment',comment.encode('hex').encode('base64'))
	metadata.write()

	metadata = pyexiv2.ImageMetadata(r_img)
	metadata.read()
	metadata['Exif.Photo.UserComment'] = pyexiv2.ExifTag('Exif.Photo.UserComment',rkey.encode('hex').encode('base64'))
	metadata.write()

	# DEBUG
	# print msg.encode('hex')
	# print rkey.encode('hex')
	# print comment.encode('hex')
	# for ek in metadata.exif_keys:
	# 	print ek,':', metadata[ek].raw_value

def decode_from_image(img, r_img):
	'''
	description - given 2 images, recovers hidden msg using xor
	@img,r_img - two filenames of images containing message
	@returns output message from xor of data
	'''
	metadata = pyexiv2.ImageMetadata(r_img)
	metadata.read()
	rkey = metadata['Exif.Photo.UserComment'].raw_value.decode('base64').decode('hex')

	metadata = pyexiv2.ImageMetadata(img)
	metadata.read()
	comment = metadata['Exif.Photo.UserComment'].raw_value.decode('base64').decode('hex')

	msg = ''.join([chr(ord(comment[i]) ^ ord(rkey[i])) for i in range(len(rkey))])

	# DEBUG
	# print [chr(ord(c)) for c in comment]
	# print [chr(ord(c)) for c in rkey]
	# print msg

	return msg

import os
def print_exif(sub_dir):
	for filename in os.listdir(sub_dir):
		img = os.path.join(sub_dir, filename)
		metadata = pyexiv2.ImageMetadata(img)
		metadata.read()
		for ek in metadata.exif_keys:
	 		print ek,':', metadata[ek].raw_value
			# del metadata[ek]
	 	# metadata.write()

# print_exif('recv')
# print_exif('send')

def create_files(sub_dir, l_list):
	'''
	helper function to encode data into images
	'''
	files = os.listdir(sub_dir)
	i = j = 0
	while i < len(files):
		img1 = os.path.join(sub_dir, files[i])
		img2 = os.path.join(sub_dir, files[i+1])
		encode_into_image(img1, l_list[j], img2)
		i+=2
		j+=1

def convo_encode(c_file, recv_dir='recv', send_dir='send'):
	'''
	description - takes convo file and hides in images
	@c_file - conversation file containing data sent and recevied
	@recv_dir, send_dir - path to directories containing images 
	'''
	recv_list = []
	send_list = []

	with open(c_file, 'r') as f:
		lines = f.readlines()

	for line in lines:
		if line[0] == '\t':
			recv_list.append(line.lstrip().rstrip())
		else:
			send_list.append(line.rstrip())

	# print send_list
	# print recv_list

	create_files(recv_dir, recv_list)
	create_files(send_dir, send_list)

def convo_decode(recv_dir='recv', send_dir='send'):
	'''
	description - takes images dirs and recovers convo
	@recv_dir, send_dir - path to directories containing images 
	'''
	r_files = os.listdir(recv_dir)
	s_files = os.listdir(send_dir)
	i = 0
	while i < len(r_files):
		img1 = os.path.join(send_dir, s_files[i])
		img2 = os.path.join(send_dir, s_files[i+1])
		print decode_from_image(img1, img2)

		img1 = os.path.join(recv_dir, r_files[i])
		img2 = os.path.join(recv_dir, r_files[i+1])
		print '\t', decode_from_image(img1, img2)
		i+=2

convo_encode('conversation.txt')

convo_decode()