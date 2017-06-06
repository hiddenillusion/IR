#!/bin/bash
# created by Glenn P. Edwards Jr.
#      http://hiddenillusion.blogspot.com
#               @hiddenillusion
#	(while at FireEye)
# Version 0.0.3
# Date: 09-24-2014

# list of keywords to search on
keywords=$1

# directory of logs to recursively search through
logdir=$2

# directory to save log results
outdir=$3

logfiles=(`find $logdir -type f -print`)
logtotal="${#logfiles[@]}"
keywordTotal="${#keywords[@]}"

if [[ $1 == "" ]]; then
	echo "Usage : $0 [keyword list] [log directory] [output directory]"
	exit 1
fi

consolidate() {
	echo "[-] Consolidating tmp files"
	if ! [[ `lsof | grep $safe_query &> /dev/null` ]]; then                
		rm "$forked_pids"
		# to handle spaces in file paths
		OFS="$IFS"
		IFS=$'\n'
		tmp_logfiles=(`find $tmp_outdir -type f -print`)
		tmp_logtotal="${#tmp_logfiles[@]}"
		final_out="$outdir/$safe_query"
		echo "[.] cat'ing '$tmp_logtotal' files"
		echo "[.] saving to: $final_out"
		for tmp in "${tmp_logfiles[@]}"; do
			cat "$tmp" >> "$final_out"
		done

		IFS=$OFS
		wait
		echo "[.] deleting tmp files in: $tmp_outdir"
		rm -rf "$tmp_outdir"
	fi
}

looper() {
	tmp_file=`mktemp`
	while [ -f $tmp_file ]; do
		rm $tmp_file
		cat "$forked_pids" | grep -v "^$" | while read p; do
			ps -p $p > /dev/null
			if [ $? -eq 0 ]; then
				touch $tmp_file
				echo "[-] PID '$p' is still active"
				sleep 2s			
			else
				#echo "[i] PID '$p' not active, deleting"
				sed -i '/$p/d' "$forked_pids"	
			fi
		done

	done
	
	consolidate
}

qry() {
	tmp_file="$query_`date +%s%N`"
	tmp_full_path="$tmp_outdir/$tmp_file"
	echo "[$count/$logtotal] Saving tmp results to: $tmp_full_path"
	# this isn't doing case insensitive FYI
        grep -H "$query" "$file" >> "$tmp_full_path" & pid2=$!
	echo $pid2 >> "$forked_pids"
	# fgrep helps if query terms are IP's
}

tic=$(date +%s)

cat "$keywords" | while read query; do
	count=1
        echo "[+] Querying: '$query'"
        echo -e "[-] Time....: `date +"%D %T"`"
	# to handle spaces in file paths
	OFS="$IFS"
	IFS=$'\n'
	for file in "${logfiles[@]}"; do
		out_dir_last_chr=$(echo $outdir | awk '{print substr($0,length($0),1)}')
		if [ $out_dir_last_chr == "/" ]; then
			outdir=$(echo $outdir | sed 's/.$//')
		fi
	
		# replace any special characters not allowed in a filename for Windows (http://support.microsoft.com/kb/177506) & spaces since they cause issues with paths
		safe_query=$(echo $query | sed 's/[\\\/:*?\"<>\| ]/_/g')
		outty="$outdir/$safe_query.txt"
		tmp_outdir="$outdir/tmp/$safe_query"
		forked_pids="$tmp_outdir/forked_pids"
		if [ ! -d "$outdir/$safe_query" ]; then
			mkdir -p "$tmp_outdir"
		fi

		#echo -en "\r[$count/$logtotal]"
		qry $query $file
		while [ `jobs | wc -l` -ge 30 ]; do
			sleep 3s
		done
		((count++))
	done

	IFS=$OFS
	looper

done

# clean up, just in case
rm -rvf "$outdir/tmp"

# End the analysis timer
toc=$(date +%s)
total=$(expr $toc - $tic)
min=$(expr $total / 60)
sec=$(expr $total % 60)
echo "Processing took :" $min"m":$sec"s"

