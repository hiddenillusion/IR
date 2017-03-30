#!/usr/bin/env python

# created by Glenn P. Edwards Jr.
#   http://hiddenillusion.blogspot.com
#       @hiddenillusion
# Date: 2016-07-06
# (while at FireEye)

import os
import sys
import json

try:
	from sshpubkeys import InvalidKeyException, SSHKey
except ImportError:
	print("[!] python-sshpubkeys needed : https://github.com/ojarva/python-sshpubkeys")
	sys.exit(1)

# Servers you've already connected to:
# 	- /.ssh/known_hosts
# The login attempt is accepted if the user proves that (s)he knows the private key and the public key is in the account's authorization list:
# /.ssh/authorized_keys
# /.ssh/authorized_key2

# The SSH fingerprint will be displayed within /var/log/secure* when it's provided during SSH authentication
#	e.g. - Accepted publickey for root from 1.2.3.4 port 39874 ssh2: RSA 56:84:1e:90:08:3b:60:c7:29:70:5f:5e:25:a6:3b:86

"""
1. configure either the entire compromised SSH public key or the MD5 fingerprint of the compromised SSH public key:

	1.1 - `--key` could hold the contents of the compromised public key you want to hunt for
	- e.g. - /root/.ssh/id_rsa.pub or /home/<user>/.ssh/id_rsa.pub would contain:
	'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQCxO38tKAJXIs9ivPxt7AYdfybgtAR1ow3Qkb9GPQ6wkFHQqcFDe6faKCxH6iDRteo4D8L8BxwzN42uZSB0nfmjkIxFTcEU3mFSXEbWByg78aoddMrAAjatyrhH1pON6P0='

	1.2 - `--fingerprint` could hold '56:84:1e:90:08:3b:60:c7:29:70:5f:5e:25:a6:3b:86'

2. supply path to file(s) containing SSH public keys to test the `compromised_public_key` against
	- e.g. - */.ssh/authorized_keys, */.ssh/authorized_keys2, */.ssh/known_hosts

Results of all processing will be dumped is json format to `--output`. If the MD5 fingerprint of the `compromised_public_key`	is found in
	any of the entries from step #2, it is printed to STDOUT + loggedin the field `fingerprint_matched_compromised`.
"""

class CompromisedSSHKey(object):
	""" Placeholder for result of supplied compromised key information """
	details = {}

class ExtractSSHKeyDetails(object):
	def __init__(self, ssh_key, query_type=None):
		"""
		@query_type : What you want to add to the key names of the returned dictionary (e.g. - 'compromised')
		"""
		self._query_type = query_type
		self._ssh_key = ssh_key

	def get_ssh_key_details(self):
		"""
		@return: A dictionary of parsed ssh key details
		"""
		details = {
			'bits': self._ssh_key.bits,									# 768
			'key_type': self._ssh_key.key_type,					# ssh-rsa
			'key_data': self._ssh_key.keydata,					# ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQCxO38tKAJXIs9ivPxt7AYdfybgtAR1ow3Qkb9GPQ6wkFHQqcFDe6faKCxH6iDRteo4D8L8BxwzN42uZSB0nfmjkIxFTcEU3mFSXEbWByg78aoddMrAAjatyrhH1pON6P0=
			'md5_hash': self._ssh_key.hash_md5(),				# 56:84:1e:90:08:3b:60:c7:29:70:5f:5e:25:a6:3b:86
			'sha256_hash': self._ssh_key.hash_sha256(),	# SHA256:xk3IEJIdIoR9MmSRXTP98rjDdZocmXJje/28ohMQEwM
			'sha512_hash': self._ssh_key.hash_sha512(),	# SHA512:1C3lNBhjpDVQe39hnyy+xvlZYU3IPwzqK1rVneGavy6O3/ebjEQSFvmeWoyMTplIanmUK1hmr9nA8Skmj516HA
		}

		if self._query_type:
			old_details = details
			details = {}
			for k, v in old_details.iteritems():
				details['{0}_{1}'.format(k, self._query_type)] = v

		return details

