import json

with open('languages.json', 'r') as f:
    data = f.read()

LANG_ISO = json.loads(data)
LANG_DEFAULT = "en"

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
            print(f"Language {v['name']} not in dictionary\nor not supported by {provider}")
    return languages

