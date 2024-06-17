#!/bin/python3

# This tool performs DNS lookups for domain names provided via standard input and prints the first resolved IP address for each domain. It prioritizes checking for the IPv4 address (A record) of each domain. If the IPv4 address is found, it prints it and moves to the next domain without checking for the IPv6 address. Only if the IPv4 address is not found, it then checks for the IPv6 address (AAAA record). If neither IPv4 nor IPv6 addresses are found, it moves to the next domain.

# just change the max_workers number on line 42 to increase or decrease the speed

import subprocess
import sys
import concurrent.futures

def dig_lookup(domain):
    try:
        ipv4_address = subprocess.check_output(['dig', '+short', domain, '-t', 'a'], stderr=subprocess.PIPE).decode().strip()
        if ipv4_address and not ipv4_address.startswith(";;"):
            return ipv4_address.split()[0]  # Get the first IP address
    except subprocess.CalledProcessError:
        pass
    
    try:
        ipv6_address = subprocess.check_output(['dig', '+short', domain, '-t', 'aaaa'], stderr=subprocess.PIPE).decode().strip()
        if ipv6_address and not ipv6_address.startswith(";;"):
            return ipv6_address.split()[0]  # Get the first IP address
    except subprocess.CalledProcessError:
        pass  # Connection error, do nothing
    
    return None

def resolve_domain(domain):
    domain = domain.strip()
    ip = dig_lookup(domain)
    if ip:
        # Print resolved domain immediately with color formatting
        print(f"\033[93m{domain}\033[0m \033[94m{ip}\033[0m")
    return domain, ip

if __name__ == "__main__":
    # Read domain names from pipe
    domains = sys.stdin.readlines()
    resolved_domains = {}
    
    # Use ThreadPoolExecutor to perform DNS lookups concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_domain = {executor.submit(resolve_domain, domain): domain for domain in domains}
        for future in concurrent.futures.as_completed(future_to_domain):
            domain, ip = future.result()
            if ip:
                resolved_domains[domain] = ip
