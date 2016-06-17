#!/bin/bash
for i in {10..1000000..1}
do
	dd if=/dev/zero bs=258 count=$i 2> /dev/null | gzip -9 -n -f > bomb.zip
	gzip -l bomb.zip | sed '1d' | gawk '{}{print $2/$1}'
done

