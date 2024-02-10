#!/bin/python3

#This tool performs DNS lookups for domain names provided via standard input and prints the first resolved IP address for each domain.

import subprocess
import sys

def dig_lookup(domain):
    try:
        ipv4_address = subprocess.check_output(['dig', '+short', domain, '-t', 'a'], stderr=subprocess.PIPE).decode().strip()
        if ipv4_address and not ipv4_address.startswith(";;"):
            return ipv4_address.split()[0]  # Get the first IP address
    except subprocess.CalledProcessError:
        try:
            ipv6_address = subprocess.check_output(['dig', '+short', domain, '-t', 'aaaa'], stderr=subprocess.PIPE).decode().strip()
            if ipv6_address and not ipv6_address.startswith(";;"):
                return ipv6_address.split()[0]  # Get the first IP address
        except subprocess.CalledProcessError:
            pass  # Connection error, do nothing
    return None

if __name__ == "__main__":
    # Read domain names from pipe
    domains = sys.stdin.readlines()
    resolved_domains = {}
    for domain in domains:
        domain = domain.strip()
        if domain not in resolved_domains:
            ip = dig_lookup(domain)
            if ip:
                resolved_domains[domain] = ip
                # Print resolved domain immediately
                print(f"\033[93m{domain}\033[0m \033[94m{ip}\033[0m")
                #print(f"{domain} {ip}")


