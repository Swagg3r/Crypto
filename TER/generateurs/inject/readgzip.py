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
	if magic_number != "1f8b":
		out=filename+ " is not a gzip file."
		return out 
	out=out+"MAGIC NUMBER: 0x"+binascii.hexlify(m[0:2])+'\n'
	out=out+"Compression type: 0x"+binascii.hexlify(m[2])+'\n'
	out=out+"FLAG: 0x"+binascii.hexlify(m[3])+'\n'
	flag=int(m[3].encode('hex'),16)
	out=out+"UNIX TIMESTAMPS: 0x"+binascii.hexlify(m[4:8])+'\n'
	out=out+"EXTRA: 0x"+binascii.hexlify(m[8])+'\n'
	out=out+"OS: 0x"+binascii.hexlify(m[9])+'\n'

	pos=10
	if (flag & 2) != 0:
        	out=out+"OPTION1: 0x"+binascii.hexlify(m[pos:pos+2])+'\n'
        	pos=pos+2

	if (flag & 4) != 0:
       		out=out+"OPTION2: 0x"+binascii.hexlify(m[pos:pos+2])+'\n'
        	pos=pos+2

	if (flag & 8) !=0:
		name=""
       		current=int(m[pos].encode('hex'),16)
		while current!=0:
			name=name+m[pos]
			pos=pos+1
			current=int(m[pos].encode('hex'),16)
		out=out+"NAME: "+name+'\n'

	if (flag & 16) !=0:
 		comment=""
        	current=int(m[pos].encode('hex'),16)
        	while current!=0:
                	comment=comment+m[pos]
                	pos=pos+1
                	current=int(m[pos].encode('hex'),16)
        	out=out+"COMMENT:"+comment+'\n'

	if (flag & 32) !=0:
        	out=out+"ENCRYPTION HEADER: 0x"+ m[pos:pos+12]+'\n'
        	pos=pos+12

	s=m.size()
	out=out+"PAYLOAD: 0x"+binascii.hexlify(m[pos:s-8]) +'\n'
	out=out+"CRC32: 0x"+binascii.hexlify(m[s-8:s-4])+'\n'
	out=out+"SIZE: 0x"+binascii.hexlify(m[s-4:])
	m.close()
	f.close()
	return  out



def main(argv):
	for arg in sys.argv[1:]:
		print decode(arg)

if __name__ == "__main__":
   main(sys.argv[1:])
