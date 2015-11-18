#!/usr/bin/env python

import sys
import json
import time
import socket

sigs = json.loads(open('sigs.out', 'r').read())

IP = '127.0.0.1'
PORT = 45454

s = socket.socket()
s.connect((IP, PORT))

s.recv(1024)

tmp = ''
while 'flag' not in tmp:
	tmp = s.recv(1024).strip()
	print '[!] Ext: {}'.format(tmp)
	ans = sigs[tmp]
	print '[+] Ans: {}'.format(ans)
	s.send('{}\n'.format(ans))
	tmp = s.recv(1024).strip()
	print '[X] Junk: {}'.format(tmp)
print tmp
