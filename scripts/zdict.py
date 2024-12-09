import requests
import json
import sys
import re
import os

def fetch_dictionary_data(term):
    # Construct the API endpoint URL and parameters
    api_url = "https://api.pons.com/v1/dictionary"
    headers = {
        'X-Secret': os.getenv('X_SECRET')
    }
    params = {
        'l': 'enit',
        'in': 'it',
        'ref': 'false',
        'q': term
    }
    
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

def save_to_json(term, data):
    # Sanitize the term to create a valid filename
    filename = re.sub(r"[ ']", "_", term) + ".json"
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"Data saved to {filename}")

def process_term(term):
    filename = re.sub(r"[ ']", "_", term) + ".json"
    
    # Check if the JSON file already exists
    if os.path.exists(filename):
        print(f"The file {filename} already exists. Skipping API call.")
        return
    
    data = fetch_dictionary_data(term)
    
    if data:
        save_to_json(term, data)
    else:
        print(f"Failed to fetch data for the term: {term}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <term_or_file>")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    # Check if the input is a file or a single term
    if os.path.isfile(input_arg):
        with open(input_arg, 'r', encoding='utf-8') as file:
            terms = file.readlines()
            terms = [term.strip() for term in terms if term.strip()]  # Remove any leading/trailing whitespace
    else:
        terms = [input_arg]
    
    for term in terms:
        process_term(term)

if __name__ == "__main__":
    main()
