import csv
import sys

def compare_files(file1, file2, output_file):
    # Load the first column of the first CSV file
    with open(file1, 'r') as f:
        file1_data = [row[0] for row in csv.reader(f)]

    # Load all the rows from the second CSV file
    with open(file2, 'r') as f:
        file2_data = list(csv.reader(f))

    # Remove rows from the second CSV file if their first column matches the first column of any row in the first CSV file
    file2_data = [row for row in file2_data if row[0] not in file1_data]

    # Write the result to a new CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file2_data)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: python script.py <file1.csv> <file2.csv> <output_file.csv>')
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]

    compare_files(file1, file2, output_file)
