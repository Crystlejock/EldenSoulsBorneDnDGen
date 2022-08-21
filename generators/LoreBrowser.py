import openai
from db.lore_store import LoreStore

# key.txt shoud be in the same directory as the program is run
def loadAPIKey():
    with open('key.txt', 'r', encoding='utf-8') as infile:
        openai.api_key = infile.read()


def prompt():
    region = input('Name of the region:')
    themes = input('Themes:')
    lore_store = LoreStore('lore_store.db')
    summary = lore_store.region_summary(themes=themes, region=region, location="")
    print("\n")
    print("Summary\n"+summary)


if __name__ == '__main__':

    loadAPIKey()
    while(True):
        print("\n")
        prompt()