#!/usr/bin/env python3
import sys
import requests
import time
import logging
import argparse
from threading import Thread

IP='127.0.0.1'
MANIFEST_TEMPLATE = 'http://%s:%s/vod/big_buck_bunny.f4m'
URL_TEMPLATE = 'http://%s:%s/vod/%sSeg%s-Frag%s'

# A generator returning each line in a file with comments removed
# f is an open file object
def strip_comments(f):
    for line in f:
        if '#' in line:
            line = line.split('#')[0]
        line = line.strip()
        if line != '':
            yield line

def get_millliseconds():
    return int(round(time.time() * 1000))

def simple_fetcher(id, bitrate, seg_id, frag_id, outcome_list, port):
    sess = requests.Session()
    count = 0
    chunk_time_list = []

    while count < 1:
        start_t = get_millliseconds()
        content = sess.get(URL_TEMPLATE % (IP, port, bitrate, seg_id, frag_id))
        end_t = get_millliseconds()
        logging.getLogger(__name__).debug('Fetched chunk %d in %f sec.\n' %
                                          (count, (end_t - start_t) / 1000))
        chunk_time_list.append(end_t - start_t)
        count += 1

    sum_time = 0
    for chunk_time in chunk_time_list:
        sum_time += chunk_time

    logging.getLogger(__name__).info('Fetched %d %dbitrate chunk. Mean '
                                     'fetching time is %f sec' %
                                     (count, bitrate,
                                      sum_time / (count * 1000)))
    outcome_list.append((id, sum_time / (count * 1000)))

def execute_event(id, wait_time, bitrate, seg_id, frag_id, port):
    time.sleep(wait_time)
    thread_set = []
    outcome_list = []

    if args.log:
        with open(args.log, 'a') as logfile:
            logfile.write('Command id %d start\n' % id)
        logfile.closed

    simple_fetcher(i, bitrate, seg_id, frag_id, outcome_list, port)

    if args.log:
        with open(args.log, 'a') as logfile:
            logfile.write('id: %d, [%s]\n' % (id, ', '.join(map(str,
                                                                outcome_list))))
        logfile.closed

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(description='Generate a load to the target'
                                     ' port according to events file')
    parser.add_argument('-e', '--events', required=True, help='events files.')
    parser.add_argument('-p', '--port', required=True, help='the port to connect to')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Print debug message.')
    parser.add_argument('-l', '--log', default=None, help='Log filename, logs '
                        'would be printed to this file if a filename is given.')
    args = parser.parse_args()

    # set up logging
    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
	format = "%(levelname) -2s %(asctime)s.%(msecs)03d %(module)s:%(lineno)"
                 " -5s %(message)s",
        datefmt = '%Y-%m-%d %H:%M:%S',
	level = level
    )

    # Read event list
    events = []
    with open(args.events) as events_file:
        for i, line in enumerate(strip_comments(events_file)):
            argv = line.split(' ')
            events.append(Thread(target=execute_event,
                          args=(i, float(argv[0]), int(argv[1]),
				                int(argv[2]), int(argv[3]), args.port)))
    events_file.closed

    sess = requests.Session()
    content = sess.get(MANIFEST_TEMPLATE % (IP, args.port))
    logging.getLogger(__name__).info('Fetched manifest of length %d' % len(content.content))

    for event in events:
        event.start()

    for event in events:
        event.join()

    logging.getLogger(__name__).info('Events finished')
