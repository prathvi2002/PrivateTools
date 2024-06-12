# This script reads a word list from a specified file, sorts the lines, takes the first N lines, and prints them to the terminal.

# python3 script.py wordlist.txt 10000


import argparse

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Sort a word list and print the first N lines.")
    parser.add_argument("input_file", type=str, help="The input file containing the word list.")
    parser.add_argument("num_lines", type=int, help="The number of first lines to take after sorting.")
    
    # Parse the arguments
    args = parser.parse_args()

    # Read the word list from the input file
    with open(args.input_file, 'r') as file:
        lines = file.readlines()

    # Sort the lines
    lines.sort()

    # Take the first N lines
    lines = lines[:args.num_lines]

    # Print the sorted list to the terminal
    for line in lines:
        print(line, end='')

if __name__ == "__main__":
    main()

