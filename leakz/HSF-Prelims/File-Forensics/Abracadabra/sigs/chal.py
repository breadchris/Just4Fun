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

import re
import sys
import json
import time
import random

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

@timeout(30)
def chal():
	sigs = json.loads(open('sigs.out', 'r').read())
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
	THRESHOLD  = 25

	print 'You think you know file signatures? I\'m really good at file signatures - lets see if you know more than me.'
	print 'For each file description, give me the signature. But you\'ll be timed, so hurry up >;D'
	time.sleep(.5)

	cnt = 0
	used = []

	exts = sigs.keys()

	while True:
		ext = random.choice(exts)
		# while ext in used:
		#	ext = random.choice(exts)
		exts.remove(ext)
		used.append(ext)
		s = time.time()
		print ext
		ans = sigs[ext]
		try:
			inp = sys.stdin.readline().strip()
			if time.time() - s >= TIME_LIMIT:
				print random.choice(slow)
				sys.exit()
			if inp != ans:
				print random.choice(wrong)
				sys.exit()
			else:
				cnt += 1
				if cnt >= THRESHOLD:
					print 'You\'re quick. {}'.format(flag)
					sys.exit()
				print random.choice(right)
				time.sleep(.5)
		except Exception, e:
			print 'Exception: {}'.format(e)

chal()
