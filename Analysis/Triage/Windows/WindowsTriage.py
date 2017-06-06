#!/usr/bin/env python

# created by Glenn P. Edwards Jr.
#   http://hiddenillusion.blogspot.com
#       @hiddenillusion
# Date: 2014-12-29
# (while at FireEye)

# To-Do:
#	[ ] $MFT
#	[ ] A/V logs

import re
import os
import sys
import time
import errno
import logging
from zipfile import ZipFile
from shutil import copytree, copy, rmtree

__version__ = "0.1.0"

def acceptable_size(filepath):
	artifact_size = os.path.getsize(filepath)
	unacceptable_sizes = {}
	# Doesn't look like a good one to use. This size can mean it's empty
	#	or it has a small amount of events. Eh.
	#unacceptable_sizes['.evtx'] = 69632

	for artifact_ext, unacceptable_size in unacceptable_sizes.iteritems():
		if filepath.endswith(artifact_ext):
			if artifact_size <= int(unacceptable_size):
				_logger.warn("File size is considered unacceptable, skipping '{0}'".format(filepath))
				return False

# this helps with size but still much larger than something like 7z
def compress_artifacts(filepath, destination_path, zip_name=None):
	if not zip_name:
		zip_name = os.path.join(os.path.dirname(destination_path), 'artifacts.zip')

	with ZipFile(zip_name, mode='a') as zippy:
		try:
			zippy.write(filepath)
		except Exception as err:
			_logger.error("Error compressing '{0}'".format(filepath))

def convert_paths(filepath):
	if not os.name == "nt":
		# os.path.join will interpret this as the path is it leads with a slash
		return filepath.replace('\\', '/').lstrip('/')
	else:
		return filepath

def copy_dir(filepath, destination_path):
	safe_dir_path = get_safe_path(filepath)
	safe_dest_path = os.path.join(destination_path, safe_dir_path)

	try:
		copytree(filepath, safe_dest_path)
	except OSError as err:
		_logger.error("Error copying '{0}".format(filepath))
	except IOError as err:
		_logger.error("IOError on '{0}'".format(filepath))
		if err.errno == 13:
			_logger.warning("Permission denied on '{0}', elevate privileges?".format(filepath))

def copy_files(filepath, destination_path):
	create_dir(destination_path)
	safe_dest_path = os.path.join(destination_path, get_safe_path(filepath))

	try:
		_logger.debug("Copying '{0}'".format(filepath))
		copy(filepath, safe_dest_path)
	except OSError as err:
		_logger.error("Error copying '{0}".format(filepath))

def create_dir(dir_name):
	if not os.path.exists(dir_name):
		_logger.debug("Creating output dir: {0}".format(dir_name))
		try:
			os.makedirs(dir_name)
		except Exception as err:
			_logger.error("Unable to create directory")

def get_artifacts(root, artifact_files, output_dir):
	# Process artifact files with exact locations
	for artifact in artifact_files:
		artifact = convert_paths(artifact)
		artifact_path = os.path.join(root, artifact)
		if os.path.exists(artifact_path):
			if not acceptable_size(artifact_path):
				pass

			copy_files(artifact_path, output_dir)
		else:
			_logger.debug("Skipping non-existing artifact '{0}'".format(artifact))

def get_artifact_folders(root, artifact_folders, output_dir):
	# 	- dest folder must not exist already with shutil.copytree
	for folder in artifact_folders:
		# Process artifact folder with file extention restrictions
		if isinstance(folder, dict):
			for f, lst in folder.iteritems():
				new_folder = convert_paths(f)
				ext_lst = lst

			artifact_folder = os.path.join(root, new_folder)
			if os.path.exists(artifact_folder):
				_logger.debug("Copying '{0}' files from {1}'".format(ext_lst, artifact_folder))
				for fpath in RecursePath(artifact_folder):
					for ext in ext_lst:
						if fpath.endswith(ext):
							try:
								copy_files(fpath, output_dir)
							except Exception as err: # could be related to named pipes
								_logger.error(err)
								continue
			else:
				_logger.debug("Skipping non-existing artifact '{0}'".format(folder))
		else:
			folder = convert_paths(folder)
			artifact_folder = os.path.join(root, folder)
			if os.path.exists(artifact_folder):
				_logger.debug("Copying '{0}'".format(artifact_folder))
				try:
					copy_dir(artifact_folder, output_dir)
				except Exception as err: # could be related to named pipes
					_logger.error(err)
					continue
			else:
				_logger.debug("Skipping non-existing artifact '{0}'".format(folder))

