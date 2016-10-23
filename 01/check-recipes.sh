#!/bin/bash

#######################################################
# author:	Giacomo Lanciano
# date:		23/10/2016
#
# descr:	
#######################################################

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC="$DIR/recipes.txt"
REC="$DIR/recipes"
DEST="$DIR/recipes-missing.txt"
URL_PREFIX_LENGTH=34
TIMEOUT="1"

i=0
while IFS='' read -r line || [[ -n "$line" ]]; do
    name=$(echo ${line:URL_PREFIX_LENGTH} | tr -d '\r')
    
    if [ ! -f "$REC/$name.html" ]; then
        printf "%s\n" $(echo ${line} | tr -d '\r')
        printf "%s\n" $(echo ${line} | tr -d '\r') >> $DEST
        ((i += 1))
    fi
done < $SRC

printf "\n%i recipes not downloaded.\n" $i

exit 0