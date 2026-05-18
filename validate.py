import yaml
import json
from jsonschema import validate

with open('vocabolario/schema.json') as f:
    schema = json.load(f)

with open('vocabolario/abbondante.yaml') as f:
    data = yaml.safe_load(f)

validate(instance=data, schema=schema)
print("Valid!")
