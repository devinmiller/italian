import csv

# Function to convert each line to flashcards format
def convert_to_flashcards(line):
    verb, conjugations = line
    # Strip quotes if present
    verb = verb.strip('"')
    conjugations = conjugations.strip('"')

    # Split the conjugations
    conjugation_list = conjugations.split(', ')

    # Prepare flashcards in the desired format
    flashcards = []
    for conjugation in conjugation_list:
        pronoun, form = conjugation.split(' ')
        flashcard = [f"{pronoun} {verb}", form]
        flashcards.append(flashcard)

    return flashcards

# Function to read input file, convert, and write output file
def process_file(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        flashcards = []

        for line in reader:
            flashcards.extend(convert_to_flashcards(line))

    # Write flashcards to output file
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(flashcards)

    print(f"Conversion complete. Flashcards saved to {output_file}")

# Example usage
input_file = 'italian-conjugations.csv'  # replace with your input file name
output_file = 'output_flashcards.csv'  # replace with your desired output file name

process_file(input_file, output_file)