class ProcessFile(CompromisedSSHKey):
	def __init__(self, filepath):
		self._compromised_ssh_key_details = CompromisedSSHKey.details
		self._current_ssh_key_details = {}
		self._filepath = filepath
		self._all_parsed_lines = []

	def compare_fingerprints(self):
		"""
		@compromised_fingerprint : Dict. containing MD5 fingerprint supplied at runtime for hunting
		@parsed_fingerprint : Dict. MD5 fingerprint found in current line being parsed
		"""

		#if compromised_ssh_key_details.get('md5_hash') == ssh_key_details.get('md5_hash'):
		if self._compromised_ssh_key_details.get('md5_hash_compromised') == self._current_ssh_key_details.get('md5_hash'):
			print("[+] Compromised SSH fingerprint found in: '{0}'".format(self._current_ssh_key_details.get('key_file_path')))
			self._current_ssh_key_details['fingerprint_matched_compromised'] = True
		else:
			self._current_ssh_key_details['fingerprint_matched_compromised'] = False

		for k, v in self._compromised_ssh_key_details.iteritems():
			self._current_ssh_key_details[k] = v

		return self._current_ssh_key_details

	def parse_lines(self):
		with open(self._filepath, 'r') as inny:
			data = inny.readlines()
			for line in data:
				line = line.strip()

				if not line:
					continue

				try:
					ssh_key_data = SSHKey(line)
					extracted_details = ExtractSSHKeyDetails(ssh_key_data)
					self._current_ssh_key_details = extracted_details.get_ssh_key_details()
					self._current_ssh_key_details['key_file_path'] = filepath
				except InvalidKeyException:
					continue

				# Incase we just run this over mixed data
				except Exception as err:
					continue

				self.compare_fingerprints()
				self._all_parsed_lines.append(self._current_ssh_key_details)

		return self._all_parsed_lines

def RecursePath(path):
	if not os.path.exists(path):
		path = path.rstrip('"')
		if not os.path.exists(path):
			return

	if os.path.exists(path):
		if os.path.isdir(path):
			for root, dirs, files in os.walk(path):
				dirs.sort()
				for name in sorted(files):
					fname = os.path.join(root, name)
					if os.path.isfile(fname):
						yield fname
					else:
						pass
		else:
			if os.path.isfile(path):
				yield path

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Generates MD5 of SSH public key & searches for it across supplied authorized_keys* & known_host files')
	parser.add_argument('-i', '--input', action='store', help='Input file or directory of files to recursively process.', required=True)
	parser.add_argument('-o', '--output', action='store', help='Path to store parsed results.', required=True)

	compromised_group = parser.add_mutually_exclusive_group()
	compromised_group.add_argument('-k', '--key', action='store', help='Key type and base64 encoded value of compromised SSH public key to hash & compare against. \
		e.g. - \'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQCxO38tKAJXIs9ivPxt7AYdfybgtAR1ow3Qkb9GPQ6wkFHQqcFDe6faKCxH6iDRteo4D8L8BxwzN42uZSB0nfmjkIxFTcEU3mFSXEbWByg78aoddMrAAjatyrhH1pON6P0=\'',
		required=False)
	compromised_group.add_argument('-f', '--fingerprint', action='store', help='MD5 hash of the base64-encoded compromised SSH public key to compare against. \
		e.g. - 56:84:1e:90:08:3b:60:c7:29:70:5f:5e:25:a6:3b:86', required=False)

	args = vars(parser.parse_args())

	path = os.path.abspath(args['input'])
	output = os.path.abspath(args['output'])
	compromised_key = args['key']
	compromised_fingerprint = args['fingerprint']

	if not os.path.exists(path):
		print("[!] Input path does not exist")
		sys.exit(1)

	if not os.path.exists(output):
		print("[!] Output path does not exist")
		sys.exit(1)
	else:
		output = os.path.join(output, 'ssh_parsed_results.json')

	if compromised_key:
		compromised_ssh_key = SSHKey(compromised_key)
		extracted_details = ExtractSSHKeyDetails(compromised_ssh_key, 'compromised')
		CompromisedSSHKey.details = extracted_details.get_ssh_key_details()
	else:
		CompromisedSSHKey.details = {'md5_hash_compromised': compromised_fingerprint}

	for filepath in RecursePath(path):
		process = ProcessFile(filepath)
		parsed_lines = process.parse_lines()

		if parsed_lines:
			#print(json.dumps(parsed_lines, sort_keys=True, indent=4))
			with open(output, 'a') as outty:
				outty.write(json.dumps(parsed_lines, sort_keys=True, indent=4))
