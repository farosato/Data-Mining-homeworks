#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
src_file=
src_file_taken=0    # flag to check whether the mandatory argument is taken
save_opt=0          # flag to check whether -s option is taken
clean_opt=0         # flag to check whether -c option is taken


function usage {
	printf "usage: $ ./compute-freq-moments.sh [OPTIONS] file.txt\n\n" 1>&2
	printf "  -c,  --clean   remove temporary files\n" 1>&2
	printf "  -s,  --save    save output to file\n" 1>&2
	printf "  -h,  --help    print this help and exit\n" 1>&2
}


# if mandatory argument is NOT taken, accept options
while [ "$1" != "" ]; do
	case $1 in
		-s | --save )       if (( $src_file_taken )); then
								usage
								exit 1
							fi
							save_opt=1
							;;
		-c | --clean )      if (( $src_file_taken )); then
								usage
								exit 1
							fi
							clean_opt=1
							;;
		-h | --help )       if (( $src_file_taken )); then
								usage
								exit 1
							fi
							usage
							exit 0
							;;
		* )                 if (( $src_file_taken )); then
								usage
								exit 1
							fi
							src_file_taken=1
							src_file="$1"
							;;
	esac
	shift
done

if [[ $src_file == "" || ! $src_file == *.txt ]]; then
	usage
	exit 1
fi

freq_file="$DIR/`basename "$src_file" .txt`_frequencies.txt"
dest_file="$DIR/`basename "$src_file" .txt`_results.txt"

# compute items frequencies
sort $src_file | uniq -c > $freq_file

if (( $save_opt )); then
	# compute 0-th frequency moment
	# (input redirection used to have the only value as output of wc)
	echo F0: $(wc -l < $freq_file) > $dest_file

	# compute 2-nd frequency moment
	python $DIR/compute_fk.py 2 $freq_file >> $dest_file
else
	echo F0: $(wc -l < $freq_file)
	python $DIR/compute_fk.py 2 $freq_file
fi

# delete temp files
if (( $clean_opt )); then
	rm $freq_file
fi

exit 0
