#!/usr/bin/python

import binascii
import os
import sys
from sys import argv
import operator
import mmap
import argparse
from collections import Counter

def check(m):
	magic_number=binascii.hexlify(m[0:2])
	if magic_number != "1f8b":
		print "File is not a gzip."
		exit(2)

def readvfield(m,offset): 
	name=''
	pos=offset
	current=int(m[pos].encode('hex'),16)
        while current!=0:
                name=name+m[pos]
                pos=pos+1
                current=int(m[pos].encode('hex'),16)
	return name

def offset_name(m):
	pos=10
	flag=int(m[3].encode('hex'),16)
        if (flag & 2) != 0:
                pos=pos+2
        if (flag & 4) != 0:
                pos=pos+2
	return pos


def offset_comment(m):
	pos=offset_name(m)
	if (flag & 8) != 0:
		current=int(m[pos].encode('hex'),16)
        	while current!=0:
                	pos=pos+1
                	current=int(m[pos].encode('hex'),16)
	return pos

def offset_payload(m):
	pos=offset_comment(m)
	current=int(m[pos].encode('hex'),16)
        while current!=0:
                pos=pos+1
                current=int(m[pos].encode('hex'),16)
	return pos 


def Most_Common(lst):
	c=Counter(lst)
	return c.most_common(2)[0][0]

def header(m):
	new=''
	new=new+m[0:9]
	flag=int(m[3].encode('hex'),16)
	position=10
	if (flag & 2) != 0:
		new=new+m[position:position+2]
		position=position+2
	if (flag & 4) != 0:
		new=new+m[position:position+2]
		position=position+2
	return new

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('filename', type=str,help="Filename")
	parser.add_argument('-b', '--block', type=int, dest="block",default=258,help="Block size (in bytes)")
	parser.add_argument('-m', type=int, dest="nb_block",default=1,help="Number of blocks")
	parser.add_argument('-t', type=int, dest="pattern",default=0,help="pattern")
	parser.add_argument('-o', '--output', type=str, dest="out")
	parser.add_argument("-c", "--comment", help="Inject string in comment field", dest='comment', action='store_true')
	parser.add_argument("-n", "--name", help="Inject string in name field", dest='name', action='store_true')

	args = parser.parse_args()

	if os.stat(args.filename).st_size == 0 :
		print args.filename+" is empty."
		exit(2)
	f = open(args.filename, 'r')
	m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
	
	check(m)
	new=''
	new=new+header(m)
	flag=int(m[3].encode('hex'),16)
        pos=10
        if (flag & 2) != 0:
                pos=pos+2
        if (flag & 4) != 0:
                pos=pos+2
	if args.name:
		tmp=list(new)
		tmp[3]=chr(ord(tmp[3])|8)
		new=new+"tototototototoo"+chr(0)
	else: 
		if (flag & 8) !=0:
			pos=offset_name(m)
			new=new+readvfield(m,pos)+chr(0)
		
	if args.comment:
		tmp=list(new)
		tmp[3]=chr(ord(tmp[3])|16)
		new=''.join(tmp)
		tmp=list(m)
		if args.pattern:
			print binascii.hexlify(chr(args.pattern))
			new=new+chr(args.pattern)*(args.block*args.nb_block)
		else:
			pattern=Most_Common(tmp)
			print "most common"
			new=new+pattern*(args.block*args.nb_block)
	else:
		if (flag & 16) !=0: 
			pos=offset_comment(m)
			new=new+readvfield(m,pos)+chr(0)

	s=m.size()
	pos=offset_payload(m)
	new=new+m[pos:]
	if args.out:
		f_out=open(args.out,"w+a")
		f_out.write(new)
		f_out.close()
	else:
		print binascii.hexlify(new)
	m.close()
	f.close()
		
