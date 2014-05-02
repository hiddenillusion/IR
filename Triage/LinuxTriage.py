#!/usr/bin/env python

# original source : @sk3tchymoos3 
# modified by Glenn P. Edwards Jr.
#	http://hiddenillusion.blogspot.com
#       	@hiddenillusion
# Date: 12-28-2012

import os
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Grabs some *nix info off of a system.')
parser.add_argument('-d','--directory', help='Directory to save the output of the commands to.', required=True)
parser.add_argument('-o','--output', default='info.txt', help='Filename to save the output of the commands to.  Default is "info.txt"', required=False)
args = vars(parser.parse_args())

directory = args['directory']
if not os.path.exists(directory):
    try:
        os.makedirs(directory)
    except Exception, msg:
        print "[!] ",msg
        sys.exit()

if args['output']:
    fname = args['output']

outty = os.path.join(directory,fname)
print "[+] Saving to: ", os.path.abspath(outty)

def general(f):
    """
    Collects general *nix info.
    """
    genCmds = ['date',
            'id',
            'hostname',
            'uname',
            'uname -a',
            'who',
            'w',
            'cat /etc/*-release',
            'cat /proc/version',
            'ifconfig',
            'ps -aef',
            'crontab -l',
            'lsof -w',
            'netstat -an',
            'df -HaT',
            'lsmod '
            'cat /etc/passwd',
            #'sudo cat /etc/shadow', # this is going to prompt you for the pw then
            'date']

    for cmd in genCmds:
        info = "[+] Command: %s" % cmd
        print info
        f.write('\n' + info + '\n')
        p = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
        for line in p.communicate():
            f.write(line)

def specific(f):
    """
    Checks for specific package installers/locations (on the left) and if they exist then run the command (on the right)
    """
    specCmds = {'/usr/bin/rpm': 'rpm -qa',
                '/usr/bin/dpkg': 'dpkg --get-selections',
                '/usr/bin/yum': 'list installed',
                '/etc/hosts': 'cat /etc/hosts',
                '/etc/hosts.equiv': 'cat /etc/hosts.equiv',
                '/var/log/messages': 'cat /var/log/messages',
                '/var/log/auth.log': 'cat /var/log/auth.log',
                '/var/log/apache2/access.log': 'cat /var/log/apache2/access.log',
                '/var/log/apache2/error.log': 'cat /var/log/apache2/error.log'
               }
    for loc,cmd in specCmds.iteritems():
        if os.path.exists(loc):
            info = "[+] Command: %s" % cmd
            print info
            f.write('\n' + info + '\n')
            p = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
            for line in p.communicate():
                f.write(line)
        else: 
            err = "[!] Doesn't exist: '%s'" % loc
            print err
            f.write('\n' + err + '\n')

def main():
    with open(outty,'wa') as f:
        general(f)
        specific(f)

if __name__ == "__main__":
    main()
