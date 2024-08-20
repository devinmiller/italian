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
        
        # Convert JSON to string
        json_str = json.dumps(data, indent=4, ensure_ascii=False)
        
        # Decode HTML entities and remove tags
        plain_text = remove_html_tags(json_str)
        
        # Print the prettified JSON
        print(plain_text)

def remove_html_tags(data):
    # Decode HTML entities
    data = html.unescape(data)
    
    # Remove HTML tags using BeautifulSoup
    soup = BeautifulSoup(data, "html.parser")
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
