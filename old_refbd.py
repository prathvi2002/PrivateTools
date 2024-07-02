# THIS DO NOT modify URLs by removing query parameters, appending a randomly generated segment in formats /?<random-segment> and /<random-segment>. For the workaround of this limitation get all the urls with query parameters, remove the query parameters from those urls and add these urls without query parameters in the file with urls.

# This script will process multiple URLs concurrently, modify them as required, and check for the presence of specified random strings in the response body. Adjust the max_workers parameter in ThreadPoolExecutor to control the level of concurrency.
# Modify the URLs based on specified conditions: replace query parameter values, append random strings to root URLs, or add a random segment to endpoint paths without query parameters.

# also handle URLs that are root URLs (i.e., http://example.com or http://example.com/) by appending a "?" and a random string in the format http://example.com/?<random-string>.

# also handle URL endpoints (i.e., http://example.com/main/shop/ or http://example.com/main/shop) by appending a "?" and a random string in the format http://example.com/main/shop/?<random-string> | http://example.com/main/shop/<random-string>?.

# refbd.py urls.txt | tee results.txt
# cat results.txt | grep "Random string"

import subprocess
import sys
import urllib.parse
import random
import string
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        modified_url = [
                f"{url.rstrip('/')}/?{random_segment}",
                f"{url.rstrip('/')}/{random_segment}"
            ]
    else:
        # Condition 3: URL endpoint has no query parameter
        random_segment1 = generate_random_string()
        random_segment2 = generate_random_string()
        random_strings = [random_segment1, random_segment2]
        modified_url = [
            f"{url.rstrip('/')}/?{random_segment1}",
            f"{url.rstrip('/')}/{random_segment2}"
        ]

    return modified_url, random_strings

def make_curl_request(url):
    """Make a curl request to the given URL and return the response body."""
    try:
        result = subprocess.run(['curl', '-k', '-s', url], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def check_response_for_random_strings(response, random_strings):
    """Check if any of the random strings are present in the response body."""
    for random_string in random_strings:
        if re.search(re.escape(random_string), response):
            return random_string
    return None

def process_url(url):
    """Process each URL: modify, make curl request, and check response."""
    try:
        modified_urls, random_strings = modify_url(url)
        if isinstance(modified_urls, list):
            for modified_url in modified_urls:
                print(f"\n\nRequesting URL: {modified_url}")
                response = make_curl_request(modified_url)
                found_string = check_response_for_random_strings(response, random_strings)
                if found_string:
                    print(f"Random string '{found_string}' found in response for URL: {modified_url}")
        else:
            print(f"\n\nRequesting URL: {modified_urls}")
            response = make_curl_request(modified_urls)
            found_string = check_response_for_random_strings(response, random_strings)
            if found_string:
                print(f"Random string '{found_string}' found in response for URL: {modified_urls}")
    except Exception as e:
        print(f"Error processing URL {url}: {e}")

def main(file_path):
    """Main function to read URLs from the file and process them concurrently."""
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()

        # Using ThreadPoolExecutor to process URLs concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
            # Submitting tasks for each URL
            futures = [executor.submit(process_url, url.strip()) for url in urls]

            # Iterate over completed futures to handle exceptions if any
            for future in as_completed(futures):
                try:
                    future.result()  # Retrieve result to handle exceptions if any
                except Exception as e:
                    print(f"Exception occurred: {e}")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    """Entry point of the script."""
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        main(file_path)
