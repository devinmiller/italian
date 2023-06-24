import csv
import sys

def update_csv_file(filename):
    # Read the data from the file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Update the third column with the value of the first column
    for row in data:
        row[2] = row[0]

    # Write the updated data back to the file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL) # quote all fields
        writer.writerows(data)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    update_csv_file(filename)
