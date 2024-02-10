#!/bin/python3

# This Python script takes input from standard input in the form of lines, where each line contains a domain name and its corresponding IP address separated by whitespace. It then runs the nmap command for each IP address to perform a full port scan.

# Works for both IPV4 and IPV6 addresses.

import subprocess
import sys

def run_nmap(ip):
    try:
        # Check if IP is IPv6
        is_ipv6 = ':' in ip
        # Run the provided nmap command
        #nmap_command = f"nmap -p- {'-6 ' if is_ipv6 else ''}{ip} | awk -F/ '/[0-9]+\/tcp/{{print $1}}'"
        nmap_command = f"nmap -p- {'-6 ' if is_ipv6 else ''}{ip} | awk -F/ '/[0-9]+\/tcp/{{printf \"%s%s\", sep, $1; sep=\",\"}} END {{printf \"\"}}'"
        nmap_output = subprocess.check_output(nmap_command, shell=True).decode().strip()
        return nmap_output
    except subprocess.CalledProcessError as e:
        return f"Error running nmap: {e}"

if __name__ == "__main__":
    # Read domain names and IPs from standard input
    for line in sys.stdin:
        parts = line.strip().split()
        if len(parts) == 2:
            domain, ip = parts
            # Run nmap command for the IP address
            result = run_nmap(ip)
            # Print domain and nmap results
            print(f"{domain} {result}")
        else:
            print(f"Skipping invalid input: {line.strip()}")
