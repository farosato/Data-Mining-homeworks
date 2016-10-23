#!/bin/bash

#######################################################
# author:	Giacomo Lanciano
# date:		23/10/2016
#
# descr:	
#######################################################

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC="$DIR/recipes-names.txt"
DEST="$DIR/recipes_old"
TIMEOUT="1"

i=0
while IFS='' read -r line || [[ -n "$line" ]]; do
    name=$(echo ${line} | tr -d '\r')
    
    if [ ! -f "$DEST/$name.html" ]; then
        printf "%s\n" $name
        ((i += 1))
    fi
    #if [ $i = 10 ]; then
    #    exit 1
    #fi
done < $SRC

printf "\n%i recipes not downloaded.\n" $i

exit 0