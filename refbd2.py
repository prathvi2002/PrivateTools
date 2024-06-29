# The script removes query parameters from URLs, appends a random string after a '/', makes a curl request, and checks if the random string is present in the response.

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
    """Modify the URL to remove query parameters and add a random string after a '/'."""
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path.rstrip('/')
    random_string = generate_random_string()
    modified_url = f"{parsed_url.scheme}://{parsed_url.netloc}{path}/{random_string}"
    return modified_url, random_string

def make_curl_request(url):
    """Make a curl request to the given URL and return the response body."""
    try:
        result = subprocess.run(['curl', '-k', '-s', url], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def check_response_for_random_string(response, random_string):
    """Check if the random string is present in the response body."""
    if re.search(re.escape(random_string), response):
        return random_string
    return None

def process_url(url):
    """Process each URL: modify, make curl request, and check response."""
    try:
        modified_url, random_string = modify_url(url)
        print(f"\n\nRequesting URL: {modified_url}")
        response = make_curl_request(modified_url)
        found_string = check_response_for_random_string(response, random_string)
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

