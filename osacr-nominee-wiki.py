# Get oscar nominee names list from wikipedia

import requests
import mwparserfromhell

title = "List_of_actors_with_Academy_Award_nominations"  # Replace with any Wikipedia page title
url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={title}"

response = requests.get(url)
data = response.json()

# Extract Wikitext
page_id = list(data["query"]["pages"].keys())[0]
wikitext = data["query"]["pages"][page_id]["revisions"][0]["*"]

# Parse Wikitext
parsed_wiki = mwparserfromhell.parse(wikitext)

# Extract nominee list
start_keyword  = '==List of actors=='
end_keyword = '==See also=='
used_text = parsed_wiki.split(start_keyword, 1)[-1].split(end_keyword, 1)[0].strip() 

# Split the text by row
entries = used_text.split("|-\n")

# Extract the name
oscar_nominee_names = []
for entry in entries:
    parts = entry.split(" || ")
    if '||' in entry and parts[3] == "~":
        start = entry.find("[[") + 2
        end = entry.find("]]")
        name = entry[start:end]
        oscar_nominee_names.append(name)
    for index, name in enumerate(oscar_nominee_names):
        if '|' in name:
            oscar_nominee_names[index] = name.split('|',1)[-1]

print(oscar_nominee_names)
