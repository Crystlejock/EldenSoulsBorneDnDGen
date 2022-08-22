import openai
from db.lore_store import LoreStore
import os



# key.txt shoud be in the same directory as the program is run
def loadAPIKey():
    with open('key.txt', 'r', encoding='utf-8') as infile:
        openai.api_key = infile.read()


def pickWorld():
    dir_list = os.listdir("worlds")
    options = list(filter(lambda file: file.endswith(".db"), dir_list))
    options = list(map(lambda f : f[:-len(".db")], options))
    options.append("Create New World")
    for idx, option in enumerate(options):
        print("{idx}) {option}".format(idx=idx, option=option))

    selected = options[int(input('World No:'))]

    if (selected == "Create New World"):
        selected = input("world name:")

    return LoreStore('worlds/%s.db' % selected)


def addLocation(lore_store, region):
    location = input('Name of the location:')
    themes = input('Themes:')
def addRegion(lore_store):
    with open('prompts/region.txt', 'r') as file:
        region = input('Name of the region:')
        biome = input('Biome for the region:')
        themes = input('Themes:')
        template = file.read()
        prompt = template.format(region=region, themes=themes, biome=biome)
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
        )
        lore = response.choices[0].text.strip()
        lore_store.writeRegionLore(lore, themes=themes, region=region, biome=biome)

def updatedRegionEdges(lore_store, region):
    edges = lore_store.regionEdges(region)


def pickLocation(lore_store, region):
    options = lore_store.knownLocations(region)
    options.append("Create New Location")
    for idx, option in enumerate(options):
        print("{idx}) {option}".format(idx=idx, option=option))
    selected = options[int(input('Location No:'))]
    if (selected == "Create New Location"):
        print("not yet supported")
    else:
        lore = lore_store.readLoreForLocation(region=region, location=selected)
        print(lore)

def pickRegion(lore_store):
    options = lore_store.knownRegions()
    options.append("Create New Region")
    options.append("Back")
    for idx, option in enumerate(options):
        print("{idx}) {option}".format(idx=idx, option=option))

    selected = options[int(input('Region No:'))]
    if (selected == "Create New Region"):
        addRegion(lore_store)
    elif (selected == "Back"):
        return True
    else:
        pickLocation(lore_store, selected)
    return False


if __name__ == '__main__':
    loadAPIKey()
    store = pickWorld()
    done = False
    while (not done):
        print("\n")
        done = pickRegion(store)
    store.close()
