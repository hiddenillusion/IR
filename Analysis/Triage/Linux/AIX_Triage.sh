#!/usr/bin/env bash

####################################################
# LinuxTriage was created by Glenn P. Edwards Jr.
#     https://hiddenillusion.github.io
#          @hiddenillusion
# Date: 2013-11-19
# (While at FireEye/Mandiant)
####################################################

TEST_MODE="false"
START_DIR=`pwd`
EVIDENCE_DIR=`hostname`
EVIDENCE_COLLECTION_FILE="${EVIDENCE_DIR}.collection.tar.gz"
DATE_FMT=`date '+%Y-%m-%d %T %Z'`
SAFE_DATE=`date +%Y-%m-%d_%T_%Z`
OUTPUT_FILE="process_${SAFE_DATE}.txt"
ERROR_FILE="${OUTPUT_FILE}.errors"

# Pre-populated items
COMMANDS_TO_EXECUTE=("ps -ef" "last" "failedlogin" "ifconfig -a" "hostname" "uname -a");
DIRECTORIES_TO_COPY=("/var/adm/" "/var/log/" "/var/spool/cron/");
FILES_TO_READ=();
HISTORY_FILES_TO_ACQUIRE=(".history" ".ash_history" ".bash_history" ".lesshst" ".mysql_history" ".psql_history" ".sh_history" ".sqlite_history" ".tsch_history" ".viminfo" ".vsql_history");
MISC_FILES_TO_ACQUIRE=(".bashrc" ".bash_logout" ".bash_login" ".bash_profile" ".kshrc" ".mkshrc" ".pam_environment" ".profile" ".zshrc" "authorized_keys" "known_hosts" "ssh_config");
SPECIFIC_FILES_TO_ACQUIRE=("/etc/group" "/etc/passwd" "/etc/profile" "/etc/security/failedlogin" "/etc/security/passwd" "/etc/sudoers");

format_main_separator() {
  echo "======================================================" >> ${OUTPUT_FILE}
}

format_section_separator() {
  _value=$1
  echo -e "\n------------------------------------------------------" >> ${OUTPUT_FILE}
  echo "$_value" >> ${OUTPUT_FILE}
  echo "------------------------------------------------------" >> ${OUTPUT_FILE}
}

run_check_privs() {
  if [ "$EUID" -ne 0 ]; then
    echo "[!] Please run as root"
    exit 1
  fi
}

# NOTE:
#  If $COMPRESS_EVIDENCE_CMD is changed, the proper
#   file extention in $EVIDENCE_COLLECTION_FILE
#   may also need to be changed
run_cleanup(){
  format_main_separator
  echo "[*] Collection Finished: ${DATE_FMT}" | tee -a ${OUTPUT_FILE}

  echo "[+] Compressing evidence" | tee -a ${OUTPUT_FILE}
  cd "${START_DIR}"
  COMPRESS_EVIDENCE_CMD=(tar -Sczf)
  "${COMPRESS_EVIDENCE_CMD[@]}" "${EVIDENCE_COLLECTION_FILE}" "${EVIDENCE_DIR}"

  if [ "${TEST_MODE}" = "false" ]; then
    echo "[+] Removing collection folder"
    rm -rf "${EVIDENCE_DIR}"
  fi
}

# NOTE:
#   Requires: root privileges (some commands)
run_commands() {
  echo "[+] Running general triage commands" | tee -a ${OUTPUT_FILE}
  for _command in "${COMMANDS_TO_EXECUTE[@]}"; do
    format_section_separator "$_command"
    $_command &>> ${OUTPUT_FILE}
  done
}

run_copy_misc_files() {
  if [ "${#MISC_FILES_TO_ACQUIRE[@]}" -gt 0 ]; then
    echo "[+] Copying misc. files of interest" | tee -a ${OUTPUT_FILE}
    for _misc_file in "${MISC_FILES_TO_ACQUIRE[@]}"; do
      echo -e "\t[-] Looking for: $_misc_file" >> ${OUTPUT_FILE}
      MISC_FILES_TO_ACQUIRE_CMD=(find /etc /home /root -type f -name $_misc_file -exec cp --parents --no-preserve=mode,ownership {} . \;)
      "${MISC_FILES_TO_ACQUIRE_CMD[@]}" 2>>${ERROR_FILE}
    done
  fi
}

