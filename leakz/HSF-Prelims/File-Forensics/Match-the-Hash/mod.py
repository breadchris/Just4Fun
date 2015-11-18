import os, string
"""
for i in range(1, 29):
    os.system('exiftool -xmp:dateTimeOriginal="2015:03:%s" julius_%s.gif' % (string.rjust(str(i), 2, "0"), string.rjust(str(i), 2, "0")))
"""

from os import listdir
from os.path import isfile, join
import hashlib
mypath = "/Users/breadchris/Documents/Programming/ISIS/HSF-Prelims/Disk-OS-Forensics/Match-the-Hash/images/"
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

l = []
for n,f in enumerate(onlyfiles):
    with open("images/" +f, "rb") as fin:
        h = md5_for_file(fin)
        if h in l:
            print h
        l.append(h)
        ext = f.split(".")[1]
        #os.system("mv images/%s.%s images/%d.%s" % (h, ext, n, ext))

