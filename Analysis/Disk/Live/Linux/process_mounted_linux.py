#!/usr/bin/env python

# created by Glenn P. Edwards Jr.
#   http://hiddenillusion.blogspot.com
#       @hiddenillusion
# Version 0.0.2
# Date: 10-09 -2014
# (while at FireEye)

import os
import re
import sys
import logging
#from collections import defaultdict

def logger(loggerName, logLevel):
	""" Simple logger """
	logger = logging.getLogger(loggerName)

	if logLevel == "INFO":
		logger.setLevel(logging.INFO)
	elif logLevel == "WARN":
		logger.setLevel(logging.WARN)
	elif logLevel == "DEBUG":
		logger.setLevel(logging.DEBUG)
	elif logLevel == "ERROR":
		logger.setLevel(logging.ERROR)
	else:
		pass

	formatter = logging.Formatter('%(levelname)-5s %(name)s - %(asctime)s - %(module)s:%(funcName)s():%(lineno)d  | %(message)s') # right now in local time, change to UTC?

	shandler = logging.StreamHandler(sys.stdout)
	shandler.setFormatter(formatter)
	logger.addHandler(shandler)

	return logger

def create_dir(folder):
	print "[i] creating dir: {0}".format(folder)
	if not os.path.exists(folder):
		try:
			os.makedirs(folder)
		except Exception: #change this to a specific one?
			print "[!]",e
			sys.exit(1)    
	else:
		print "[-] Folder already exists:",folder

