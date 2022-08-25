import json
import random
import re

# Opening JSON file
f = open('json/DnDMagicData.json')

data = json.load(f)
template = ""
with open('prompts/ItemPrompt.txt', 'r') as file:
    template = file.read()

type_table = {'HA': 'Heavy Armor', 'WD': 'Wand', 'S': 'Shield', 'MA': 'Medium Armor', 'P': 'Potion',
              'INS': 'Instrument', 'R': 'Ranged Weapon', 'M': 'Melee Weapon', 'RD': 'Rod', 'RG': 'Ring',
              'AF': 'Ammunition', 'GV': 'Generic Variant', 'SC': 'Scroll', 'LA': 'Light Armor', 'SCF': 'Wondrous Item',
              'OTH': 'Key item', 'A': 'Arrow'}

types = set()

matcher = re.compile("\{@[a-z]* (.*?)(\|.*?)?}")

def parseInset(inset):
    result = ""
    result += inset['name'] + '\n'
    for sub in inset['entries']:
        result += '   ' + parseEffect(sub)
    return result
def parseList(list):
    result = ""
    for item in list['items']:
        result += parseEffect(item)
    return result

def parseWrapper(wrapper):
    return parseEffect(wrapper['wrapped'])

def removeTokens(text):
    pass1 = matcher.sub('\\1', text)
    pass2 = matcher.sub('\\1', pass1)
    return pass2

def parseEffect(effect):
    result = ""
    if (isinstance(effect, str)):
        result += removeTokens(effect) + "\n"
    elif (effect['type'] == "entries"):
        if 'name' in effect:
            result += effect['name'] + ":\n"
        for sub in effect['entries']:
            result += parseEffect(sub)
    elif (effect['type'] == "table"):
        result += "\n"
        for row in effect['rows'][0]:
            if (isinstance(row, str)):
                result += removeTokens(row) + "\n"
        result += "\n"
    elif (effect['type'] == 'inset'):
        result += parseInset(effect)
    elif (effect['type'] == 'wrapper'):
        result += parseWrapper(effect)
    elif (effect['type'] == "list"):
        parseList(effect)

    else:
        return "unknown type " + effect['type'] + "\n"
    return result + "\n"


def parseItem(item):
    print(item["name"])
    description = '{generated description}'
    type = ""
    if 'type' in item:
        type = item['type']
        types.add(type)
    elif 'wondrous' in item:
        type = 'OTH'
    else:
        type = "OTH"

    effects = ""
    if "_fullEntries" in item:
        for effect in item["_fullEntries"]:
            effects += parseEffect(effect)
    else:
        for effect in item["entries"]:
            effects += parseEffect(effect)

    prompt = template.format(name=item["name"], type=type_table[type], rarity=item["rarity"], effects=effects,
                             description="{description}")
    return prompt


count = 0

with open('prompts/ItemPromptOut.txt', 'w') as file:
    for item in data:
        prompt = ""
        if '_isInherited' in item:
            v = random.choice(item["variants"])
            count += 1
            prompt = parseItem(v["specificVariant"])
        else:
            prompt = parseItem(item)
            count += 1
        file.write(prompt)

