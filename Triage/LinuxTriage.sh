#!/bin/bash

####################################################
# LinuxTriage was created by Glenn P. Edwards Jr.
#	 	http://hiddenillusion.blogspot.com
# 				@hiddenillusion
# Date: 2013-11-19
# (While at FireEye)
####################################################

### Usage ###
# 1 - just place it on the system (possibly need to dos2unix it depending on how it's pulled down)
# 2 - chmod +x LinuxTriage.sh
# 3 - sudo ./LinuxTriage.sh

# While not all commands require root, just easier
if [ "$EUID" -ne 0 ]; then
	echo "[!] Please run as root"
  exit 1
fi

dirname=`hostname`_triage

if [ ! -d dirname ]; then
	mkdir $dirname
fi

Date=`date +%m-%d-%Y_%T`
outty="process.log"
triage_dir=$dirname/$Date

mkdir $triage_dir
cd $triage_dir

echo "[+] Collection Started: $Date"
echo "[+] Collection Started: $Date" >> $outty
echo "======================================================" >> $outty

history_files=(".bash_history"
	".sh_history"
	".tsch_history"
	".tcsh_history"
	".sqlite_history"
	".lesshst"
	".viminfo"
);

misc_files=("authorized_keys"
	"known_hosts"
	".bashrc"
	".bash_logout"
);

cmds=("ps -eaf"
	"ps auwwx"
	"netstat -rn"
	"netstat -tulpan"
	"lsof -n"
	"lsof -w"
	"w"
	"who -a"
	"last -a -i"
	"lastlog"
	"lastb"
	"df -k"
	"df -HaT"
	"lsmod"
	"ifconfig -a"
	"mount"
	"crontab -l"
	"fdisk -l"
	"lsblk"
	"free"
	"hostname"
	"id"
	"uname"
	"uname -a"
	"hostid"	
	"cat /proc/version"
	"cat /proc/meminfo"
	"cat /etc/hosts"
	"cat /etc/os-release"
	"rpm -qa"
	"dpkg --get-selections"
);

read_contents=("/var/log/sudo"
	"/var/log/secure"
	"/var/log/auth.log"
	"/var/log/audit/audit.log"
	"/var/log/messages"
	"/var/log/apache2/access.log"
	"/var/log/apache2/error.log"
	"/etc/passwd"
	"/etc/group"
	"/etc/syslog.conf"
	"/etc/inetd.conf"
	"/etc/audit/auditd.conf"
	"/etc/ssh/sshd_config"
	"/etc/fstab"
	"/etc/mtab"
);

echo "[-] Getting history files"
# Get all *history*-ish files before they're modified too much
for hf in "${history_files[@]}"; do
	echo "[-] Looking for $hf" >> $outty
	find / -name $hf | while read f; do cat $f > `echo $f | sed 's/\//_/g'`.txt;done
done

echo "[-] Running basic triage commands"
# Commands that are having their output put into the main files
for c in "${cmds[@]}"; do
	echo "------------------------------------------------------" >> $outty
	echo "$c" >> $outty
	echo "------------------------------------------------------" >> $outty
	$c &>> $outty
done

echo "[-] Running read content commands"
# Commands that are having their output put into their own file
for rc in "${read_contents[@]}"; do
	echo "[-] Looking for $rc" >> $outty
	if [ -f $rc ]; then
		output=`echo $rc | sed s'/[ \/]/_/g'`
		cat $rc 1> $output 2>>$outty
	fi
done

echo "[-] Getting misc. files of interest"
for mf in "${misc_files[@]}"; do
	echo "[-] Looking for $mf" >> $outty
	find / -name $mf | while read f; do cat $f > `echo $f | sed 's/\//_/g'`.txt;done
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