#!/bin/python3

# This Python tool performs reverse DNS lookups using dig for a list of IP addresses and outputs the corresponding domain names.


import subprocess
import sys
import threading
from queue import Queue

# Thread-safe queue to hold IP addresses
ip_queue = Queue()

# Function to perform reverse DNS lookup
def reverse_dns_lookup():
    while not ip_queue.empty():
        ip_address = ip_queue.get()
        try:
            result = subprocess.check_output(['dig', '+short', '-x', ip_address], stderr=subprocess.PIPE).decode().strip()
            if result and not result.startswith(";;"):
                print(f"{ip_address} {result.split()[0]}")
            else:
                print(f"{ip_address} ")
        except subprocess.CalledProcessError:
            print(f"{ip_address} Lookup_failed")
        ip_queue.task_done()

if __name__ == "__main__":
    # Read IP addresses from standard input and add them to the queue
    ips = sys.stdin.readlines()
    for ip in ips:
        ip_queue.put(ip.strip())

    # Create and start 5 threads
    for _ in range(5):
        worker = threading.Thread(target=reverse_dns_lookup)
        worker.daemon = True
        worker.start()

    # Wait for all tasks in the queue to be processed
    ip_queue.join()

