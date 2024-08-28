import json
import sys
import re
import os
import html
import csv
from bs4 import BeautifulSoup

def find_json_file(term):
    # Sanitize the term to match the file naming convention
    filename = re.sub(r"[ ']", "_", term) + ".json"
    
    # Check if the JSON file exists
    if not os.path.exists(filename):
        print(f"The file {filename} does not exist.")
        return None
    
    return filename

def load_and_prettify_json(filename, term):
    with open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        
        # Process the JSON content to extract the required output
        return process_data(data, term)

def process_data(data, term):
    definitions = []
    examples = []

    for entry in data:
        hits = entry.get("hits", [])
        for hit in hits:
            roms = hit.get("roms", [])
            for rom in roms:
                # Common attributes
                arabs = rom.get("arabs", [])
                definition = ""
                headword = rom.get("headword", "").lower()
                headword_full = BeautifulSoup(rom.get("headword_full", ""), "html.parser")
                headword_full_flexion = headword_full.find("span", class_="flexion")
                flexion = headword_full_flexion.get_text().strip() if headword_full_flexion else ""
                wordclass = rom.get("wordclass", "").lower()

                # For now, let's skip terms that don't match exactly
                if headword != term: continue

                # Get translations from arabs
                translation_output, examples_output = get_translations(arabs)
                
                if wordclass == "adverb":
                    wordclass_acronym = "adv"

                    # Print the formatted output for headword
                    if headword and wordclass_acronym and flexion:
                        definition += f'"{headword}","{wordclass_acronym}. {flexion} '
                    else:
                        definition += f'"{headword}","{wordclass_acronym}. '

                    # Print all arab outputs, separated by semicolons
                    definition += f'{"; ".join(translation_output)}"'
                    definitions.append(definition)

                    # print(definition)

                    # if len(examples_output) > 0:
                    #     print("\n".join(examples_output))
                else:
                    continue

                # Check if wordclass is an adjective
                if wordclass == "adjective and adverb":
                    if headword.endswith('o'):
                        headword += ", -a"
                    elif headword.endswith('e'):
                        headword += ", -i"

                    wordclass_acronym = "adj"

                    if headword and wordclass_acronym and flexion:
                        definition += f'"{headword}","{wordclass_acronym}. {flexion} '
                    else:
                        definition += f'"{headword}","{wordclass_acronym}. '

                    # Print all arab outputs, separated by semicolons
                    definition += f'{"; ".join(translation_output)}"'
                    definitions.append(definition)

                    if len(examples_output) > 0:
                        for example in examples_output:
                            example = re.sub(r'[\t\n]', '', f'{headword}: {example}')
                            examples.append(example)

                    # print(definition)

                    # if len(examples_output) > 0:
                    #     print("\n".join(examples_output))

                # Check if the wordclass is a "verb"
                if wordclass in ["transitive verb", "intransitive verb", "reflexive verb"]:
                    verb_fps_present = ""
                    verb_past_participle = ""
                    verb_auxiliary_verb = "avere"

                    match wordclass:
                        case "intransitive verb":
                            wordclass_acronym = "vi"
                        case "transitive verb":
                            wordclass_acronym = "vt"
                        case "reflexive verb":
                            wordclass_acronym = "vr"
                            verb_auxiliary_verb = "essersi"
                            # For reflexive verbs the headword isn't always the reflexive form
                            headword = headword[:-1] + "si" if not headword.endswith("si") else headword                          
                          
                    if flexion:                         
                        # For verbs, the flexion usually includes irregular forms
                        verb_flexions = flexion.strip()[1:-1].split(',')
                        # First flexion entry should be first person singular conjugation
                        verb_fps_present = f"<{verb_flexions[0].strip()}>"
                        # Third flexion should be the past participle of the verb
                        verb_past_participle = verb_flexions[2].strip() if len(verb_flexions) > 2 else ""

                    headword_full_auxiliary_verb = headword_full.find("span", class_="auxiliary_verb")
                    # The auxiliary verb should only appear in the full headword if not avere
                    # We also first check that the auxiliary verb was changed for a reflexive
                    if headword_full_auxiliary_verb and verb_auxiliary_verb == "avere": verb_auxiliary_verb = "essere"

                    headword_full_sense = headword_full.find("span",class_="sense")
                    verb_headword_sense = headword_full_sense.get_text().strip() if headword_full_sense else ""

                    # Print the formatted output for headword
                    if headword and wordclass_acronym: definition += f'"{headword}","{wordclass_acronym}. '
                    if verb_fps_present: definition += f'{verb_fps_present} '
                    if verb_headword_sense: definition += f'{verb_headword_sense} '

                    # If not set from a flexion follow standard rules
                    if verb_past_participle == "":
                        headword_ending = headword[len(headword)-(4 if wordclass_acronym == "vr" else 3):]
                        match headword_ending:
                            case "are":
                                verb_past_participle = f"{headword[:-3]}ato"
                            case "arsi":
                                verb_past_participle = f"{headword[:-4]}ato"
                            case "ere":
                                verb_past_participle = f"{headword[:-3]}uto"
                            case "ersi":
                                verb_past_participle = f"{headword[:-4]}uto"
                            case "ire":
                                verb_past_participle = f"{headword[:-3]}ito"
                            case "irsi":
                                verb_past_participle = f"{headword[:-4]}ito"
                            
                    # Print all arab outputs, separated by semicolons
                    definition += f'{"; ".join(translation_output)}; {verb_auxiliary_verb} {verb_past_participle}"'
                    definitions.append(definition)

                    if len(examples_output) > 0:
                        for example in examples_output:
                            example = re.sub(r'[\t\n]', '', f'{headword}: {example}')
                            examples.append(example)

                    # print(definition)

                    # if len(examples_output) > 0:
                    #     print("\n".join(examples_output))

                # Check if the wordclass is "noun"
                if wordclass == "noun":
                    
                    wordclass = headword_full.find("span", class_="wordclass")
                    genus = headword_full.find("span", class_="genus")
                    
                    wordclass_acronym = wordclass.find("acronym").get_text().lower() if wordclass else ""
                    genus_acronym = genus.find("acronym").get_text().lower() if genus else ""
                    
                    # Print the formatted output for headword
                    if headword and wordclass_acronym and genus_acronym and flexion:
                        definition += f'"{headword}","{wordclass_acronym}. {genus_acronym}. {flexion} '
                    else:
                        definition += f'"{headword}","{wordclass_acronym}. {genus_acronym}. '
                    
                    # Print all arab outputs, separated by semicolons
                    definition += f'{"; ".join(translation_output)}"'
                    definitions.append(definition)

                    if len(examples_output) > 0:
                        for example in examples_output:
                            example = re.sub(r'[\t\n]', '', f'{headword}: {example}')
                            examples.append(example)

                    # print(definition)

                    # if len(examples_output) > 0:
                    #     print("\n".join(examples_output))
          
    return definitions, examples