def get_all_user_paths(root):
	discovered_user_paths = []

	try:
		xp = os.path.join(root, '{0}'.format(convert_paths('\\Documents and Settings')))
		xp_users = os.listdir(xp)
	except WindowsError:
		xp_users = False

	if xp_users:
		_logger.debug("System detected as XP")
		for username in xp_users:
			discovered_user_paths.append(os.path.join(xp, username))
		return discovered_user_paths

	try:
		seven = os.path.join(root, '{0}'.format(convert_paths('\\Users')))
		seven_users = os.listdir(seven)
	except WindowsError:
		seven_users = False

	if seven_users:
		_logger.debug("System detected as 7")
		for username in seven_users:
			discovered_user_paths.append(os.path.join(seven, username))
		return discovered_user_paths

	return False

def get_specific_artifacts(user_paths, user_artifacts, output_dir):
	try:
		for user_path in user_paths:
			for artifact in user_artifacts:
				user_artifact = os.path.join(user_path, convert_paths(artifact))
				if os.path.exists(user_artifact):
					try:
						if os.path.isdir(user_artifact):
							copy_dir(user_artifact, output_dir)
						else:
							copy_files(user_artifact, output_dir)
					except Exception as err:
						if not err.errno == 22:
							_logger.error(err)
						continue
				else:
					_logger.debug("Filepath does not exist '{0}'".format(user_artifact))

	except Exception as err:
		if not err.errno == 22: #path not there
			_logger.error(err)
		pass

def doWork(path, output_dir):
	if os.name == "nt":
		root = os.path.split(os.path.dirname(path))[0]
	else:
		root = path

	# TO-DO: maybe better just to check OS & %windir% then grab since
	#	there are still systems running Win 2k etc.?
	# Try all and fail if non-existent
	# should probably put these into their respective folders in
	#	the output folder since going to do that anyway
	artifact_files = ['\\Windows\\AppCompat\\Programs\\Amcache.hve',
						'\\Windows\\AppCompat\\Programs\\RecentFileCache.bcf',
						'\\Windows\\inf\\setupapi.dev.log',
						'\\Windows\\SchedLgU.txt',
						'\\Windows\\setupapi.log',
						#'\\Windows\\System32\\config\\AppEvent.evt',
						#'\\Windows\\System32\\config\\SecEvent.evt',
						#'\\Windows\\System32\\config\\SysEvent.evt',
						'\\Windows\\System32\\config\\SAM',
						'\\Windows\\System32\\config\\SECURITY',
						'\\Windows\\System32\\config\\SOFTWARE',
						'\\Windows\\System32\\config\\SYSTEM',
						'\\Windows\\System32\\drivers\\etc\\hosts',
						#'\\Windows\\System32\\wbem\\Repository\\Objects.data',
						#'\\Windows\\System32\\winevt\\Logs\\Application.evtx',
						#'\\Windows\\System32\\winevt\\Logs\\microsoft-windows-RemoteDesktopServices-RemoteDesktopSessionManager%4Admin.evtx',
						#'\\Windows\\System32\\winevt\\Logs\\microsoft-windows-RemoteDesktopServices-RemoteDesktopSessionManager%4Operational.evtx',
						#'\\Windows\\System32\\winevt\\Logs\\Microsoft-Windows-TaskScheduler%4Operational.evtx',
						#'\\Windows\\System32\\winevt\\Logs\\Microsoft-Windows-TerminalServices-LocalSessionManager%4Admin.evtx',
						#'\\Windows\\System32\\winevt\\Logs\\Microsoft-Windows-TerminalServices-LocalSessionManager%4Operational.evtx',
						#'\\Windows\\System32\\winevt\\Logs\\Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Operational.evtx',
						#'\\Windows\\System32\\winevt\\Logs\\OAlerts.evtx',
						#'\\Windows\\System32\\winevt\\Logs\\Security.evtx',
						#'\\Windows\\System32\\winevt\\Logs\\System.evtx',
						#'\\Windows\\System32\\winevt\\Logs\\Windows PowerShell.evtx',
						'\\WINNT\\SchedLgU.txt',
						#'\\WINNT\\System32\\config\\AppEvt.evt',
						#'\\WINNT\\System32\\config\\SecEvent.evt',
						#'\\WINNT\\System32\\config\\SysEvent.evt',
						'\\WINNT\\System32\\config\\SAM',
						'\\WINNT\\System32\\config\\SECURITY',
						'\\WINNT\\System32\\config\\SOFTWARE',
						'\\WINNT\\System32\\config\\SYSTEM',
			 ]

	# Make life easier and just don't have trailing slashes here
	artifact_folders = ['\\Windows\\Prefetch',
						'\\Windows\\Tasks',
						{'\\Windows\\System32\\config': ['.evt']},
						'\\Windows\\System32\\winevt\\Logs',
						'\\Windows\\SysWOW64\\Tasks',
						{'\\WINNT\\System32\\config': ['.evt']},
			]

	# Process artifact files with flexible locations
	# TO-DO: add other ntuser.dat locations?
	user_artifacts = ['NTUSER.DAT',
						'AppData\\Local\\Microsoft\\Windows\\UsrClass.dat',
						'AppData\\Local\\Microsoft\\Terminal Server Client\\Cache\\bcache22.bmc',
						'Default.rdp',
						'AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadline\\ConsoleHost_history.txt',
			]

	# Make life easier and just don't have trailing slashes here
	user_folders = ['AppData\\Roaming\\Microsoft\\Windows\\Recent\\AutomaticDestinations',
					'AppData\\Roaming\\Microsoft\\Windows\\Recent\\CustomDestinations',
					'AppData\\Roaming\\Microsoft\\Windows\\Recent',
			]

	# Get a list of user profile directories
	user_paths = get_all_user_paths(root)
	if not user_paths:
		_logger.error("No user profiles found")
	else:
		get_specific_artifacts(user_paths, user_artifacts, output_dir)
		# Process user specific folders
		#get_artifact_folders(root, user_folders, output_dir)
		get_specific_artifacts(user_paths, user_folders, output_dir)

	# Process artifact files with exact locations
	get_artifacts(root, artifact_files, output_dir)
	# Process artifact folders
	get_artifact_folders(root, artifact_folders, output_dir)

