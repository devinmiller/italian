import csv
import sys

def compare_files(file1, file2):
    # Load the first column of the first CSV file
    with open(file1, 'r') as f:
        file1_data = [row[0] for row in csv.reader(f)]

    # Load all the rows from the second CSV file
    with open(file2, 'r') as f:
        file2_data = list(csv.reader(f))

    # Remove rows from the second CSV file if their first column matches the first column of any row in the first CSV file
    file2_data = [row for row in file2_data if row[0] not in file1_data]

    # Write the result back to the second CSV file with all fields surrounded by double quotes
    with open(file2, 'w', newline='') as f:
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerows(file2_data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python script.py <file1.csv> <file2.csv>')
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    compare_files(file1, file2)
