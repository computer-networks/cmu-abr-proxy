#!/usr/bin/env python3
import sys
import requests
import time
import logging
import argparse
from threading import Thread
from util import strip_comments

MANIFEST_TEMPLATE = 'http://127.0.0.1:%s/vod/big_buck_bunny.f4m'
URL_TEMPLATE = 'http://127.0.0.1:%s/vod/%sSeg2-Frag7'

def simple_fetcher(id, port, bitrate, interval, number, outcome_list):
	sess = requests.Session()
	count = 0
	chunk_time_list = []

	while count < number:
		chunk_start_time = get_millliseconds()
		content = sess.get(URL_TEMPLATE % (port, bitrate))
		chunk_end_time = get_millliseconds()

		logging.getLogger(__name__).debug('Fetched chunk %d using time %fs.\n' % (count, (chunk_end_time - chunk_start_time) / 1000))
		chunk_time_list.append(chunk_end_time - chunk_start_time)

		time.sleep(interval)
		count += 1

	sum_time = 0
	for chunk_time in chunk_time_list:
		sum_time += chunk_time

	logging.getLogger(__name__).debug('Fetched %d %dbitrate chunk with interval %fs. The mean fetching time is %f' %
		(count, bitrate, interval, sum_time / (count * 1000)))

	outcome_list.append((id, sum_time / (count * 1000)))


def get_millliseconds():
	return int(round(time.time() * 1000))


def execute_event(id, wait_time, port, bitrate, interval, count, thread):

	time.sleep(wait_time)
	thread_set = []
	outcome_list = []

	if args.log:
		with open(args.log, 'a') as logfile:
			logfile.write('Command id %d start\n' % id)
		logfile.closed

	for i in range(thread):
		thread_set.append(Thread(target=simple_fetcher, args=(i, port, bitrate, interval, count, outcome_list)))

	for thread in thread_set:
		thread.start()

	for thread in thread_set:
		thread.join()

	if args.log:
		with open(args.log, 'a') as logfile:
			logfile.write('id: %d, [%s]\n' % (id, ', '.join(map(str, outcome_list))))
		logfile.closed

if __name__ == "__main__":
	# set up command line args
	parser = argparse.ArgumentParser(description='Generate a load to the target port according to events file')
	parser.add_argument('-e', '--events', required=True, help='events files.')
	parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Print debug message.')
	parser.add_argument('-l', '--log', default=None, help='The log filename, a log would be printed in this file if a filename is given.')
	args = parser.parse_args()
	
	# set up logging
	if args.verbose:
		level = logging.DEBUG
	else:
		level = logging.INFO

	logging.basicConfig(
		format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno) -7s %(message)s",
		level = level
	)

	# Read event list
	events = []
	with open(args.events) as events_file:
		for i, line in enumerate(strip_comments(events_file)):
			arguments = line.split(' ')
			events.append(Thread(target=execute_event, args=(i, float(arguments[0]), int(arguments[1]), 
				int(arguments[2]), float(arguments[3]), int(arguments[4]), int(arguments[5]))))
	events_file.closed

	for event in events:
		event.start()

	for event in events:
		event.join()

	logging.getLogger(__name__).info('Events finished')