def get_safe_path(filepath):
	no_bueno = ['<', '>', '{', '}', '|', ':', ';', '\\', '/']
	return ''.join(['_' if c in no_bueno else c for c in os.path.abspath(filepath)])

def RecursePath(path):
	if os.path.exists(path):
		if os.path.isdir(path):
			for root, dirs, files in os.walk(path):
				dirs.sort()
				for name in sorted(files):
					fname = os.path.join(root, name)
					if os.path.isfile(fname):
						_logger.debug("File found '{0}'".format(fname))
						yield fname
					else:
						_logger.debug("Skipping symlink '{0}'".format(fname))
						pass
		else:
			if os.path.isfile(path):
				_logger.debug("File found '{0}'".format(path))
				yield path
			else:
				_logger.debug("Symlink provided '{0}'".format(path))

def SetupLogger(loggerName, logLevel, logFile):
	# import sys, time, logging
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

	formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(name)s - %(module)s:%(funcName)s():%(lineno)d  | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	# Default TZ is local
	formatter.converter = time.gmtime
	shandler = logging.StreamHandler(sys.stdout)
	shandler.setFormatter(formatter)
	logger.addHandler(shandler)

	if logFile:
		log_path = os.path.abspath(logFile)
		log_dir = os.path.dirname(log_path)
		if not os.path.exists(log_dir):
			os.makedirs(log_dir)
		fhandler = logging.FileHandler(logFile)
		fhandler.setFormatter(formatter)
		logger.addHandler(fhandler)

	return logger

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Grabs sniper artifacts from a mounted filesystem. Try running from an elevated shell if errors are generated. \
													Note: This currently compresses the artifacts grabbed but you may want to add stuff it doesn\'t \
													currently grab such as $MFT etc. so uncompressed folder structure is also left there.')
	parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging', required=False)
	parser.add_argument('-i', '--input', action='store', metavar='[Mount Point]', help='Path to mounted filesystem (e.g. - "E:" or "/mnt/point").', required=True)
	parser.add_argument('-o', '--output', action='store', metavar='[Output Directory]', help='Output path to copy files to.', required=True)
	args = vars(parser.parse_args())

	path = args['input']
	output_dir = os.path.abspath(args['output'])

	if not args['debug']:
		logLevel = "INFO"
	else:
		logLevel = "DEBUG"

	_logger = SetupLogger("AutoDFIR", logLevel, os.path.join(output_dir, 'sniper_process.log'))
	_logger.info("Starting {0}".format(__file__))
	_logger.info("Copying files to '{0}'".format(output_dir))

	doWork(path, output_dir)

	# Compress artifacts for quicker transfer
	# Note: 7z was 44.8 MB, python zip was 198.8 MB!
	#zip_name = os.path.join(os.path.dirname(output_dir), 'artifacts.zip')
	#_logger.info("Compressing artifacts to '{0}'".format(zip_name))
	#for path in RecursePath(output_dir):
	#	compress_artifacts(path, output_dir)

	# Get rid of uncompressed artifacts previously copied - will get error if logger stil active
	'''
	sys.stdout.write("[+] Deleting uncompressed artifacts '{0}'\n".format(output_dir))
	try:
		rmtree(output_dir)
	except Exception as err:
		sys.stdout.write("[!] Could not delete uncompressed artifacts '{0}'\n".format(output_dir))
		sys.stdout.write("{0}".format(err))
	'''
	sys.stdout.write("[+] Don't forget to delete uncompressed artifacts '{0}'\n".format(zip_name))
