# DomainHarvester

## Overview

The tool, named 'DomainHarvester,' is designed to extract domains and subdomains from the source code of a list of URLs provided in a text file. It utilizes web scraping techniques to fetch the HTML content of each URL and subsequently parses the HTML to identify and extract unique domains and subdomains. The extracted domains and subdomains are then displayed in the terminal.

## Features

- Extract domains and subdomains from the source code of a list of URLs.
- Utilizes web scraping techniques to fetch HTML content.
- Identifies and extracts unique domains and subdomains.
- Outputs results to the terminal.

## Usage

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/DomainHarvester.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd DomainHarvester
    ```

3. **Run the Script:**

    ```bash
    python domain_harvester.py path/to/url_file.txt
    ```

    Replace `path/to/url_file.txt` with the actual path to your text file containing the list of URLs.

## Example

Suppose you have a file named `urls.txt` with the following content:

```text
https://example1.com
https://example2.com
https://example3.com
