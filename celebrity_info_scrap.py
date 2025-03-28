"""
Functions to get celebrity's occupation, age and networth.
"""

from datetime import date

# Get the current year to calculate age
current_date = date.today()
current_year = current_date.year


# Get first two or three occupations
def get_occupations(infobox_data):
    """
    Get a celebrity's first two or three occupations on Wikipedia

    Args:
    Infobox_data: the infobox of the celebrity

    Returns:
    A list of the first two or three occupations from the Wikipedia page
    """
    # Retrieve the occupation data from the infobox
    all_occupations = infobox_data.get("occupation") or infobox_data.get(
        "occupations"
    )

    # Clean the occupations data and split by '|'
    cleaned_occupations = all_occupations.replace("*", "|")
    raw_occupation_list = cleaned_occupations.split("|")

    occupation_list = []
    for occupation in raw_occupation_list:
        # Clean each occupation string by removing non-alphabetic characters
        lower_occupation = occupation.strip().lower()
        cleaned_occupation = "".join(
            [char for char in lower_occupation if char.isalpha()]
        )
        occupation_list.append(cleaned_occupation)

    return occupation_list[1:4]


# Decide an occupation for each person
def decide_occupation(name, occupations):
    """
    Decide an occupation for each celebrity according to their Wikipedia data
    and manually search if not applicable

    Args:
    Occupations: a list of occupations of a celebrity from Wikipedia infobox

    Returns:
    The celebrity's occupation, categorized into: Business & Politics, Music, TV & Media, Movie, and Sports
    """
    # Define categories of occupations and their respective terms
    categories = {
        "Business & Politics": {
            "politician",
            "businessman",
            "businesswoman",
            "investor",
            "venturecapitalist",
            "entrepreneur",
        },
        "Music": {
            "singer",
            "songwriter",
            "singersongwriter",
            "rapper",
            "musician",
            "composer",
        },
        "TV & Media": {
            "producer",
            "comedian",
            "televisionhost",
            "televisionpersonality",
            "influencer",
            "televisionpresenter",
            "mediapersonality",
        },
        "Movie": {"actor", "actress", "filmdirector"},
    }

    # Special cases where the occupation is explicitly defined
    special_categories = {
        "Elon Musk": "Business & Politics",
        "Eric Schmidt": "Business & Politics",
        "Harrison Ford": "Movie",
        "Judy Sheindlin": "TV & Media",
        "Ron DeSantis": "Business & Politics",
        "Marc Benioff": "Business & Politics",
        "Tommy Hilfiger": "Business & Politics",
        "Steve Wynn": "Business & Politics",
    }

    if name in special_categories:
        return special_categories[name]

    # Check occupations from the list to determine the category
    if occupations:
        for occupation in occupations:
            for category, content in categories.items():
                if occupation in content:
                    return category

    # Default to "Sports" if no other category is found, because sports celebrities usually don't have and "occupation" description in Wikipedia infobox
    return "Sports"


# Get age
def get_age(infobox_data):
    """
    Get a celebrity's current age

    Args:
    Infobox_data: the infobox of the celebrity

    Returns:
    A string representing their age
    """
    # Extract the birth date from the infobox
    birth_date = infobox_data.get("birth_date")
    split_info = birth_date.split("|")

    for ele in split_info:
        # Extract the year and calculate the age
        if len(ele) == 4:
            age = current_year - int(ele)
            break

    return age


# Get net worth
def get_net_worth():
    """
    Get a celebrity's net worth from API ninja

    Returns:
    net_worth_dict: A dictionary with celebrity names as keys and their net worth as values
    """
    net_worth_dict = {}

    # Read net worth data from a CSV file
    with open("Data/raw_api_info.csv", "r") as f:
        for line in f:
            if line != "[]":
                # Extract the name and net worth from each line in the file
                name_start = line.find('"name": "') + len('"name": "')
                name_end = line.find('"', name_start)
                name = line[name_start:name_end]

                net_worth_start = line.find('"net_worth": ') + len(
                    '"net_worth": '
                )
                net_worth_end = line.find(",", net_worth_start)
                net_worth = line[net_worth_start:net_worth_end]

                # Store the name and net worth in the dictionary
                net_worth_dict[name] = net_worth

    return net_worth_dict
