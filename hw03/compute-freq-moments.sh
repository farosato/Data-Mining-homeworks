#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ $# -lt 1 ]; then
	SRC="$DIR/access_log_prep.txt"
else
    SRC="$1"
fi

DEST="$DIR/`basename "$SRC" .txt`_frequencies.txt"

# compute items frequencies
sort $SRC | uniq -c > $DEST

# compute 0-th frequency moment
echo F0: $(wc -l < $DEST)

# compute 2-nd frequency moment
python $DIR/compute_f2.py $DEST

exit 0
