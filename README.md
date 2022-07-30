# EldenSoulsBorneDnDGen
Project to create a DND content generator that creates Elden SOuls Borne style content for Dnd Games


Temp Google Collab https://colab.research.google.com/drive/1kB9rnXzoS90UlYqgYXxyCYBcbmn7VZOd#scrollTo=XEa5ENl-fLmu

Current goals
-Read csv file and clean to quality, Format and print to Jsonl.  
-Develope data structure from Various Possible 




-Prompt COmpletion Formatting !!MUST FOLLOW!!!
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
 For configuring training data


Items = [Prompt] "Item Name" [Completion] Flaming Sword 

Properties = [Prompt] Flaming Sword, Rarity: Rare ,Type: Longsword, Properties:  [Completion] Item Properties Here

Descriptions = [Prompt]Flaming Sword, Rarity: Rare ,Type: Longsword, Properties: Damage X versitile,\nDescription: [Completion] Sword is Unfire and burns things, made by Sparky ina  volcano

Effects = [Prompt]Flaming Sword, Rarity: Rare ,Type: Longsword, Properties: Damage X versitile,Description Sword is Unfire and burns things, made by Sparky ina  volcano  [Completion] does extra 1d6 fire damage, and lights things on fire

Characters = [Prompt] "Character Name" [Completion] Fred 

Monsters = [Prompt] Creture Name: [Completion] Lizard 

MLore = [Prompt] Lizard,\nInfo: [Completion] Big Scary Lizard

Monsters Stats=  [Prompt] Lizard,\nClore Big SCary Lizard,\nChallange "(Variable input from me),   [Completion] Monster stats Here

Locations = [Prompt] "Location Name" [Completion] Location Names here 

LLore = [Prompt] Location Name,\nLocation Lore: [Completion] Location Descriptions here

---Probably not---
Dialogue = [Prompt] Circumstance, [Completion] Dialogue here






Generator code



If choice = false
	While Choice = False
		Print (What do you want to do, list Dict'Generator')
		Input = User input int.Variable [1-Generate random Item,2-Generate Specific Item,3-Generate Type of Item,4-Generate Character,5-Generate Location

	Else run GeneratorX

		Prompt = 




		Generator ends
		Export Generator Output
		Choice = False


Items = [Prompt] Item Name [Completion] item Names here 

Rarity = Select Option from Dict, Or Random

Subtype = Select Option From Dict, Or random

Properties = [Prompt]Item Name,\nRarity,\nSub-Type, [Completion] Item Properties Here

Descriptions = [Prompt] Description [Completion] item description here 


Effects = [Prompt]Item Name,\nRarity,\nSub-Type,\nProperties,\nitem Description,\n\nEFFECTS   [Completion] Effects Of Item Here

Setup Data Steps?

Fine Tune Model 1 - Names (I Have this Data)
{"prompt": "<Generate ESB Item Name>", "completion": "<Mjolnir>"}
{"prompt": "<Generate ESB Character Name>", "completion": "<Godwyn the Golden>"}
{"prompt": "<Generate ESB Monster Name>", "completion": "<Undead Asylum>"}


Fine Tune Model 2 - Descriptions (I have this Data) - goal teach it to generate themeatic descriptions based on somethings Name type
{"prompt": "<Generate ESB Item Description for "Rivers of Blood">", "completion": "<Weapon of Okina, swordsman from the Land of Reeds. A cursed weapon that has felled countless men.When Mohg, the Lord of Blood, first felt Okina's sword, and madness, upon his flesh, he had a proposal, to offer Okina the life of a demon, whose thirst would never go unsated.>"}
etc

Use Model 2 to Generate ESB Descriptions for DnD names- goal teach it to asscoiate

Fine Tune Model 3 - Generate Specififed thing + Base DnD Item Name + Model 2 Generated Description dor Base DnD Item 
{"prompt": "<Generate Item Name:"Mojnir" + Item Description "Description of item here">", "completion": "<Katana, Legendary, Finesse, 1d8/1d10 slashing damage>"}
Question - Since it all ready has DnD info available would it be Better to A-Use a broad 200 sample size, or B - do this for all 1500 DnD items, or C Do 200 for each CLassifier used for generation (Rarity(None,Common,Rare,Very Rare,Legendary,Artifact),Item Type(Adventuring gear,Consumable,Weapon,Armor,Trinket,Wand,Staff,Rod,),Item Sub Type (Heavya armor, Medium Armor, Light Armor, Long Sword, Short Sword, ETC)

Fine Tune 4 - Repeat Model 3 for Monster stats

















++++++++++++++++++++++++++++++++++++++++++++  CODE PLANS *************************************************

View ESBDDoc jpg for Design concept.


