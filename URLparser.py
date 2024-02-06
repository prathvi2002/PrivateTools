#!/bin/python3


"""
https://docs.python.org/3/library/urllib.parse.html


Description: URL Components Extractor is a Python tool that parses URLs from a provided file and extracts their various components, including the scheme, netloc, path, params, query, and fragment. It then prints out both the individual components for each URL and the unique sets of components aggregated from all URLs in the file. This tool is useful for analyzing and understanding the structure of URLs contained within a text file.

"""


from urllib.parse import urlparse
import sys

def parse_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        return parse_urls(urls)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

def parse_urls(urls):
    schemes = set()
    netlocs = set()
    paths = set()
    params_list = set()
    queries_list = set()
    fragments = set()

    for url in urls:
        parsed_url = urlparse(url)
        schemes.add(parsed_url.scheme)
        netlocs.add(parsed_url.netloc)
        paths.add(parsed_url.path)
        params_list.add(parsed_url.params)
        queries_list.add(parsed_url.query)
        fragments.add(parsed_url.fragment)

        # Print individual components for each URL
        print("\n\033[93mURL:", url, "\033[0m")
        print("Scheme:", parsed_url.scheme)
        print("Netloc:", parsed_url.netloc)
        print("Path:", parsed_url.path)
        print("Params:", parsed_url.params)
        print("Query:", parsed_url.query)
        print("Fragment:", parsed_url.fragment)

    # Print unique sets at the end
    print("\n\033[94mUnique components:\033[0m")
    print("Scheme:", list(schemes))
    print("Netloc:", list(netlocs))
    print("Path:", list(paths))
    print("Params:", list(params_list))
    print("Query:", list(queries_list))
    print("Fragment:", list(fragments))

# Example usage:
if __name__ == "__main__":
    # Check if a file path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/url_file.txt")
        sys.exit(1)

    # Extract file path from command-line arguments
    file_path = sys.argv[1]

    # Parse URLs from the file
    parse_urls_from_file(file_path)

