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
	#if magic_number != "BZ":
		#out=filename+ " is not a bzip2 file."
		#return out 
	out=out+"MAGIC NUMBER: 0x"+binascii.hexlify(m[0:2])+'\n'
	out=out+"VERSION: 0x"+binascii.hexlify(m[2])+'\n'
	out=out+"BLOCK SIZE: 0x"+binascii.hexlify(m[3])+'\n'
	out=out+"COMPRESSED_MAGIC: 0x"+binascii.hexlify(m[4:10])+'\n'
	out=out+"CHECKSUM: 0x"+binascii.hexlify(m[10:14])+'\n'
	out=out+"RANDOMISED: 0x"+binascii.hexlify(m[14])+'\n'
	out=out+"ORIGPTR: 0x"+binascii.hexlify(m[15:18])+'\n'
	
	m.close()
	f.close()	
	return  out



def main(argv):
	for arg in sys.argv[1:]:
		print decode(arg)

if __name__ == "__main__":
   main(sys.argv[1:])