def get_device(mount_pnt):
	import subprocess
	try:
		p = subprocess.Popen('mount',stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
		for line in p.stdout:
			reggy = re.match(r'(.*)\son\s(.*)type.*', line)
			dev = reggy.group(1)
			mnt_pnt = reggy.group(2).strip()
			if mnt_pnt == mount_pnt:
				return dev
	except Exception as e:
		print "[!]", e

def check_sudo():
    """
    Checks the UID of the current user
    @return String indication if user is Sudo or not
    """
    if os.getuid() != 0:
        return "NotSudo"
    else:
        return "Sudo"

# delete and move to Process class?
def get_path(evidence_path, artifact_path):
    '''
    If the image is mounted, the regular full path
    will be incorrect so it needs to be corrected.

    Note: os.path.join discards args propt to one containing a leading slash
    '''

    #print os.path.join(input_path, artifact_path)
    combined_path = evidence_path + artifact_path
    return combined_path

# delete and move to Process class?
def check_list(data):
	if type(data).__name__ == "list":
		return True
	else:
		return False

def check_string(data):
	if type(data).__name__ == "str":
		return True
	else:
		return False

def get_current_user():
    """
    @return Current user name
    """
    import getpass
    return getpass.getuser()

def query(data):
    pass

class ProcessException(Exception):
    """
    Base Exception class for process
    """
    def __init__(self, value):
        """
        @value: A string description
        """
        super(ProcessException, self).__init__()
        self._value = value

    def __str__(self):
        return "Process Exception: {0}".format(self._value)

class Process:
	"""
	Convenience class that gets common data and performs
	common operations
	"""
    
	def __init__(self, evidence, logLevel=None):
		if not logLevel:
			logLevel = "INFO"

		self._evidence = evidence
		self._buff = None
		self._f = None
		self._fh = None
		self._output_path = None
		self._artifact_path = None
		self._checks = None
		self._results = {}
		self._data = None
        	self._log = logger("auto_dfir_linux:Process", logLevel)

	def find_artifact(self, artifact_path):
		"""
		artifact_path: str
		"""
		self._artifact_path = artifact_path
		self._log.debug("Checking for artifact: {0}".format(self._artifact_path))
		if os.path.exists(get_path(self._evidence, self._artifact_path)):
			return True
		else:
			return False

	def read_contents(self, location):
		"""
		location: string, dictionary or list
		@return List of results
		"""
		self._location = location
		results = []
		# check to see if it's a directory

		# string
		if check_string(self._location) == True:
			artifact_path = get_path(self._evidence, self._location)
			if os.path.exists(artifact_path):
				self._log.debug("Attempting to read: {0}".format(artifact_path))
				with open(artifact_path, 'r') as contents:
					for line in contents:
						results.append(line.strip('\n'))
					yield results
			else:
				self._log.debug("Path doesn't exist: {0}".format(artifact_path))
 		# list
		elif check_list(self._location) == True:
			for loc in self._location:
				artifact_path = get_path(self._evidence, loc)
				if os.path.exists(artifact_path):
					self._log.debug("Attempting to read: {0}".format(artifact_path))
					with open(artifact_path, 'r') as contents:
						for line in contents:
							results.append(line.strip('\n'))
						yield results
				else:
					self._log.debug("Path doesn't exist: {0}".format(artifact_path))
		# dictionary
		else:
			for check, location in self._location.iteritems():
				artifact_path = get_path(self._evidence, location)
				if os.path.exists(artifact_path):
					self._log.debug("Attempting to read: {0}".format(artifact_path))
					with open(artifact_path, 'r') as contents:
						for line in contents:
							results.append(line.strip('\n'))
						yield results
				else:
					self._log.debug("Path doesn't exist: {0}".format(artifact_path))
		#return results

class General:
    def __init__(self, evidence, logLevel=None):
        """
        @evidence: Path to mounted image
        """
	if not logLevel:
		logLevel = "INFO"
        self._evidence = evidence
        self._data = {}
        self._results = {}
        self._log = logger("auto_dfir_linux:General", logLevel)

    def get_all_general_info(self):
	print self.system_info()
	print self.volume_info()
	print self.user_info()

    def automated_info():
        pass

    def auth_info():
        pass

    def logging_info():
        pass

    def network_info():
        pass

    def security_info():
        pass

    def system_info(self):
	self._log.info("Getting system information")
	version_lst = ['/proc/version', '/etc/lsb-release', '/etc/centos-release', '/etc/redhat-release']
	hostname_lst = ['/etc/sysconfig/network']

	proc = Process(self._evidence)
	for check in proc.read_contents(version_lst):
		if check:
			self._results['version'] = check
	for check in proc.read_contents(hostname_lst):
		if check:
			for setting in check:
				if re.match('^hostname=.*$', setting, re.I):
					self._results['hostname'] = setting.lower().replace("hostname=","")

	return self._results

    def user_info(self):
	self._log.info("Getting user information")
	users = []
	proc = Process(self._evidence)
	for line in proc.read_contents('/etc/passwd'):
		for l in line:
			if l:
				un = l.split(':')[0]
				users.append(un)
	self._results['users'] = users

	hm_dir = os.path.join(self._evidence, 'home')
	if os.path.exists(hm_dir):
		for root, dirs, files in os.walk(hm_dir):
			dirname = root
			print dirname
		        #for name in files:

    def user_specific_info(self):
	self._user = None
	self._log.info("Getting user's information for {0}".format(self._user))
	users_folders_lst = ['']

	proc = Process(self._evidence)
	for check in proc.read_contents(users_lst):
        	print check


    def mount_info(self):
	self._data = {'mount': '/etc/mtab',
	}
	
	pass

		
    def volume_info(self):
	self._log.info("Getting volume information")
	self._data = {'volume_label': '/etc/fstab',
	}
	
	proc = Process(self._evidence)
	for line in proc.read_contents(self._data):
		if line:
			for l in line:
				if re.match('.*LABEL=.*', l, re.I):
					self._results['label'] = l.split('=')[1]
					self._results['mnt_pt'] = l.split( )[1]
					self._results['fs_type'] = l.split( )[2]
					return self._results
				elif re.match('.*LABEL.*', l, re.I):
					self._results['label'] = l.split(' ')[0]
					self._results['mnt_pt'] = l.split( )[1]
					self._results['fs_type'] = l.split( )[2]
					return self._results
	# means other checks failed
	import subprocess
	dev = get_device(self._evidence)
	opts = " -s "
	cmd =  'file' + opts + dev

	try:
		p = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
		for line in p.stdout.readlines():
			self._results['mnt_pt'] = line.split(':')[0]
			self._results['fs_type'] = line.split(':')[1]
	except Exception as e:
		self._log.error(e)
	return self._results

class Timeline:
	def __init__(self, evidence, output_dir, logLevel=None):
		"""
		@evidence: Path to mounted image
		@output_dir: Path to output	
		"""
		if not logLevel:
			logLevel = "INFO"
		self._evidence = evidence
		self._output_dir = output_dir
		self._device = get_device(self._evidence)
		self._body_file = None
		self._log = logger("auto_dfir_linux:Timeline", logLevel)

	def create_timeline(self):
		self._log.info("Creating timeline")
		self.run_fls()
		self.run_l2t()
		self.run_mactime()

	def run_fls(self):
		import subprocess
		opts = " -r -m '/' "
		self._body_file = os.path.join(self._output_dir, 'fls.body')
		cmd =  'fls' + opts + self._device + ' > ' + self._body_file 

		self._log.info("Running 'fls'")
		self._log.debug("cmd............: {0}".format(cmd))

		try:
			p = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
			p.wait()
		except Exception as e:
			self._log.error(e)

		if not os.path.exists(self._body_file):
			self._log.warn("fls output file not created")

	def run_l2t(self):
		import subprocess
		opts = " -f linux -o mactime -r "
		l2t_out = os.path.join(self._output_dir, 'l2t.csv')
		cmd = 'log2timeline' + opts + self._evidence + ' -w ' + l2t_out

		self._log.info("Running 'l2t'")
		self._log.debug("cmd............: {0}".format(cmd))
	
		try:
			p = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
			p.wait()
		except Exception as e:
			self._log.error(e)

		if not os.path.exists(l2t_out):
			self._log.warn("l2t output file not created")

	def run_mactime(self):
		import subprocess
		self._log.info("Running 'mactime'")
		if self._body_file:
			if os.path.exists(self._body_file):
				opts = " -y -d -b "
				mactime_out = os.path.join(self._output_dir, 'mactime.csv')
				cmd =  'mactime' + opts + self._body_file + ' >> ' + mactime_out

				self._log.info("Running 'mactime' over body_file")
				self._log.debug("cmd............: {0}".format(cmd))
	
				try:
					p = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
					p.wait()
				except Exception as e:
					self._log.error(e)

				if not os.path.exists(mactime_out):
					self._log.warn("mactime output file not created")
			else:
				self._log.warn("body_file not found, skipping mactime execution")
		else:
			self._log.warn("body_file not found, skipping mactime execution")

class Web_Server:
	def __init__(self, evidence):
		"""
		@evidence: Path to mounted image
		"""
		self._log = logging.getLogger(__name__)
		self._evidence = evidence
		self._results = {}
		self._artifacts = {'apache_access': '/var/log/apache2/access.log',
					'apache_error': '/var/log/apache2/error.log',
					'access': '/var/log/httpd/access_log',
					'error': '/var/log/httpd/error_log',
		}

	def read_web_logs(self):
		proc = Process(self._evidence)
		self._results = proc.read_contents(self._artifacts)
		return self._results

	def find_web_logs(self):
		proc = Process(self._evidence)
		for cat, loc in self._artifacts.iteritems():
			self._results[loc] = str(proc.find_artifact(loc))
		return self._results
	
    # web shell scan

class SQL():
    pass

def main():
	import argparse

	parser = argparse.ArgumentParser(description='Grabs data of interest from a mounted linux system & kicks off additional analysis processes')
	parser.add_argument('-c', '--case', metavar='[Case#]', help='Case number to use', required=True)    
	parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging', required=False)
	parser.add_argument('-i', '--input', metavar='[Path]', help='Path to mounted image', required=True)
	parser.add_argument('-o', '--output', metavar='[Output]', help='Output file to write the to.  \
                                                                       If not provided, data written to "/mnt/storage/Cases/[Case #]/[Evidence Tag #]"', required=False)
	parser.add_argument('-t', '--tag', metavar='[Evidence Tag #]', help='Evidence tag number assigned to evidence', required=True)
	args = vars(parser.parse_args())

	# add this as switch
	if args['debug']:
		logLevel = "DEBUG"  
	else:
		logLevel = "INFO"

	_log = logger("auto_dfir_linux", logLevel) 
	case = args['case']
	tag = args['tag']
	evidence = os.path.abspath(args['input'])
	path = os.path.dirname(args['input'])
	#_log = log.LogMe()
	#_log = logging.getLogger(__name__)

	if not os.path.exists(args['input']):
		_log.error("Input file doesn't seem to exist")
		sys.exit(1)

	if args['output']:
		if not args['case'] and not args['tag']:
			_log.error("Output (-o) requires a Case (-c) and a Tag (-t)")
			sys.exit(1)
		else:
			# hax to ensure path gets build correctly cross-platform
			tmp_dir = (args['output'] + ',' + case + ',' + tag).split(',')
			output_dir = os.path.join(*tmp_dir)
	else:
		# hax to ensure path gets build correctly cross-platform
		# need to change this to ls on the storage dir since labs have it different
		#tmp_dir = ("/mnt/storage/Cases" + ',' + case + ',' + tag).split(',')
		#output_dir = os.path.join(*tmp_dir)
		tmp_dir = ("/tmp/" + ',' + case + ',' + tag).split(',')
		output_dir = os.path.join(*tmp_dir)

	if not os.path.exists(output_dir):
		create_dir(output_dir)

	current_user = get_current_user()
	if not current_user == "root":
		_log.debug("Currently running as the user '{0}', not root".format(current_user))
	else:
		_log.debug("Currently running as the user 'root'")        

	_log.info("Processing.....: {0}".format(evidence))
	_log.info("Device.........: {0}".format(get_device(evidence)))
	_log.info("Output location: {0}".format(output_dir))
	_log.info("Assigning Case#: {0}".format(case))


	'''
	report = {}
	gen = General(evidence)
	print gen.system_info()
	#for result in gen.system_info():
	#	r = result.lower()
	#	if re.match('^hostname.*', r):
	#		report['hostname'] = r.split('=')[1] # dangerous but usually seen this way?
	#print report
	#print gen.volume_info()

	web = Web_Server(evidence)
	print web.find_web_logs()

	'''
	#timeline = Timeline(evidence, output_dir, logLevel)
	#timeline.create_timeline()

	gen = General(evidence, logLevel)
	gen.get_all_general_info()
	#for k, v in  gen.system_info().iteritems():
	#	print str(k) +','+ str(v)

if __name__ == "__main__":
	main()

