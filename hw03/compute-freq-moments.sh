#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ $# -lt 1 ]; then
	SRC="$DIR/access_log_prep.txt"
else
    SRC="$1"
fi

FREQ="$DIR/`basename "$SRC" .txt`_frequencies.txt"

# compute items frequencies
sort $SRC | uniq -c > $FREQ

# compute 0-th frequency moment
echo F0: $(wc -l < $FREQ)

# compute 2-nd frequency moment
python $DIR/compute_fk.py 2 $FREQ

exit 0
