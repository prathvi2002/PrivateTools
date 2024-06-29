# This script will process multiple URLs concurrently, modify them as required, and check for the presence of specified random strings in the response body. Adjust the max_workers parameter in ThreadPoolExecutor to control the level of concurrency.
# Modifies the URLs based on specified conditions: replace query parameter values, append random strings to root URLs, removes the query parameters and adds a random string at the end of the endpoint, or add a random segment to endpoint paths without query parameters. Additionally, add fragments (#<random-string>) to check for reflection, preserving original query parameter values.

# refbd2.py urls.txt | tee results.txt
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
    modified_urls = []

    if query_params:
        # Condition 1: URL has query parameters
        modified_query = {key: generate_random_string() for key in query_params}
        random_strings = list(modified_query.values())
        new_query = urllib.parse.urlencode(modified_query)
        modified_urls.append(parsed_url._replace(query=new_query).geturl())

        # Adding fragment to query parameters, preserving original values
        fragment_string = generate_random_string()
        random_strings.append(fragment_string)
        modified_urls.append(parsed_url.geturl() + f"#{fragment_string}")

        # Removing query parameters and adding a random string to the endpoint
        random_segment = generate_random_string()
        random_strings.append(random_segment)
        modified_urls.append(parsed_url._replace(query="").geturl().rstrip('/') + f"/{random_segment}")

    if path == '/':
        # Condition 2: URL is the root URL
        random_segment = generate_random_string()
        random_strings = [random_segment]
        modified_urls.append(f"{url.rstrip('/')}/{random_segment}")

        # Adding fragment to root URL
        fragment_string = generate_random_string()
        random_strings.append(fragment_string)
        modified_urls.append(f"{url.rstrip('/')}/#{fragment_string}")
    else:
        # Condition 3: URL endpoint has no query parameter
        random_segment = generate_random_string()
        random_strings = [random_segment]
        modified_urls.append(f"{url.rstrip('/')}/{random_segment}")

        # Adding fragment to endpoint paths without query parameters
        fragment_string = generate_random_string()
        random_strings.append(fragment_string)
        modified_urls.append(f"{url.rstrip('/')}/#{fragment_string}")

    return modified_urls, random_strings

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
        for modified_url in modified_urls:
            print(f"\n\nRequesting URL: {modified_url}")
            response = make_curl_request(modified_url)
            found_string = check_response_for_random_strings(response, random_strings)
            if found_string:
                print(f"Random string '{found_string}' found in response for URL: {modified_url}")
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

