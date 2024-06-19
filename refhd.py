#!/bin/bash

# reflection detection in http response headers
# This script reads each URL, modifies it according to the specified conditions, makes a curl request to the modified URL, and checks if the random strings are present in the response headers. If found, it prints the relevant details to the terminal.
# These are those specified conditions: If the URL contains query parameters, replace each parameter value with a randomly generated string. If the URL is the root URL (ends with /), append a randomly generated string to the URL path. If the URL is an endpoint without query parameters, append / followed by a randomly generated string to the endpoint path.

# python3 refh.py urls.txt | tee results.txt 
# cat results.txt | grep -A 2 "Random string" | grep "Header:" | cut -f3 -d" "

import subprocess
import sys
import urllib.parse
import random
import string
import re

def generate_random_string(length=8):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def modify_url(url):
    """Modify the URL based on specified conditions."""
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    path = parsed_url.path

    random_strings = []

    if query_params:
        # Condition 1: URL has query parameters
        modified_query = {key: generate_random_string() for key in query_params}
        random_strings = list(modified_query.values())
        new_query = urllib.parse.urlencode(modified_query)
        modified_url = parsed_url._replace(query=new_query).geturl()
    elif path == '/':
        # Condition 2: URL is the root URL
        random_segment = generate_random_string()
        random_strings = [random_segment]
        modified_url = f"{url.rstrip('/')}/{random_segment}"
    else:
        # Condition 3: URL endpoint has no query parameter
        random_segment = generate_random_string()
        random_strings = [random_segment]
        modified_url = f"{url.rstrip('/')}/{random_segment}"

    return modified_url, random_strings

def make_curl_request(url):
    """Make a curl request to the given URL and return the response headers."""
    try:
        result = subprocess.run(['curl', '-s', '-I', url], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def check_response_for_random_strings(response, random_strings):
    """Check if any of the random strings are present in the response headers."""
    for random_string in random_strings:
        if re.search(re.escape(random_string), response):
            return random_string
    return None

def main(file_path):
    """Main function to read URLs from the file, modify them, make curl requests, and check responses."""
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
        
        for url in urls:
            url = url.strip()
            if url:
                modified_url, random_strings = modify_url(url)
                print(f"\n\nRequesting URL: {modified_url}")
                response = make_curl_request(modified_url)
                print(response)
                found_string = check_response_for_random_strings(response, random_strings)
                if found_string:
                    print(f"Random string '{found_string}' found in response for URL: {modified_url}")
                    headers = response.split('\n')
                    for header in headers:
                        if found_string in header:
                            print(f"Header: {header.strip()}")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    """Entry point of the script."""
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        main(file_path)

