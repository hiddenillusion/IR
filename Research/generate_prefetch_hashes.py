# created by Glenn P. Edwards Jr.
#   hiddenillusion.github.io
#       @hiddenillusion
# Date: 2016-05-10
# (while at FireEye)

import os
import sys
import json

class Hasher(object):
	def __init__(self, filepath, device=None):
		self._filepath = filepath.upper()
		self._device = ('\\DEVICE\\HARDDISKVOLUME1\\' if not device else device)

	def calculate_all(self):
		if not "device" in self._filepath.lower():
			self._filepath = self.original_to_kernel(path=self._filepath)

		result = {
				'device_used': self._device,
				'filepath': self._filepath,
		}

		all_calculations = [
			{'vista_gleeda': '{0:X}'.format(self.gleeda_vista_function())},
			{'xp_gleeda': '{0:X}'.format(self.gleeda_xp_function())},
			{'xp_libyal': '{0:X}'.format(self.libyal_ssca_xp_hash_function())},
			{'vista_libyal': '{0:X}'.format(self.libyal_ssca_vista_hash_function())},
			{'2008_libyal': '{0:X}'.format(self.libyal_ssca_2008_hash_function())},
		]

		for pair in all_calculations:
			for resource, hash_int in pair.iteritems():
				result.setdefault(hash_int, []).append(resource)

		return result

	def original_to_kernel(self, path):
		"""
		C:\Users\User\AppData\Local\Temp\svchost.exe ->
		USERS\USER\APPDATA\LOCAL\TEMP\SVCHOST.EXE

		Users\User\AppData\Local\Temp\svchost.exe ->
		USERS\USER\APPDATA\LOCAL\TEMP\SVCHOST.EXE
		"""
		try:
			if not ":" in path:
				return '{0}{1}'.format(self._device, path).upper()
			else:
				return '{0}{1}'.format(self._device, path.split('\\', 1)[1]).upper()
		except IndexError as err:
			print('{0} : {1}'.format(path, err))
			return

	def gleeda_xp_function(self):
		import ctypes
		hash = 0
		uni = unicode(self._filepath)
		for i in range(len(uni)):
			num = ord(uni[i])
			if (num > 255):
				hash = ctypes.c_int32(37 * ((37 * hash) + (num / 256)) + (num % 256)).value
			else:
				hash = ctypes.c_int32(37 * ((37 * hash) + num)).value
		hash *= 314159269
		hash = ctypes.c_int32(hash).value
		if hash < 0:
			hash *= -1
		hash %= 1000000007

		return ctypes.c_uint32(hash).value

	def gleeda_vista_function(self):
		import ctypes
		hash = 314159
		uni = unicode(self._filepath)
		for i in range(len(uni)):
			num = ord(uni[i])
			if (num > 255):
				hash = ctypes.c_int32(37 * ((37 * hash) + (num / 256)) + (num % 256)).value
			else:
				hash = ctypes.c_int32(37 * ((37 * hash) + num)).value

		return ctypes.c_uint32(hash).value

	def libyal_ssca_xp_hash_function(self):
		filepath = self._filepath.encode('utf-16-le')
		hash_value = 0
		for character in filepath:
			hash_value = ((hash_value * 37) + ord(character)) % 0x100000000

		hash_value = (hash_value * 314159269) % 0x100000000

		if hash_value > 0x80000000:
			hash_value = 0x100000000 - hash_value

		return (abs(hash_value) % 1000000007) % 0x100000000

	def libyal_ssca_vista_hash_function(self):
		filepath = self._filepath.encode('utf-16-le')
		hash_value = 314159

		for character in filepath:
			hash_value = ((hash_value * 37) + ord(character)) % 0x100000000

		return hash_value

	def libyal_ssca_2008_hash_function(self):
		filepath = self._filepath.encode('utf-16-le')
		hash_value = 314159
		filename_index = 0
		filename_length = len(filepath)

		while filename_index + 8 < filename_length:
			character_value = ord(filepath[filename_index + 1]) * 37
			character_value += ord(filepath[filename_index + 2])
			character_value *= 37
			character_value += ord(filepath[filename_index + 3])
			character_value *= 37
			character_value += ord(filepath[filename_index + 4])
			character_value *= 37
			character_value += ord(filepath[filename_index + 5])
			character_value *= 37
			character_value += ord(filepath[filename_index + 6])
			character_value *= 37
			character_value += ord(filepath[filename_index]) * 442596621
			character_value += ord(filepath[filename_index + 7])

			hash_value = ((character_value - (hash_value * 803794207)) %
						  0x100000000)

			filename_index += 8

		while filename_index < filename_length:
			hash_value = (((37 * hash_value) + ord(filepath[filename_index])) %
						  0x100000000)

			filename_index += 1

		return hash_value

def iterate_devices():
	# ref: http://www.hexacorn.com/blog/2012/10/29/prefetch-file-names-and-unc-paths/
	all_devices = []

	# Enumerated 0-10 for harddiskvolume
	for num in xrange(0,10):
		all_devices.append('\\DEVICE\\HARDDISKVOLUME{0}\\'.format(num))

	# Enumerate a-z for mount points
	mount_point_letters = ['{0}'.format(c.upper()) for c in map(chr, range(97, 123))]

	for mount_letter in mount_point_letters:
		all_devices.append('\\DEVICE\\LANMANREDIRECTOR\\{0}\\'.format(mount_letter))

	# Add misc.
	all_devices.append('\\DEVICE\\HGFS\\VMWARE-HOST\\SHARED FOLDERS\\')

	for device in all_devices:
		yield device

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Calculates Prefetch hashes based on a given file/kernel path.')
	parser.add_argument('-i', '--input', action='store', help="Path to calculate hash on or path to a file containing multiple paths (one per line). \
															Paths can be in 3 forms:\
															'Users\User\AppData\Local\Temp\svchost.exe', \
															'Users\User\AppData\Local\Temp\svchost.exe', or \
															'\device\harddiskvolume1\Users\User\AppData\Local\Temp\svchost.exe'", required=True)
	parser.add_argument('-b', '--brute_force', action='store_true', help='Iterate possible device paths when calculating Prefetch path hashes')
	args = vars(parser.parse_args())

	path = args['input']
	brute_force = args['brute_force']

	if os.path.exists(path):
		with open(path, 'r') as inny:
			for line in inny:
				if brute_force:
					for possible_device_path in iterate_devices():
						prefetch_hasher = Hasher(filepath=line, device=possible_device_path)
						print(json.dumps(prefetch_hasher.calculate_all(), indent=4, sort_keys=True))
				else:
					prefetch_hasher = Hasher(line)
					print(json.dumps(prefetch_hasher.calculate_all(), indent=4, sort_keys=True))
	else:
		if brute_force:
			for possible_device_path in iterate_devices():
				prefetch_hasher = Hasher(filepath=path, device=possible_device_path)
				print(json.dumps(prefetch_hasher.calculate_all(), indent=4, sort_keys=True))
		else:
			prefetch_hasher = Hasher(path)
			print(json.dumps(prefetch_hasher.calculate_all(), indent=4, sort_keys=True))
