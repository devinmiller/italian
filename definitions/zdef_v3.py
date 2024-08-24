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
                # Common attributes
                arabs = rom.get("arabs", [])
                definition = ""
                headword = rom.get("headword", "").lower()
                headword_full = BeautifulSoup(rom.get("headword_full", ""), "html.parser")
                headword_full_flexion = headword_full.find("span", class_="flexion")
                flexion = headword_full_flexion.get_text().strip() if headword_full_flexion else ""
                wordclass = rom.get("wordclass", "").lower()

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

                    print(definition)
                    print("\n".join(examples_output))

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

                    print(definition)
                    print("\n".join(examples_output))

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
                        verb_fps_present = f" <{verb_flexions[0].strip()}> "
                        # Third flexion should be the past participle of the verb
                        verb_past_participle = verb_flexions[2].strip() if len(verb_flexions) > 1 else ""

                    headword_full_auxiliary_verb = headword_full.find("span", class_="auxiliary_verb")
                    # The auxiliary verb should only appear in the full headword if not avere
                    # We also first check that the auxiliary verb was changed for a reflexive
                    if headword_full_auxiliary_verb and verb_auxiliary_verb == "avere": verb_auxiliary_verb = "essere"

                    # Print the formatted output for headword
                    if headword and wordclass_acronym and verb_fps_present:
                        definition += f'"{headword}","{wordclass_acronym}. {verb_fps_present} '
                    else:
                        definition += f'"{headword}","{wordclass_acronym}. '

                    # If not set from a flexion follow standard rules
                    if verb_past_participle == "":
                        match headword[len(headword)-3:]:
                            case "are":
                                verb_past_participle = f"{headword[:-3]}ato"
                            case "ere":
                                verb_past_participle = f"{headword[:-3]}uto"
                            case "ire":
                                verb_past_participle = f"{headword[:-3]}ito"
                            

                    # Print all arab outputs, separated by semicolons
                    definition += f'{"; ".join(translation_output)}; {verb_auxiliary_verb} {verb_past_participle}"'

                    print(definition)
                    print("\n".join(examples_output))

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
        arab_header_soup = BeautifulSoup(arab.get("header", ""), "html.parser")
        
        # Not interested in topic specific definitions
        arab_header_topic = arab_header_soup.find("span", class_="topic")
        # Move on to next iteration if topic found
        if arab_header_topic: continue

        # Look for a sense on the arab header
        sense = arab_header_soup.find("span", class_="sense")
        # Get the sense text if sense found
        if sense: arab_sense = f"{sense.get_text()} "

        # Look for a plural acronym
        plural = arab_header_soup.find("acronym", title="plurale")
        if plural: arab_pl = f"{plural.get_text()}. "

        rhetoric = arab_header_soup.find("span", class_="rhetoric")
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
              target_text = translation.get("target", "").strip()
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
