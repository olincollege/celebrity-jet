from datetime import date
import json

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
    A list of the first two or three occupations on wiki page
    """
    all_occupations = infobox_data.get("occupation") or infobox_data.get(
        "occupations"
    )
    cleaned_occupations = all_occupations.replace("*", "|")
    raw_occupation_list = cleaned_occupations.split("|")
    occupation_list = []
    for occupation in raw_occupation_list:
        lower_occupation = occupation.strip().lower()
        cleaned_occupation = "".join(
            [char for char in lower_occupation if char.isalpha()]
        )
        occupation_list.append(cleaned_occupation)
    return occupation_list[1:4]


# Decide a occupation for each person
def decide_occupation(name, occupations):
    """
    Decide a occupation for each celebrity according to their wikipedia data
    and manually search up if not applicable

    Args:
    Occupations: a list of occupations of a celebrity from wikipedia infobox

    Returns:
    Their occupation, within the following categories:
    Business & politics, music, TV & media, movie, and sports
    """
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
    if occupations:
        for occupation in occupations:
            for category, content in categories.items():
                if occupation in content:
                    return category
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
    birth_date = infobox_data.get("birth_date")
    split_info = birth_date.split("|")
    for ele in split_info:
        if len(ele) == 4:
            age = current_year - int(ele)
            break
    return age


# Get net worth
def get_net_worth():
    """
    Get a celebrity's net worth from API ninja

    Returns:
    A string representing their net worth
    """
    with open("Data/raw_api_data.json", "r") as f:
        for line in f:
            if not line:
                continue
            data = json.loads(line.strip())
            return data[0]["net_worth"]
