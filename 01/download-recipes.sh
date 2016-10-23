#!/bin/bash

#######################################################
# author:   Giacomo Lanciano
# date:	    22/10/2016
#
# descr:    
#######################################################

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC="$DIR/recipes.txt"
DEST="$DIR/recipes"
TIMEOUT="1"

# start python script to write urls in SRC

# download pages
while IFS='' read -r line || [[ -n "$line" ]]; do
    wget -t10 --retry-connrefused -np -nH -nd -nc -e robots=off -w $TIMEOUT --waitretry=$TIMEOUT --adjust-extension -P $DEST $(echo ${line} | tr -d '\r')
done < $SRC

exit 0