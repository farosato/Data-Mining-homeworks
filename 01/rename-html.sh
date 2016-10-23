#!/bin/bash

#######################################################
# author:	Giacomo Lanciano
# date:		23/10/2016
#
# descr:	
#######################################################

if [ $# -ne 1 ]; then
	echo "usage: $ rename-html dir_name" 1>&2
	exit 1
fi

for file in $(find $1 -type f ! -name "*.*"); do 
	mv "$file" $file".html" 
done
