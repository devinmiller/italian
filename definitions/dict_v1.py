import requests
import json
import sys
import re

def fetch_dictionary_data(term):
    # Replace this URL with the actual dictionary API endpoint
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{term}"
    
    try:
        response = requests.get(api_url)
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
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <term>")
        sys.exit(1)
    
    term = sys.argv[1]
    data = fetch_dictionary_data(term)
    
    if data:
        save_to_json(term, data)
    else:
        print(f"Failed to fetch data for the term: {term}")

if __name__ == "__main__":
    main()