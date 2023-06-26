import csv
import argparse
from collections import OrderedDict

def remove_duplicates(file_path):
    # Read the file and remove duplicates
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = OrderedDict()

        for row in reader:
            # Use the first column as the key, and ignore duplicates
            if row[0] not in data:
                data[row[0]] = row

    # Write the unique rows back to the same file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(data.values())

def main():
    parser = argparse.ArgumentParser(description='Remove duplicates from a CSV file based on the contents of the first column.')
    parser.add_argument('file_path', help='The CSV file to edit in-place.')
    args = parser.parse_args()

    remove_duplicates(args.file_path)

if __name__ == "__main__":
    main()
