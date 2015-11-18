import os, string
for i in range(1, 29):
    os.system('exiftool -xmp:dateTimeOriginal="2015:03:%s" release/images/julius_%s.gif' % (string.rjust(str(i), 2, "0"), string.rjust(str(i), 2, "0")))
    os.system('touch -t 201503{0}0000 -mt 201503{0}0000 release/images/julius_{0}.gif'.format(string.rjust(str(i), 2, "0")))

os.system("rm release/images/*original")

from os import listdir
from os.path import isfile, join
import hashlib
mypath = "/Users/breadchris/Documents/Programming/ISIS/HSF-Prelims/Disk-OS-Forensics/Ides_of_March/release/images"

onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

for f in onlyfiles:
    with open("release/images/" +f, "rb") as fin:
        h = md5_for_file(fin)
        os.system("mv release/images/%s release/images/%s" % (f, h))

