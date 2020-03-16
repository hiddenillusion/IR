#!/usr/bin/env bash

####################################################
# LinuxTriage was created by Glenn P. Edwards Jr.
#	 	https://hiddenillusion.github.io
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

safe_date=`date +%Y-%m-%d_%T_%Z`
outty="process.log"
triage_dir=$dirname/`echo $safe_date | sed s'/:/./g'`

mkdir $triage_dir
cd $triage_dir

echo "[+] Collection Started: `date`"
echo "[+] Collection Started: `date`" >> $outty
echo "======================================================" >> $outty

# bourne shells (sh, bash, zsh, ksh)
# c-shells (csh, tcsh, bcsh)

history_files=(".bash_history"
	".sh_history"
	".tsch_history"
	".tcsh_history"
	".sqlite_history"
	".mysql_history"
	".vsql_history"
	".lesshst"
	".viminfo"
);

misc_files=("authorized_keys"
	"known_hosts"
	".bashrc"
	".mkshrc"
	".zshrc"
	".bash_logout"
	".bash_login"
	".bash_profile"
	".profile"
	".pam_environment"
);

# Note: some of these won't display
#		all relevant details if user doesn't
#		have proper privileges, e.g. - not run w/ sudo
cmds=("ps auwwx"
	"netstat -tulpan"
	"ps -eaf"
	"ps -eo pid,ppid,start,etime,user,comm,args"
	"pstree -A -a -p"
	"netstat -rn"
	"lsof -n"
	"lsof -w"
	"w"
	"who -a"
	"last -Faix"
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
	"cat /proc/uptime"
	"cat /etc/hosts"
	"cat /etc/os-release"
	"alias"
	"printenv | sort"
	"rpm -qa"
	"dpkg --get-selections"
	"dmesg -T"
);

env_variables=("HISTFILESIZE"
	"HISTSIZE"
	"TERM"
	"SHELL"
	"LD_PRELOAD"
	"LD_LIBRARY_PATH"
	"TMPDIR"
	"BROWSER"
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
	"/etc/sudoers"
	"/etc/fstab"
	"/etc/mtab"
);

list_files=("/etc/profile.d"
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

echo "[-] Printing environment variables"
for ev in "${env_variables[@]}"; do
	echo "------------------------------------------------------" >> $outty
	echo "$ev" >> $outty
	echo "------------------------------------------------------" >> $outty
	$ev &>> $outty
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
