#!/usr/bin/python

import os
import sys

msg=chr(int(sys.argv[1]))*1024*1048576

f = open('file.txt', 'w')
f.write(msg)
f.close()
