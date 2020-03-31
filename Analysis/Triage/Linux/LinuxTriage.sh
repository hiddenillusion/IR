#!/usr/bin/env bash

####################################################
# LinuxTriage was created by Glenn P. Edwards Jr.
#     https://hiddenillusion.github.io
#         @hiddenillusion
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

initial_dir=`pwd`
evidence_dir=`hostname`

if [ ! -d dirname ]; then
  mkdir $evidence_dir
fi

# Change working directory to triage directory
cd $evidence_dir

safe_date=`date +%Y-%m-%d_%T_%Z`
output_file="process_$safe_date.txt"
error_file="$output_file.errors"

echo "[+] Collection Started: `date`"
echo "[+] Collection Started: `date`" >> $output_file
echo "======================================================" >> $output_file

# bourne shells (sh, bash, zsh, ksh)
# c-shells (csh, tcsh, bcsh)

history_files=(".bash_history"
  ".sh_history"
  ".tsch_history"
  ".psql_history"
  ".sqlite_history"
  ".mysql_history"
  ".vsql_history"
  ".lesshst"
  ".viminfo"
);

var_log=("access.log*" #apache2
  "access_log*" #httpd
  "audit.log*" #audit
  "auth.log*"
  "btmp*"
  "dmesg"
  "dpkg.log*"
  "error.log*" #apache2
  "error_log*" #httpd
  "faillog"
  "history.log*" #apt
  "httpd-error.log*"
  "lastlog"
  "messages*"
  "rpm.log*"
  "secure*"
  "syslog*"
  "sudo*"
  "utmp*"
  "wtmp*"
  "yum.log*"
);

etc=("apache2.conf"
  "auditd.conf"
  "dnsmasq.conf"
  "fstab"
  "group"
  "hosts"
  "httpd.conf"
  "inetd.conf"
  "mtab"
  "my.cnf"
  "passwd"
  "resolv.conf"
  "smb.cnf"
  "sshd_config"
  "sudoers"
  "syslog.conf"
);

misc_files=(
  ".bashrc"
  ".bash_logout"
  ".bash_login"
  ".bash_profile"
  ".mkshrc"
  ".pam_environment"
  ".profile"
  ".zshrc"
  "authorized_keys"
  "known_hosts"
  "ssh_config"
);

# Note: some of these won't display
#    all relevant details if user doesn't
#    have proper privileges, e.g. - not run w/ sudo
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

echo "[-] Getting history files"
# Get all *history*-ish files before they're modified too much
for hf in "${history_files[@]}"; do
  echo "[-] Looking for $hf" >> $output_file
  find /home /root -type f -name $hf -exec cp --parents {} . \; 2>$error_file
done

echo "[-] Running basic triage commands"
# Commands that are having their output put into the main files
for c in "${cmds[@]}"; do
  echo "------------------------------------------------------" >> $output_file
  echo "$c" >> $output_file
  echo "------------------------------------------------------" >> $output_file
  $c &>> $output_file
done

echo "[-] Printing environment variables"
for ev in "${env_variables[@]}"; do
  echo "------------------------------------------------------" >> $output_file
  echo "$ev" >> $output_file
  echo "------------------------------------------------------" >> $output_file
  $ev &>> $output_file
done

if [ "${#etc[@]}" -gt 0 ]; then
  echo "[-] Copying /etc files of interest"
  for e in "${etc[@]}"; do
    echo "[-] Looking for $e" >> $output_file
    find /etc -type f -name $e -exec cp --parents --no-preserve=mode,ownership {} . \; 2>$error_file
  done
fi

if [ "${#var_log[@]}" -gt 0 ]; then
  echo "[-] Copying /var/log files of interest"
  for vl in "${var_log[@]}"; do
    echo "[-] Looking for $vl" >> $output_file
    find /var/log -type f -name $vl -exec cp --parents --no-preserve=mode,ownership {} . \; 2>$error_file
  done
fi

if [ "${#read_contents[@]}" -gt 0 ]; then
  echo "[-] Running read content commands"
  # Commands that are having their output put into their own file
  for rc in "${read_contents[@]}"; do
    echo "[-] Looking for $rc" >> $output_file
    if [ -f $rc ]; then
      output=`echo $rc | sed s'/[ \/]/_/g'`
      cat $rc 1> $output 2>>$error_file
    fi
  done
fi

if [ "${#misc_files[@]}" -gt 0 ]; then
  echo "[-] Copying misc. files of interest"
  for mf in "${misc_files[@]}"; do
    echo "[-] Looking for $mf" >> $output_file
    find /etc /home /root -type f -name $mf -exec cp --parents --no-preserve=mode,ownership {} . \; 2>$error_file
  done
fi

echo "[-] Generating file listing"
echo "------------------------------------------------------" >> $output_file
echo "find / 2>file_listing.errors | xargs stat -c '%n,%F,%s,%A,%u,%U,%g,%G,%h,%m,%i,%W,%X,%Y,%Z' '{}'" >> $output_file
echo "------------------------------------------------------" >> $output_file
find / | xargs stat -c '%n,%F,%s,%A,%u,%U,%g,%G,%h,%m,%i,%W,%X,%Y,%Z' '{}' 2>>file_listing.errors 1>>file_listing.csv

# Get some specific information about connected disks
echo "[-] Grabbing some disk information"
echo "------------------------------------------------------" >> $output_file
echo "hdparm -I" >> $output_file
echo "------------------------------------------------------" >> $output_file
fdisk -l | grep -v Disk | grep /dev | awk '{print $1}' | while read d; do hdparm -I $d &>> $output_file; done

echo "======================================================" >> $output_file
echo "[+] Collection Finished: $Date"
echo "[+] Collection Finished: $Date" >> $output_file

echo "[+] Compressing evidence"
cd "$initial_dir"
tar -czf "$evidence_dir.collection.tar.gz" "$evidence_dir"

echo "[+] Removing collection folder"
rm -rf "$evidence_dir"
