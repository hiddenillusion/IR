#!/usr/bin/env bash

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

# Change working directory to triage directory
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
  "mount"
  "crontab -l"
);

gen_files=("/etc/passwd"
  "/etc/group"
  "/etc/syslog.conf"
  "/etc/inetd.conf"
);

log_files=("authlog"
  "apache2/access.log"
  "apache2/error.log"
  "lastlog"
  "messages"
  "sulog"
  "wtmp"
  "utmp"
);

log_dirs=("acct"
  "log"
  "sa"
);

# Commands that are having their output put into the main file
echo "[-] Running triage commands"
for c in "${cmds[@]}"; do
  echo "------------------------------------------------------" >> $outty
  echo "$c" >> $outty
  echo "------------------------------------------------------" >> $outty
  $c >> $outty
done

# Commands that are having their output put into their own file
echo '[-] Grabbing general files of interest'
for gf in "${gen_files[@]}"; do
  echo "------------------------------------------------------" >> $outty
  echo "Attempting to grab: $gf" >> $outty
  echo "------------------------------------------------------" >> $outty
  output=`echo $gf | sed s'/[ \/]/_/g'`.txt
  cat $gf 1> $output 2>>$outty
done

# Determine where we're looking
if [ -d /var/adm/ ]; then
  DIR="/var/adm/"
else
  DIR="/var/log/"
fi

echo "[-] Grabbing files of interest from: $DIR"
for lf in "${log_files[@]}"; do
  echo "------------------------------------------------------" >> $outty
  echo "$DIR$lf" >> $outty
  echo "------------------------------------------------------" >> $outty
  cp -f --parents $DIR$lf* . 2>>$outty
  #output=`echo $DIRlf | sed s'/[ \/]/_/g'`.txt
  #cat $DIR$lf 1> $output 2>>$outty
done

for ld in "${log_dirs[@]}"; do
  echo "------------------------------------------------------" >> $outty
  echo "$DIR$ld" >> $outty
  echo "------------------------------------------------------" >> $outty
  cp -rf --parents $DIR$ld . 2>>$outty
done

echo "[-] Generating file listing"
find / 2>>$outty | while read fpath; do stat -c "%n %F %s %A %u %U %g %G %h %m %i %W %X %Y %Z"
"$fpath" >> file_listing.txt; done

echo "======================================================" >> $outty
echo "[+] Collection Finished: $Date"
echo "[+] Collection Finished: $Date" >> $outty
