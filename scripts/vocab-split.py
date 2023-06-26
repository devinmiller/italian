import csv
import random
import sys

def shuffle_csv(input_file, output_prefix, block_size, start_index):
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    random.shuffle(data)

    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        with open(f'{output_prefix}-{i//block_size+start_index}-vocabulary.csv', 'w', newline='') as f:
            writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(block)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: python script.py [input_file] [output_prefix] [start_index]')
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_prefix = sys.argv[2]
    start_index = int(sys.argv[3])
    shuffle_csv(input_file, output_prefix, 25, start_index)
