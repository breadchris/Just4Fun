import glob
import hashlib

def md5(f):
	m = hashlib.md5()
	m.update(open(f, 'r').read())
	return m.hexdigest()
h = {}
for i in glob.glob('./images/*.jpg'):
	m = md5(i)
	if m not in h: h[m] = [i]
	else: h[m].append(i)

for k,v in h.items():
	if len(v) > 1: print k
