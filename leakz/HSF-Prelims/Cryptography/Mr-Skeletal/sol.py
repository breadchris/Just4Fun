print '|'.join([''.join(['.' if len(el) == 2 else '-' for el in t[1:-1].split('td')]) for t in open('morse.txt', 'r').read().strip().split(' ')])

'''
m = open('morse.txt', 'r').read().strip().split(' ')

o = []
for t in m:
	tmp = t[1:-1].split('td')
	w = []
	for el in tmp:
		if len(el) == 2: w.append('.')
		elif len(el) == 4: w.append('-')
	o.append(''.join(w))
	# o.append(''.join(['.' if len(el) == 2 else '-' for el in t[1:-1].split('td')]))
print '|'.join(o)
'''
