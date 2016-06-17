#!/usr/bin/python

import binascii
import os
import sys
from sys import argv
import operator
import mmap


def decode(filename):
	new=""
	out=""
	if os.stat(filename).st_size==0:
		out=filename+" is empty." 
		return out
	f = open(filename, 'r')
	m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
	new=m[0:3]
	print new
	new=new+"9"
	print new
	new=new+m[4:]
	
	out=out+"MAGIC NUMBER: 0x"+binascii.hexlify(new[0:2])+'\n'
	out=out+"VERSION: 0x"+binascii.hexlify(new[2])+'\n'
	out=out+"BLOCK SIZE: 0x"+binascii.hexlify(new[3])+'\n'
	out=out+"COMPRESSED_MAGIC: 0x"+binascii.hexlify(new[4:10])+'\n'
	out=out+"CHECKSUM: 0x"+binascii.hexlify(new[10:14])+'\n'
	out=out+"RANDOMISED: 0x"+binascii.hexlify(new[14])+'\n'
	out=out+"ORIGPTR: 0x"+binascii.hexlify(new[15:18])+'\n'


	f_out=open(filename,"w+a")
	f_out.write(new)
	f_out.close()
	m.close()
	f.close()	
	return out



def main(argv):
	for arg in sys.argv[1:]:
		print decode(arg)

if __name__ == "__main__":
   main(sys.argv[1:])
	
