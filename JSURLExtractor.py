#!/bin/python3


# Extracts JavaScript URLs from src attributes of script tags from a list of provided URLs in a text file


import sys
import requests
from bs4 import BeautifulSoup

def extract_js_urls_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            js_urls = [script.get('src') for script in soup.find_all('script', src=True)]
            return js_urls
        else:
            print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while processing {url}: {str(e)}")

def main():
    # Check if a file path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/url_file.txt")
        sys.exit(1)

    # Extract file path from command-line arguments
    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as file:
            # Read URLs from the file
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

    all_js_urls = []

    for url in urls:
        js_urls = extract_js_urls_from_url(url)
        if js_urls:
            print(f"\n\033[93mJavaScript URLs found in {url}:\033[0m")
            for js_url in js_urls:
                print(js_url)
            all_js_urls.extend(js_urls)

    print("\n\033[94mAll unique JavaScript URLs:\033[0m")
    unique_js_urls = list(set(all_js_urls))
    for js_url in unique_js_urls:
        print(js_url)

if __name__ == "__main__":
    main()

