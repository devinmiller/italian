# A file to sort the master vocabulary list

import csv
import sys

def sort_csv_file(filename):
    # Read the csv file
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    # Sort the data
    data.sort(key=lambda row: row[0])

    # Write the sorted data back to the file
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(data)

# Boilerplate main entry
if __name__ == "__main__":
    # Call the function with your filename from command line arguments
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Please provide a filename as a command line argument.")
        sys.exit(1)

    sort_csv_file(filename)
