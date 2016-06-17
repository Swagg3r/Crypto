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
	f = open(filename, 'r+b')
	m = mmap.mmap(f.fileno(), 0, access=mmap.PROT_WRITE)
	stream = m.size() ;
	new=m[0:stream-8]
	print new
	new=new+"\05\05\0\0\0\0\0\0"
	print new
	
	out=out+"MAGIC NUMBER: 0x"+binascii.hexlify(new[0:4])+'\n'
	out=out+"VERSION: 0x"+binascii.hexlify(new[4])+'\n'
	out=out+"DICTIONARY SIZE: 0x"+binascii.hexlify(new[5])+'\n'
	out=out+"COMPRESSED_MAGIC: 0x"+binascii.hexlify(new[5:stream-10])+'\n'
	out=out+"CRC: 0x"+binascii.hexlify(new[stream-20:stream-16])+'\n'
	out=out+"DATA SIZE: 0x"+binascii.hexlify(new[stream-16:stream-8:])+'\n'
	out=out+"MEMBER SIZE: 0x"+binascii.hexlify(new[stream-8:])+'\n'
	


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
	
