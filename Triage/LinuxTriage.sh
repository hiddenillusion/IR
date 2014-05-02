#!/bin/bash

####################################################
# LinuxTriage was created by Glenn P. Edwards Jr.
#	 	http://hiddenillusion.blogspot.com
# 				@hiddenillusion
# Version 0.1 
# Date: 11/19/2013
# (While at FireEye)
####################################################

# Some of these commands obviously need root perms #

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
	"ps aux"
	"lsof -n"
	"lsof -w"
	"w"
	"who"
	"last -a -i"
	"lastlog"
	"df -k"
	"df -HaT"
	"lsmod"
	"hostname"
	"id"
	"uname"
	"uname -a"
	"hostid"
	"ifconfig -a"
	"netstat -rn"
	"cat /etc/group"
	"mount"
	"crontab -l"
	"fdisk -l"
	"cat /proc/version"
	"cat /etc/hosts"
	"cat /var/log/messages"
	"cat /var/log/secure"
	"cat /var/log/sudo"
	"rpm -qa"
	"lastb"
	);

cmds2=("cat /etc/passwd"
	"cat /var/log/auth.log"
	"cat /var/log/apache2/access.log"
	"cat /var/log/apache2/error.log"
	"cat /etc/syslog.conf"
	"dpkg --get-selections"
	"cat /etc/inetd.conf"
	);

echo "[-] Running command set 1"
# Commands that are having their output put into the main file
for c in "${cmds[@]}"; do
	echo "------------------------------------------------------" >> $outty
	echo "$c" >> $outty
	echo "------------------------------------------------------" >> $outty
	$c &>> $outty
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

# Get some specific information about connected disks
echo "[-] Grabbing some disk information"
echo "------------------------------------------------------" >> $outty
echo "hdparm -I" >> $outty
echo "------------------------------------------------------" >> $outty
fdisk -l | grep -v Disk | grep /dev | awk '{print $1}' | while read d; do hdparm -I $d &>> $outty; done

echo "======================================================" >> $outty
echo "[+] Collection Finished: $Date"
echo "[+] Collection Finished: $Date" >> $outty
