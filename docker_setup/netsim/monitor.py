#!/usr/bin/env python

import sys
import os
import signal
import time
import argparse
from util import check_output, check_both, run_bg, strip_comments
from threading import Thread
from subprocess import Popen, PIPE

counters = []
server_ports = []
count_dict = {}

def count_connection(port, count_dict):
    count = 0
    p = Popen(('tcpdump', '-i', 'lo', 'src port %d' % port), stdout=PIPE)
    for row in iter(p.stdout.readline, b''):
        if len(row.split(' ')) < 21:
            continue
        try:
            count += int(filter(str.isdigit, row.split(" ")[20]))
        except Exception as e:
            print(row.split(" ")[20].strip())
    count_dict[port] = '%f MB' % (float(count) / (1024 * 1024))

def terminate_counters():
    check_both('killall tcpdump', False, False)

def start_counters():

    for port in server_ports:
        counters.append(Thread(target=count_connection, args=(port, count_dict)))

    for counter in counters:
        counter.start()

def sig_terminal_handler(signum, frame):
    terminate_counters()
    for counter in counters:
        counter.join()
    print(count_dict)

def main():
    terminate_counters()

    with open(args.servers) as servers_file:
        for line in strip_comments(servers_file):
            server_ports.append(int(line))
        servers_file.closed

    start_counters()
    signal.signal(signal.SIGINT, sig_terminal_handler)


if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(description='Monitor the load on server ports')
    parser.add_argument('-s', '--servers', help='the file contains the port number of servers needed to be created in server mode')
    args = parser.parse_args()
    
    main()
