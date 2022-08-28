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
    options.append("Exit")
    for idx, option in enumerate(options):
        print("{idx}) {option}".format(idx=idx, option=option))

    selected = options[int(input('World No:'))]

    if (selected == "Create New World"):
        selected = input("world name:")
    if (selected == "Exit"):
        return None

    return LoreStore('worlds/%s.db' % selected)

def addLocation(lore_store, region):
    location = input('Name of the location:')
    updatedLocationEdges(lore_store, region, location)
    themes = input('Location Themes:')
    generateLocationLore(lore_store, themes, region, location)


def generateLocationLore(lore_store, themes, region, location):
    with open('prompts/location.txt', 'r') as file:
        data = lore_store.readDataForRegion(region)
        data['themes'] = themes
        data['location'] = location
        region_lore = lore_store.summaryRegionAndConnected(region, location)
        data['lore'] = region_lore
        template = file.read()
        prompt = template.format(**data)
        print(prompt)
        while(True):
            print("===========")
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt,
                max_tokens=200,
            )
            lore = response.choices[0].text.strip()
            print("=======================")
            print(lore)
            options = ["Save", "Regenerate", "Back"];
            for idx, option in enumerate(options):
                print("{idx}) {option}".format(idx=idx, option=option))
            selected = options[int(input('Option:'))]
            if (selected == "Save"):
                lore_store.writeLocationLore(lore=lore, themes=data['themes'], region=data['region'], location=location)
                return
            elif (selected == "Back"):
                return



def addRegion(lore_store):
    with open('prompts/region.txt', 'r') as file:
        region = input('Name of the region:')
        updatedRegionEdges(lore_store, region)
        biome = input('Biome for the region:')
        themes = input('Themes:')
        template = file.read()
        connected = lore_store.summaryConnectedRegions(region)
        prompt = template.format(region=region, themes=themes, biome=biome, connected=connected)
        print("=============")
        print("Pompt: " + prompt)
        while True:
            print("=============")
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt,
                max_tokens=200,
            )

            lore = response.choices[0].text.strip()
            print(lore)
            options = ["Save", "Regenerate", "Back"];
            print("=========================")
            for idx, option in enumerate(options):
                print("{idx}) {option}".format(idx=idx, option=option))
            selected = options[int(input('Option:'))]
            if (selected == "Save"):
                lore_store.writeRegionLore(lore, themes=themes, region=region, biome=biome)
                return
            elif (selected == "Back"):
                return

def updatedLocationEdges(lore_store, region, location):
    options = lore_store.knownLocations(region)
    if (len(options) == 0):
        return
    options.append("Done")
    while True:
        connections = lore_store.locationEdges(location, region)
        print("Select location to add or break connection with")
        for idx, option in enumerate(options):
            print("{idx}) {option} [{state}]".format(idx=idx, option=option, state="X" if option in connections else " "))
        selected = options[int(input('Option:'))]
        if (selected == "Done"):
            return
        elif (selected in connections):
            lore_store.removeLocationEdge(location, selected, region)
        else:
            lore_store.addLocationEdge(location, selected, region)

def updatedRegionEdges(lore_store, region):
    options = lore_store.knownRegions()
    if (len(options) == 0):
        return
    options.append("Done")
    print("=================")
    print("Edit Connections for " + region)
    while True:
        print("=================")
        connections = lore_store.regionEdges(region)
        print("Select region to add or break connection with")
        for idx, option in enumerate(options):
            print("{idx}) {option} [{state}]".format(idx=idx, option=option, state="X" if option in connections else " "))
        selected = options[int(input('Option:'))]
        if (selected == "Done"):
            return
        elif (selected in connections):
            lore_store.removeRegionEdge(region, selected)
        else:
            lore_store.addRegionEdge(region, selected)


def updateLocation(lore_store, location, region):
    print("Location: " + location)
    data = lore_store.readDataForLocation(region=region, location=location)
    print("Lore:" + data['lore'])
    print("Themes:" + data['themes'])
    options = [];
    print("=========================")
    options.append("Generate / Replace Lore")
    options.append("Edit Connections")
    options.append("Back")
    for idx, option in enumerate(options):
        print("{idx}) {option}".format(idx=idx, option=option))
    selected = options[int(input('Location No:'))]
    if (selected == "Generate / Replace Lore"):
        generateLocationLore(lore_store, data['themes'], region, location)
    elif(selected == "Edit Connections"):
        updatedLocationEdges(lore_store, region, location)
    else:
        return

def pickLocation(lore_store, region):
    print("REGION: " + region)

    while True:
        options = lore_store.knownLocations(region)
        options.append("Create New Location")
        options.append("Back")
        for idx, option in enumerate(options):
            print("{idx}) {option}".format(idx=idx, option=option))
        selected = options[int(input('Location No:'))]
        if (selected == "Create New Location"):
            addLocation(lore_store, region)
        elif (selected == "Back"):
            return
        else:
            updateLocation(lore_store, location=selected, region=region)


def pickRegion(lore_store):
    done = False
    while (not done):
        print("\n")

        options = lore_store.knownRegions()
        options.append("Create New Region")
        options.append("Export Data")
        options.append("Back")
        for idx, option in enumerate(options):
            print("{idx}) {option}".format(idx=idx, option=option))

        selected = options[int(input('Region No:'))]
        if (selected == "Create New Region"):
            addRegion(lore_store)
        if (selected == "Export Data"):
            print("Not Yet Implemented")
        elif (selected == "Back"):
            return
        else:
            done = pickLocation(lore_store, selected)
    return


if __name__ == '__main__':
    loadAPIKey()
    store = pickWorld()
    done = False
    while (store is not None):
        print("\n")
        pickRegion(store)
        store.close()
        store = pickWorld()

