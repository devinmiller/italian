import json
import sys
import re
import os
import html
from bs4 import BeautifulSoup

def find_json_file(term):
    # Sanitize the term to match the file naming convention
    filename = re.sub(r"[ ']", "_", term) + ".json"
    
    # Check if the JSON file exists
    if not os.path.exists(filename):
        print(f"The file {filename} does not exist.")
        return None
    
    return filename

def load_and_prettify_json(filename):
    with open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        
        # Process the JSON content to extract the required output
        process_data(data)

def process_data(data):
    for entry in data:
        hits = entry.get("hits", [])
        for hit in hits:
            roms = hit.get("roms", [])
            for rom in roms:
                headword_flexion = ""
                definition = ""

                # Check if wordclass is an adjective
                if rom.get("wordclass", "").lower() == "adjective and adverb":
                    headword = rom.get("headword", "")
                    if headword.endswith('o'):
                        headword += ", -a"
                    elif headword.endswith('e'):
                        headword += ", -i"

                    wordclass_acronym = "adj"

                    if headword and wordclass_acronym:
                        definition += f'"{headword}","{wordclass_acronym}. '

                    # Get translations from arabs
                    arabs = rom.get("arabs", [])
                    arab_output, examples_output = get_translations(arabs)
                    # Print all arab outputs, separated by semicolons
                    definition += f'{"; ".join(arab_output)}"'
                    print(definition)
                    print("\n".join(examples_output))

                # Check if the wordclass is a "verb"
                if rom.get("wordclass", "").lower() in ["transitive verb", "intransitive verb", "reflexive verb"]:
                    headword = rom.get("headword", "")
                    wordclass = rom.get("wordclass", "").lower()
                    past_participle = ""
                    auxiliary_verb = "avere"

                    if wordclass == "intransitive verb":
                        wordclass_acronym = "vi"
                    elif wordclass == "transitive verb":
                        wordclass_acronym = "vt"
                    elif wordclass == "reflexive verb":
                        if not headword.endswith("si"):
                          headword = headword[:-1] + "si"
                          wordclass_acronym = "vr"
                          auxiliary_verb = "essersi"

                    headword_full = BeautifulSoup(rom.get("headword_full", ""), "html.parser")
                    flexion = headword_full.find("span", class_="flexion")
                    if flexion:                         
                        flexions = flexion.get_text().split(',')
                        headword_flexion = f" {flexions[0]}> "
                        past_participle = flexions[2].replace(">","").strip() if len(flexions) > 1 else ""

                    auxiliary = headword_full.find("span", class_="auxiliary_verb")
                    if auxiliary and auxiliary_verb == "avere": auxiliary_verb = "essere"

                    # Print the formatted output for headword
                    if headword and wordclass_acronym:
                        definition += f'"{headword}","{wordclass_acronym}.{headword_flexion}'

                    # Get translations from arabs
                    arabs = rom.get("arabs", [])
                    arab_output, examples_output = get_translations(arabs)

                    # If not irregular set the standard past participle
                    if past_participle == "":
                        if headword.endswith("are"):
                            past_participle = f"{headword[:-3]}ato"
                        elif headword.endswith("ere"):
                            past_participle = f"{headword[:-3]}uto"
                        elif headword.endswith("ire"):
                            past_participle = f"{headword[:-3]}ito"

                    # Print all arab outputs, separated by semicolons
                    definition += f'{"; ".join(arab_output)}; {auxiliary_verb} {past_participle}"'
                    print(definition)
                    print("\n".join(examples_output))

                # Check if the wordclass is "noun"
                if rom.get("wordclass", "").lower() == "noun":
                    headword = rom.get("headword", "")

                    # Extract wordclass and genus from headword_full using BeautifulSoup
                    soup = BeautifulSoup(rom.get("headword_full", ""), "html.parser")
                    
                    wordclass = soup.find("span", class_="wordclass")
                    genus = soup.find("span", class_="genus")
                    
                    wordclass_acronym = wordclass.find("acronym").get_text().lower() if wordclass else ""
                    genus_acronym = genus.find("acronym").get_text().lower() if genus else ""
                    
                    # Print the formatted output for headword
                    if headword and wordclass_acronym and genus_acronym:
                        definition += f'"{headword}","{wordclass_acronym}. {genus_acronym}. '
                    
                    # Iterate through arabs and print senses and translations
                     # Get translations from arabs
                    arabs = rom.get("arabs", [])
                    arab_output, examples_output = get_translations(arabs)
                    # Print all arab outputs, separated by semicolons
                    definition += f'{"; ".join(arab_output)}"'
                    print(definition)
                    print("\n".join(examples_output))
          
def get_translations(arabs):
    # Iterate through arabs and print senses and translations
    arab_output = []
    examples_output = []
    for arab in arabs:
        arab_rhetoric = ""
        arab_sense = ""
        arab_pl = ""
        # Parse the arab header
        arab_soup = BeautifulSoup(arab.get("header", ""), "html.parser")
        
        # Not interested in topic specific definitions
        arab_topic = arab_soup.find("span", class_="topic")
        # Move on to next iteration if topic found
        if arab_topic: continue

        # Look for a sense on the arab header
        sense = arab_soup.find("span", class_="sense")
        # Get the sense text if sense found
        if sense: arab_sense = f"{sense.get_text()} "

        # Look for a plural acronym
        plural = arab_soup.find("acronym", title="plurale")
        if plural: arab_pl = f"{plural.get_text()}. "

        rhetoric = arab_soup.find("span", class_="rhetoric")
        if rhetoric: arab_rhetoric = f"{rhetoric.get_text()}. "
        
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
            arab_topic = translation_soup.find("span", class_="topic")
            # Move on to next iteration if topic found
            if arab_topic: continue

            if translation_headword or translation_reflection:
              translation_sense = translation_soup.find("span", class_="sense")
              sense_text = f"{translation_sense.get_text()} " if translation_sense else ""
              target_text = translation.get("target", "")
              translations_output.append(f"{sense_text}{target_text}")

            
            if translation_example:
              rhetoric = ""
              translation_rhetoric = translation_soup.find("span", class_="rhetoric")
              example_text = f"{translation_example.get_text()}"
              target_text = remove_html_tags(translation.get("target", ""))

              rhetoric = f"{translation_rhetoric.get_text()}. " if translation_rhetoric else ""

              examples_output.append(f'"{example_text}","{arab_rhetoric}{rhetoric}{target_text}"')
        
        # Combine translation outputs
        if len(translations_output) > 0:
          arab_output.append(f"{arab_pl}{arab_sense}{', '.join(translations_output)}")
    
    return arab_output, examples_output

def remove_html_tags(data):
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(data, "html.parser")
    
    # Remove all remaining HTML tags
    return soup.get_text()

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <term>")
        sys.exit(1)
    
    term = sys.argv[1]
    filename = find_json_file(term)
    
    if filename:
        load_and_prettify_json(filename)

if __name__ == "__main__":
    main()
