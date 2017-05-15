import json
import os
import re
import requests
from collections import OrderedDict

sources_json = None

# Open the set of sources for modules
with open('./json/sources.json') as sources:
  sources_json = json.loads(sources.read(), object_pairs_hook=OrderedDict)

# If no sources were loaded, exit
if sources_json is None:
  exit()

# Final source to print
licenses = []

for source in sources_json:
  response = requests.get(sources_json[source])
  if response.status_code != 200:
    print('Request returned status code {}'.format(response.status_code))
    print('Could not retrieve license for source: {}'.format(source))
    exit()
  else:
    body = re.sub(r'(?<!\n)\n(?!\n)', ' ', response.text)
    body = re.sub(r' {2,}', ' ', body)
    body = re.sub(r'(?<!\n)\n(?!\n)|\n{3,}', '', body)
    licenses.append({
      'key': source,
      'data': [{
        'key': 0,
        'text': body
      }]
    })
    print('Retrieved license for source {}'.format(source))

licenses = sorted(licenses, key=lambda k: k['key'].lower())

os.makedirs('./output/', exist_ok=True)
with open('./output/licenses.json', 'w+', encoding='utf8') as outfile:
  json.dump(licenses, outfile, sort_keys=True, ensure_ascii=False)
