import json
import random

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


def parseEffect(effect):
    if (isinstance(effect, str)):
        return effect + "\n"
    elif (effect['type'] == "entries"):
        result = ""
        for sub in effect['entries']:
            result += parseEffect(sub)
        result += "\n\n"
        return result
    elif (effect['type'] == "table"):
        result = "\n"
        for row in effect['rows'][0]:
            result += row + "\n"
        result += "\n"
        return result
    elif (effect['type'] == "list"):
        result = "LISTS UNSUPORTED\n"
        return result
    else:
        return "unknown type " + effect['type'] + "\n"


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

