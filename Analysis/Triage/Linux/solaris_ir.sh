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
output_file="collection_$Date.txt"
errors_file="errors_$output_file"

echo "[+] Collection Started: $Date"
echo "[+] Collection Started: $Date" >> $output_file
echo "======================================================" >> $output_file

# Get all bash history files before they're modified too much
#   This will catch most shells (.bash_history, .sh_history, .tsch_history etc.) as well as some applications (e.g. .mysql_history)
find / \( -type d -name export -prune \) -o \( -type d -name 'proc' -prune \) -o \( -type d -name 'oa' -prune \) -o \( -type d -name 'od' -prune \) -o -name *_history -print | while read f; do cat $f > `echo $f |
 sed 's/\//_/g'`.txt;done

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
  "uname -a"
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
  echo "------------------------------------------------------" >> $output_file
  echo "$c" >> $output_file
  echo "------------------------------------------------------" >> $output_file
  $c >> $output_file 2>>$errors_file
done

# Commands that are having their output put into their own file
echo '[-] Grabbing general files of interest'
for gf in "${gen_files[@]}"; do
  echo "------------------------------------------------------" >> $output_file
  echo "Attempting to grab: $gf" >> $output_file
  echo "------------------------------------------------------" >> $output_file
  output=`echo $gf | sed s'/[ \/]/_/g'`.txt
  cat $gf 1> $output 2>>$errors_file
done

# Determine where we're looking
if [ -d /var/adm/ ]; then
  DIR="/var/adm/"
else
  DIR="/var/log/"
fi

echo "[-] Grabbing files of interest from: $DIR"
for lf in "${log_files[@]}"; do
  echo "------------------------------------------------------" >> $output_file
  echo "$DIR$lf" >> $output_file
  echo "------------------------------------------------------" >> $output_file
  cp -f --parents $DIR$lf* . 2>>$errors_file
done

for ld in "${log_dirs[@]}"; do
  echo "------------------------------------------------------" >> $output_file
  echo "$DIR$ld" >> $output_file
  echo "------------------------------------------------------" >> $output_file
  cp -rf --parents $DIR$ld . 2>>$errors_file
done

echo "[-] Generating file listing"
find / \( -type d -name 'export' -print \) -o \( -type d -name 'oa' -prune \) -o \( -type d -name 'od' -prune \) -o \( -type d -name 'proc' -prune \) -o -print 2>>$errors_file | xargs stat -c "%n,%F,%s,%A,%u,%U,%g,%G,%h,%m,%i,%W,%X,%Y,%Z" >> file_listing.csv

echo "======================================================" >> $output_file
Date=`date +%m-%d-%Y_%T`
echo "[+] Collection Finished: $Date"
echo "[+] Collection Finished: $Date" >> $output_file
