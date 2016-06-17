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
	stream = m.size() ;
	#out = binascii.hexlify(m);
	
	out=out+"MAGIC NUMBER: 0x"+binascii.hexlify(m[0:6])+'\n'
	out=out+"VERSION: 0x"+binascii.hexlify(m[6:8])+'\n'
	out=out+"CRC32: 0x"+binascii.hexlify(m[8:12])+'\n'
	out=out+"OTHER: 0x"+binascii.hexlify(m[12:])+'\n'

	out=out+"CRC32 FOOTER: 0x"+binascii.hexlify(m[stream-12:stream-8])+'\n'
	out=out+"BACKWARD SIZE: 0x"+binascii.hexlify(m[stream-8:stream-4])+'\n'
	out=out+"FLAGS: 0x"+binascii.hexlify(m[stream-4:stream-2])+'\n'
	out=out+"FOOTER MAGIC NUMBER: 0x"+binascii.hexlify(m[stream-2:])+'\n'
	m.close()
	f.close()	
	return  out



def main(argv):
	for arg in sys.argv[1:]:
		print decode(arg)

if __name__ == "__main__":
   main(sys.argv[1:])
