#!/bin/bash

argument1=$1
for i in `seq 0 10`;
	do
        gzip -c $argument1 > $argument1.gz
        #bzip2 -k $argument1
	#lzma --keep $argument1
        #lzip --keep $argument1
        #lzop --keep $argument1
        #xz --keep $argument1
	mv $argument1.gz toto$i.gz
        #xz --keep --format=lzma file$i
        #rzip -k -9 file$i
	argument1=toto$i.gz
    done 
  
exit 0
