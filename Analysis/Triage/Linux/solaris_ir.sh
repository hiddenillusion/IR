#!/bin/bash

####################################################
# Solaris 10 Triage script.
# Original script created by Glenn P. Edwards Jr.
# Modified by Ian Ahl
# Based on research from Matt Pepe
# Date: 12/04/2014
# (While at FireEye)
####################################################

# Some of these commands need root perms 

Date=`date +%m-%d-%Y_%T`
dirname=`hostname`
if [ ! -d dirname ]; then
	mkdir $dirname
fi

cd $dirname
outty="$Date.txt"

echo "[+] Collection Started: $Date"
echo "[+] Collection Started: $Date" >> $outty
echo "======================================================" >> $outty

# Get all bash history files before they're modified too much

find / -name ".bash_history" | while read f; do cat $f > `echo $f | sed 's/\//_/g'`.txt;done

cmds=("ps -eaf"
	"w"
	"who"
	"isainfo -vk"
	"prtconf -v"
	"prtdiag -v"
	"ndd -get /dev/ip ip_forwarding"
	"ndd -get /dev/ip ip6_forwarding"
	"netstat -an"
	"netstat -arn"
	"arp -an"
	"rpcinfo -p 127.0.0.1"
	"ps -efLZ"
	"ptree -ac"
	"cat /var/adm/messages"
	"modinfo -w"
	"showrev -p"
	"df -k"
	"du -a"
	"last"
	"hostname"
	"id"
	"uname -a"
	"hostid"
	"ifconfig -a"
	"netstat -rn"
	"cat /etc/group"
	"mount"
	"crontab -l"
	);

cmds2=("cat /etc/passwd"
	"cat /var/log/authlog"
	"cat /var/log/apache2/access.log"
	"cat /var/log/apache2/error.log"
	"cat /etc/syslog.conf"
	"cat /etc/inetd.conf"
	);

echo "[-] Running command set 1"
# Commands that are having their output put into the main file
for c in "${cmds[@]}"; do
	echo "------------------------------------------------------" >> $outty
	echo "$c" >> $outty
	echo "------------------------------------------------------" >> $outty
	$c >> $outty
done

echo "[-] Running command set 2"
# Commands that are having their output put into their own file
for c2 in "${cmds2[@]}"; do
	echo "------------------------------------------------------" >> $outty
	echo "$c2" >> $outty
	echo "------------------------------------------------------" >> $outty
	output=`echo $c2 | sed s'/[ \/]/_/g'`.txt
	$c2 1> $output 2>>$outty
done

echo "======================================================" >> $outty
echo "[+] Collection Finished: $Date"
echo "[+] Collection Finished: $Date" >> $outty