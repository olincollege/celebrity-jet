import requests
import mwparserfromhell


def get_grammy_nominee():
    """
    Get grammy nominee names list from wikipedia
    """
    title = "List_of_American_Grammy_Award_winners_and_nominees"  # Replace with any Wikipedia page title
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={title}"
    response = requests.get(url)
    data = response.json()

    # Extract Wikitext
    page_id = list(data["query"]["pages"].keys())[0]
    wikitext = data["query"]["pages"][page_id]["revisions"][0]["*"]

    # Parse Wikitext
    parsed_wiki = mwparserfromhell.parse(wikitext)

    # Extract nominee names with link
    names = [link.title for link in parsed_wiki.filter_wikilinks()]

    # Filter out irrelevant items
    grammy_nominee_names = []
    for name in names:
        if " " in name:
            if "(" not in name:
                grammy_nominee_names.append(name)
            elif "(band)" not in name:
                name_only = name.split("(")[0]
                grammy_nominee_names.append(name_only)

    grammy_nominee_names = grammy_nominee_names[2:-2]
    return grammy_nominee_names


def get_oscar_nominee():
    """
    Get oscar nominee names list from wikipedia
    """
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
    start_keyword = "==List of actors=="
    end_keyword = "==See also=="
    used_text = (
        parsed_wiki.split(start_keyword, 1)[-1].split(end_keyword, 1)[0].strip()
    )

    # Split the text by row
    entries = used_text.split("|-\n")

    # Extract the name
    oscar_nominee_names = []
    for entry in entries:
        parts = entry.split(" || ")
        if "||" in entry and parts[3] == "~":
            start = entry.find("[[") + 2
            end = entry.find("]]")
            name = entry[start:end]
            oscar_nominee_names.append(name)
        for index, name in enumerate(oscar_nominee_names):
            if "|" in name:
                oscar_nominee_names[index] = name.split("|", 1)[-1]
    return oscar_nominee_names


oscar_nominees = get_oscar_nominee()
grammy_nominees = get_grammy_nominee()

with open("oscar_nominees.csv", "w") as f:
    for nominee in oscar_nominees:
        f.write(str(nominee) + "\n")

with open("grammy_nominees.csv", "w") as f:
    for nominee in grammy_nominees:
        f.write(str(nominee) + "\n")
