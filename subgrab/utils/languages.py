import logging
import json
from pathlib import  Path

with open(Path(Path(__file__).parent) / 'languages.json', 'r') as f:
    data = f.read()

LANG_ISO = json.loads(data)

logger = logging.getLogger("languages.py")

def get_language(provider, language):
    """
    Returns the value which of the language which is used by the
    provider instead of the language name in search requests.
    """
    try:
        value = LANG_ISO[language][provider]['value']
        name = LANG_ISO[language]['name']
        print(f"LANGUAGE: {name}")
        logger.debug(f"Language: {name}, Value: {value}, Provider: {provider}")

    except KeyError:
        logging.debug(f"Language {v['name']} not in subgrab language dictionary\nor not supported by {provider}.")

    return value
