#!/usr/bin/python

import binascii
import os
import sys
from sys import argv
import operator
import mmap


def decode(filename):
	out=""
	if os.stat(filename).st_size==0:
		out=filename+" is empty." 
		return out
	f = open(filename, 'r')
	m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
	magic_number=binascii.hexlify(m[0:2])
	stream = m.size() ;
	#out = binascii.hexlify(m);
	
	out=out+"MAGIC NUMBER: 0x"+binascii.hexlify(m[0:4])+'\n'
	out=out+"VERSION: 0x"+binascii.hexlify(m[4])+'\n'
	out=out+"DICTIONARY SIZE: 0x"+binascii.hexlify(m[5])+'\n'
	out=out+"COMPRESSED_MAGIC: 0x"+binascii.hexlify(m[5:stream-10])+'\n'
	out=out+"CRC: 0x"+binascii.hexlify(m[stream-20:stream-16])+'\n'
	out=out+"DATA SIZE: 0x"+binascii.hexlify(m[stream-16:stream-8:])+'\n'
	out=out+"MEMBER SIZE: 0x"+binascii.hexlify(m[stream-8:])+'\n'
	
	m.close()
	f.close()	
	return  out



def main(argv):
	for arg in sys.argv[1:]:
		print decode(arg)

if __name__ == "__main__":
   main(sys.argv[1:])
