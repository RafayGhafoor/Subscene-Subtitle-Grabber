import logging
import json
from pathlib import  Path
with open(Path(Path(__file__).parent) / 'languages.json', 'r') as f:
    data = f.read()

LANG_ISO = json.loads(data)

logger = logging.getLogger("languages.py")

def get_languages(provider):

    languages = {}

    for k,v in LANG_ISO.items():
        try:
            if v[provider]['accepted'] == True:
                languages[k] = {'name': v['name'],
                                'value': v[provider]['value']}
        except KeyError:
            # pass silently, if key not exists
            pass
        else:
            logging.debug(f"Language {v['name']} not in dictionary\nor not supported by {provider}")
    return languages

