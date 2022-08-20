# EldenSoulsBorneDnDGen
Project to create a DND content generator that creates Elden SOuls Borne style content for Dnd Games


Current goals
-Develope data structure from Various Possible Generated items
-Clean Magic Item data
-Clean Monster Data.
-Create prompts for Item rul;e generation
-Create prompts for Monster rules generation


-Prompt COmpletion Formatting !!MUST FOLLOW!!!
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
 For configuring training data


Item Name Generation


# Item description Generation {70%, Need to find prompts to generate based on context reliable} 
[prompt] Item Name: Longsword
[completion] Item Description: A standard straight sword. Widely-used by soldiers and garrisons of the old king. Many soldiers of the old king were possessed of such blades, but few remain now. The king's soldiers always led lonely lives, perhaps that is why they admired the sheen of their swords so. 

# Item Rule generation (Tested on babbage model, mostly failed, incoherant rules and properties generation)
[prompt] Generate new (rarity) (type) named (Item Name) Item Description (item Description)
[completion]
Name:Longsword 
Mundane 
weapon 
Attunment:  
Properties: 1d8, slashing, - heavy, two-handed 
Magical Effects: A longsword is a double-edged, hand-and-a-half weapon. A foe of the blade has disadvantage on attack rolls against a longsword wielder. A longsword can be dual-wielded. If the main weapon is a longsword, the back, or saber, is a short sword. Heavy. Creatures that are Small or Tiny have disadvantage on attack rolls with heavy weapons. A heavy weapon's size and bulk make it too large for a Small or Tiny creature to use effectively. Two-Handed. This property allows you to make two melee attacks with one hand.



# atempted to train davinci model on character anmes, failed, needs more prompt enginearing
Characters = [Prompt] "Character Name" [Completion] Fred 



Monsters = [Prompt] Creture Name: [Completion] Lizard 

MLore = [Prompt] Lizard,\nInfo: [Completion] Big Scary Lizard

Monsters Stats=  [Prompt] Lizard,\nClore Big SCary Lizard,\nChallange "(Variable input from me),   [Completion] Monster stats Here

Locations = [Prompt] "Location Name" [Completion] Location Names here 

LLore = [Prompt] Location Name,\nLocation Lore: [Completion] Location Descriptions here


------------------------------------------------------------


View ESBDDoc jpg for Design concept.