run_create_filelisting() {
  echo "[+] Generating file listing" | tee -a ${OUTPUT_FILE}
  FILE_LISTING_CMD=("find / -print0")
  FILE_LISTING_TIMELINE_CMD=("xargs -0 stat -c %n,%F,%s,%A,%u,%U,%g,%G,%h,%m,%i,%W,%X,%Y,%Z")
  format_section_separator "$FILE_LISTING_CMD | $FILE_LISTING_TIMELINE_CMD"
  ${FILE_LISTING_CMD[@]} | ${FILE_LISTING_TIMELINE_CMD[@]} 1>>file_listing.csv 2>>file_listing.errors
}

run_copy_directories() {
  if [ "${#DIRECTORIES_TO_COPY[@]}" -gt 0 ]; then
    echo "[-] Copying directories of interest" | tee -a ${OUTPUT_FILE}
    for _dir in "${DIRECTORIES_TO_COPY[@]}"; do
      echo -e "\t[-] Looking for: $_dir" >> ${OUTPUT_FILE}
      COPY_DIRECTORIES_CMD=(cp -r --parents --no-preserve=mode,ownership)
      "${COPY_DIRECTORIES_CMD[@]}" "$_dir" . 2>>${ERROR_FILE}
    done
  fi
}

run_copy_history_files() {
  echo "[+] Getting history files" | tee -a ${OUTPUT_FILE}
  for _history_file in "${HISTORY_FILES_TO_ACQUIRE[@]}"; do
    echo -e "\t[-] Looking for: $_history_file" >> ${OUTPUT_FILE}
    COPY_HIST_FILES_CMD=(find /home /root -type f -name $_history_file -exec cp --parents --no-preserve=mode,ownership {} . \;)
    "${COPY_HIST_FILES_CMD[@]}" 2>>${ERROR_FILE}
  done
}

run_copy_specific_files() {
  if [ "${#SPECIFIC_FILES_TO_ACQUIRE[@]}" -gt 0 ]; then
    echo "[+] Copying specific files of interest" | tee -a ${OUTPUT_FILE}
    for _specific_file in "${SPECIFIC_FILES_TO_ACQUIRE[@]}"; do
      echo -e "\t[-] Looking for: $_specific_file" >> ${OUTPUT_FILE}
      COPY_SPECIFIC_FILES_CMD=(cp --parents --no-preserve=mode,ownership $_specific_file .)
      "${COPY_SPECIFIC_FILES_CMD[@]}" 2>>${ERROR_FILE}
    done
  fi
}

run_get_file_contents() {
  if [ "${#FILES_TO_READ[@]}" -gt 0 ]; then
    echo "[+] Running read content commands" | tee -a ${OUTPUT_FILE}
    for _file_to_read in "${FILES_TO_READ[@]}"; do
      echo -e "\t[-] Looking for: $_file_to_read" >> ${OUTPUT_FILE}
      if [ -f $_file_to_read ]; then
        output=`echo $_file_to_read | sed s'/[ \/]/_/g'`
        READ_FILE_CMD=(cat)
        "${READ_FILE_CMD[@]}" $_file_to_read 1> $output 2>>${ERROR_FILE}
      fi
    done
  fi
}

run_setup() {
  mkdir -p "${EVIDENCE_DIR}"

  # Change working directory to triage directory
  cd "${EVIDENCE_DIR}"

  echo "[*] Collection Started: ${DATE_FMT}" | tee -a ${OUTPUT_FILE}
  format_main_separator
}

run_show_help() {
  echo "Mandiant shell script to retrieve forensic artifacts."
  echo
  echo "1. Change the file mode to allow executing"
  echo -e "\t chmod +x $0"
  echo "2. Run this script with elevated privileges (required for some commands)"
  echo -e "\t sudo ./$0"
  echo
}

while getopts "ht" option; do
   case ${option} in
     ##########################################
     # 1. Show usage, if needed
     ##########################################
     h)
        run_show_help
        exit;;
     t)
        TEST_MODE="true"
        ;;
   esac
done

##########################################
# 2. Check privileges
##########################################
run_check_privs

##########################################
# 3. Perform any analysis configuration
##########################################
run_setup

##########################################
# 4. Start the triage collection
##########################################
run_copy_history_files
run_commands
run_copy_specific_files
run_get_file_contents
run_copy_misc_files
run_copy_directories
run_create_filelisting

##########################################
# 5. Compress evidence
##########################################
run_cleanup