def get_translations(arabs):
    # Iterate through arabs and print senses and translations
    arab_output = []
    examples_output = []
    for arab in arabs:
        # Parse the arab header
        arab_header_soup = BeautifulSoup(arab.get("header", ""), "html.parser")
        
        # Not interested in topic specific definitions
        arab_header_topic = arab_header_soup.find("span", class_="topic")
        # Move on to next iteration if topic found
        arab_topic = f"{arab_header_topic.get_text().strip()} " if arab_header_topic else ""

        # Look for a sense on the arab header
        arab_header_sense = arab_header_soup.find("span", class_="sense")
        # Get the sense text if sense found
        arab_sense = f"{arab_header_sense.get_text()} " if arab_header_sense else ""

        # Look for a plural acronym
        arab_header_plural = arab_header_soup.find("acronym", title="plurale")
        # Get the plural text if plural found
        arab_pl = f"{arab_header_plural.get_text()}. " if arab_header_plural else ""

        arab_header_rhetoric = arab_header_soup.find("span", class_="rhetoric")
        arab_rhetoric = f"{arab_header_rhetoric.get_text()}. " if arab_header_rhetoric else ""
        
        translations_output = []
        translations = arab.get("translations", [])
        for translation in translations:
            # Parse the source for each arab translation
            translation_soup = BeautifulSoup(translation.get("source", ""), "html.parser")
            # Check if this is a headword translation
            translation_headword = translation_soup.find("strong", class_="headword")
            # Check if this is a reflexive verb translation
            translation_reflection = translation_soup.find("span", class_="reflection")
            # Check if this is an example
            translation_example = translation_soup.find("span", class_="example")

            # Not interested in topic specific definitions
            translation_topic = translation_soup.find("span", class_="topic")
            # Move on to next iteration if topic found
            topic_text = f"{translation_topic.get_text().strip()} " if translation_topic else ""

            if translation_headword or translation_reflection:
              translation_sense = translation_soup.find("span", class_="sense")
              sense_text = f"{translation_sense.get_text()} " if translation_sense else ""
              target_text = translation.get("target", "").strip()
              translations_output.append(f"{topic_text}{sense_text}{target_text}")

            
            if translation_example:
              translation_rhetoric = translation_soup.find("span", class_="rhetoric")
              example_text = f"{translation_example.get_text()}"
              target_text = remove_html_tags(translation.get("target", ""))

              rhetoric = f"{translation_rhetoric.get_text()}. " if translation_rhetoric else ""

              examples_output.append(f'"{example_text}","{topic_text}{arab_rhetoric}{rhetoric}{target_text}"')
        
        # Combine translation outputs
        if len(translations_output) > 0:
          arab_output.append(f"{arab_topic}{arab_pl}{arab_sense}{', '.join(translations_output)}")
    
    return arab_output, examples_output

def remove_html_tags(data):
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(data, "html.parser")
    
    # Remove all remaining HTML tags
    return soup.get_text()

def save_to_csv(rows, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        # Write each string in the array to a new row
        for row in rows:
            fields = [field.strip() for field in csv.reader([row]).__next__()]
            writer.writerow(fields)

    print(f"Data saved to {filename}")

def save_to_txt(rows, filename):
    with open(filename, 'w', encoding='utf-8') as textfile:
        for row in rows:
            textfile.write(row + '\n')

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <term_or_file>")
        sys.exit(1)
    
    input_arg = sys.argv[1]

    terms_definitions = []
    terms_examples = []
    
    # Check if the input is a file or a single term
    if os.path.isfile(input_arg):
        with open(input_arg, 'r', encoding='utf-8') as file:
            terms = file.readlines()
            terms = [term.strip() for term in terms if term.strip()]  # Remove any leading/trailing whitespace
    else:
        terms = [input_arg]
    
    for term in terms:
        filename = find_json_file(term)
    
        if filename:
            definitions, examples = load_and_prettify_json(filename, term)
            terms_definitions.extend(definitions)
            terms_examples.extend(examples)

    save_to_csv(terms_definitions, "zdefinitions.csv")
    save_to_txt(terms_examples, "zexamples.csv")


if __name__ == "__main__":
    main()
