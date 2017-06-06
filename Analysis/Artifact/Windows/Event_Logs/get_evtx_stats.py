#!/usr/bin/env python

# created by Glenn P. Edwards Jr.
#   http://hiddenillusion.blogspot.com
#       @hiddenillusion
# Date: 2016-03-30
# (while at FireEye)

from collections import OrderedDict
from datetime import datetime
import os
import sys

def doWork(filepath):
	with open(filepath, "rb") as fobj:
		evtx_file = pyevtx.file()
		evtx_file.open_file_object(fobj)

		details = OrderedDict()
		total_records = evtx_file.get_number_of_records()
		if not total_records > 0:
			first_record = "N/A"
			last_record = "N/A"
		else:
			evtx_log_timestamps = []
			for record_index, evtx_record in enumerate(evtx_file.records):
				# Don't want any 1601-01-01 00:00:00
				if not evtx_record.get_written_time_as_integer() == 0:
					evtx_log_timestamps.append(evtx_record.get_written_time())

			summarized = sorted(evtx_log_timestamps, key=lambda ts: datetime)
			first_record = min(summarized)
			last_record = max(summarized)
					
		details['first_record'] = first_record
		details['last_record'] = last_record
		details['total_records'] = total_records
		details['evtx_filepath'] = os.path.abspath(filepath) 

		return details

def recurse_path(path):
	if os.path.isdir(path):
		for root, dirs, files in os.walk(path):
			dirs.sort()
			for name in sorted(files):
				fname = os.path.join(root, name)
				yield fname
	else:
		yield path

if __name__ == '__main__':
	import argparse
	try:
		import pyevtx
	except ImportError:
		print("[!] pyevtx required : https://github.com/libyal/libevtx/wiki/Building")
		sys.exit(1)

	parser = argparse.ArgumentParser(description='Provides summary details for Windows EVTX Event Logs')
	parser.add_argument('-i', '--input', action='store', help='Path to EVTX file(s)', required=True)
	args = vars(parser.parse_args())

	path = args['input']
	cnt = 0
	for filepath in recurse_path(path):
		evtx_details = doWork(filepath)
		if cnt == 0:
			print('\t'.join('{0}'.format(k) for k,v in evtx_details.iteritems()))

		print('\t'.join('{0}'.format(v) for k,v in evtx_details.iteritems()))