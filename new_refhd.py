# This script will process multiple URLs concurrently, modify them as required, and check for the presence of specified random strings in the response body. Adjust the max_workers parameter in ThreadPoolExecutor to control the level of concurrency.
# Modify the URLs based on specified conditions: replace query parameter values, append random strings to root URLs, or add a random segment to endpoint paths without query parameters.

# also handle URLs that are root URLs (i.e., http://example.com or http://example.com/) by appending a "?" and a random string in the format http://example.com/?<random-string>.

# also handle URL endpoints (i.e., http://example.com/main/shop/ or http://example.com/main/shop) by appending a "?" and a random string in the format http://example.com/main/shop/?<random-string> | http://example.com/main/shop/<random-string>?.

# also modify URLs by removing query parameters and appending random segments in formats /?<random-segment> and /<random-segment>, then make requests to these modified URLs.

# refbd.py urls.txt | tee results.txt
# cat results.txt | grep "Random string"

import subprocess as subprocess_xx1
import sys as sys_xx1
import urllib.parse as urllib_parse_xx1
import random as random_xx1
import string as string_xx1
import re as re_xx1
from concurrent.futures import ThreadPoolExecutor as ThreadPoolExecutor_xx1, as_completed as as_completed_xx1

def generate_random_string_xx1(length=8):
    """Generate a random string of fixed length."""
    return ''.join(random_xx1.choices(string_xx1.ascii_letters + string_xx1.digits, k=length))

def modify_url_xx1(url_xx1):
    """Modify the URL based on specified conditions."""
    parsed_url_xx1 = urllib_parse_xx1.urlparse(url_xx1)
    query_params_xx1 = urllib_parse_xx1.parse_qs(parsed_url_xx1.query)
    path_xx1 = parsed_url_xx1.path

    random_strings_xx1 = []

    if query_params_xx1:
        # Condition 1: URL has query parameters
        modified_query_xx1 = {key_xx1: generate_random_string_xx1() for key_xx1 in query_params_xx1}
        random_strings_xx1 = list(modified_query_xx1.values())
        new_query_xx1 = urllib_parse_xx1.urlencode(modified_query_xx1)
        modified_url_xx1 = parsed_url_xx1._replace(query=new_query_xx1).geturl()
    elif path_xx1 == '/':
        # Condition 2: URL is the root URL
        random_segment_xx1 = generate_random_string_xx1()
        random_strings_xx1 = [random_segment_xx1]
        modified_url_xx1 = [
                f"{url_xx1.rstrip('/')}/?{random_segment_xx1}",
                f"{url_xx1.rstrip('/')}/{random_segment_xx1}"
            ]
    else:
        # Condition 3: URL endpoint has no query parameter
        random_segment1_xx1 = generate_random_string_xx1()
        random_segment2_xx1 = generate_random_string_xx1()
        random_strings_xx1 = [random_segment1_xx1, random_segment2_xx1]
        modified_url_xx1 = [
            f"{url_xx1.rstrip('/')}/?{random_segment1_xx1}",
            f"{url_xx1.rstrip('/')}/{random_segment2_xx1}"
        ]

    return modified_url_xx1, random_strings_xx1

def make_curl_request_xx1(url_xx1):
    """Make a curl request to the given URL and return the response body."""
    try:
        result_xx1 = subprocess_xx1.run(['curl', '-k', '-s', '-i', url_xx1], capture_output=True, text=True)
        return result_xx1.stdout
    except Exception as e_xx1:
        return f"Error: {e_xx1}"

def check_response_for_random_strings_xx1(response_xx1, random_strings_xx1):
    """Check if any of the random strings are present in the response body."""
    for random_string_xx1 in random_strings_xx1:
        if re_xx1.search(re_xx1.escape(random_string_xx1), response_xx1):
            return random_string_xx1
    return None

def process_url_xx1(url_xx1):
    """Process each URL: modify, make curl request, and check response."""
    try:
        modified_urls_xx1, random_strings_xx1 = modify_url_xx1(url_xx1)
        if isinstance(modified_urls_xx1, list):
            for modified_url_xx1 in modified_urls_xx1:
                print(f"\n\nRequesting URL: {modified_url_xx1}")
                response_xx1 = make_curl_request_xx1(modified_url_xx1)
                found_string_xx1 = check_response_for_random_strings_xx1(response_xx1, random_strings_xx1)
                if found_string_xx1:
                    print(f"Random string '{found_string_xx1}' found in response for URL: {modified_url_xx1}")
        else:
            print(f"\n\nRequesting URL: {modified_urls_xx1}")
            response_xx1 = make_curl_request_xx1(modified_urls_xx1)
            found_string_xx1 = check_response_for_random_strings_xx1(response_xx1, random_strings_xx1)
            if found_string_xx1:
                print(f"Random string '{found_string_xx1}' found in response for URL: {modified_urls_xx1}")
    except Exception as e_xx1:
        print(f"Error processing URL {url_xx1}: {e_xx1}")

def main_xx1(file_path_xx1):
    """Main function to read URLs from the file and process them concurrently."""
    try:
        with open(file_path_xx1, 'r') as file_xx1:
            urls_xx1 = file_xx1.readlines()

        # Using ThreadPoolExecutor to process URLs concurrently
        with ThreadPoolExecutor_xx1(max_workers=5) as executor_xx1:  # Adjust max_workers as needed
            # Submitting tasks for each URL
            futures_xx1 = [executor_xx1.submit(process_url_xx1, url_xx1.strip()) for url_xx1 in urls_xx1]

            # Iterate over completed futures to handle exceptions if any
            for future_xx1 in as_completed_xx1(futures_xx1):
                try:
                    future_xx1.result()  # Retrieve result to handle exceptions if any
                except Exception as e_xx1:
                    print(f"Exception occurred: {e_xx1}")
    except Exception as e_xx1:
        print(f"Error reading file: {e_xx1}")

if __name__ == "__main__":
    """Entry point of the script."""
    if len(sys_xx1.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path_xx1 = sys_xx1.argv[1]
        main_xx1(file_path_xx1)





# the below code is for modifying URLs by removing query parameters, appending a randomly generated segment in formats /?<random-segment> and /<random-segment>
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
        path_without_query = parsed_url._replace(query='').geturl().rstrip('/')
        random_segment = generate_random_string()
        random_strings = [random_segment]
        modified_url = [
            f"{path_without_query}/?{random_segment}",
            f"{path_without_query}/{random_segment}"
        ]

    return modified_url, random_strings


def make_curl_request(url):
    """Make a curl request to the given URL and return the response body."""
    try:
        result = subprocess.run(['curl', '-k', '-s', '-i', url], capture_output=True, text=True)
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