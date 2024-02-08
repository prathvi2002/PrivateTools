#!/bin/bash
#
# This script will read each domain from the pipe input and perform A and AAAA DNS queries to fetch their IPv4 and IPv6 addresses, printing the results for each domain.
#

# Function to fetch IPv4 address for a domain
get_ipv4() {
    domain="$1"
    ipv4=$(dig +short "$domain" -t a)
    echo "$ipv4"
}

# Function to fetch IPv6 address for a domain
get_ipv6() {
    domain="$1"
    ipv6=$(dig +short "$domain" -t aaaa)
    echo "$ipv6"
}

# Read domains from pipe input
while read -r domain; do
    # Fetch IPv4 and IPv6 addresses for the domain
    ipv4=$(get_ipv4 "$domain")
    ipv6=$(get_ipv6 "$domain")

    # Print domain and its IPv4 and IPv6 addresses
    echo -e "\033[93mDomain: $domain\033[0m"
    echo "IPv4: $ipv4"
    echo "IPv6: $ipv6"
done

# Example usage: cat dns.txt | ./fetch_dns.sh

