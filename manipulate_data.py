"""
Functions to get and sort scraped data, specifically from api-ninjas and
celebrityflighttracker.com
"""

import json
import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import wptools
import celebrity_info_scrap as scrap
import keys

# pylint: disable=no-member
# pylint: disable=E1101


def get_apininjas_data(celeb_name):
    """
    Given a string name of a celebrity returns the api call to apininjas celeb
    api.

    Args:
        celeb_name: A string name of a celebrity that data will be collected for

    Returns:
        Dictionary of information of a given celebrity.
    """
    api_key = keys.get_ninja_key()
    api_url = f"https://api.api-ninjas.com/v1/celebrity?name={celeb_name}"
    response = requests.get(api_url, headers={"X-Api-Key": api_key}, timeout=10)
    if response.status_code == requests.codes.ok:
        return response.text
    else:
        return None


def get_flighttracking(
    url="https://celebrityprivatejettracker.com/leaderboard/",
    file_path="Data/data_flighttracker.html",
):
    """
    Makes a request to the url site to get all the html on that page and saves
    it to a file as formatted html.

    Note: Calling this too many times will revoke site access and headers need
    to be changed to simulate different browser.

    Args:
        url: A string containing a url to scrape the html from
            Default: https://celebrityprivatejettracker.com/leaderboard/
        file: A string filepath to the file we want to write html to
            Default: flighttracking_data.html
    """
    # Simulate being a browser
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com",
        "Connection": "keep-alive",
    }
    html = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(html.text, "html.parser")
    formatted_soup = soup.prettify()
    for script in soup(["script", "style"]):
        script.decompose()
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(formatted_soup)


def get_celeb_chunks(file_path="Data/data_flighttracker.html"):
    """
    Gets the html chunk of data containing celebrity information from scraped
    celebrityflighttracker.com/leaderboards html and returns a list of all
    celebrity data.

    Args:
        file: file path to scraped data.

    Return:
        chunks of html soups that contain the celebrity flight information
    """
    elements = None
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        elements = soup.find_all("tr", class_="trlight")

    return elements[:-1]


def get_celeb_data(celeb_html):
    """
    Given a list of soup chunks of celebrity data finds name, aircraft
    model, tail registration, total miles flown, total flights, total
    fuel used, total flight time, total pollution (metric tons of co2)
    and returns nested lists in this order.

    Args:
        celeb_html: A list of soups containing individual celebrity data.

    Returns:
        A dictionary containing data about celebrity's jet usage.
        keys: celebrity names
        values: a list of celebrity information (see above)
        A dictionary string:list pairs containing celebrity information
        (see above).
    """
    data_dict = {}
    for chunk in celeb_html:
        # get the name from chunk
        clean_name = get_individual_name(chunk)
        # get associated data from chunk
        cleaned_data = get_individual_data(chunk)
        # combine name and data into a dictionary
        data_dict[clean_name] = cleaned_data
    return data_dict


def get_individual_name(celeb_chunk):
    """
    Given a chunk of celebrity data, finds the name of the celebrity

    Args:
        celeb_chunk: a bs4 object of celebrity data

    Returns:
        A string with the celebrity name and some designation (often)
    """
    # find the name catagory
    name = celeb_chunk.find("a", class_="maincolor")  # .text.strip()
    if name is None:
        name = celeb_chunk.find("td")
    # clean the name
    clean_name = name.get_text(strip=True)
    if clean_name.find("\xa0") != -1:
        clean_name = clean_name.replace("\xa0", " ")
    clean_name = fix_names(clean_name)
    return clean_name


# Fix names got from jet usage website so that we can search it on wikipedia
def fix_names(name):
    """
    Remove duplicate names and correct spelling mistakes

    Args:
    name: a dictionary whose keys are jet owners' names with repetitions
    and mistakes.

    Returns:
    A cleaned list of names ready for wikipedia search
    """
    correction_list = {
        "Alex Rodriquez": "Alex Rodriguez",
        "Dr. Phil": "Phil McGraw",
        "Drake": "Drake (musician)",
        "Judge Judy": "Judy Sheindlin",
        "Jay Z": "Jay-Z",
        "Google": None,
        "Caesars Palace Casino": None,
        "Nike Corporation": None,
        "Under Armour Corporation": None,
        "Playboy Corporation": None,
    }
    if name in correction_list:
        return correction_list[name]
    return name


def get_individual_data(celeb_chunk):
    """
    Finds individual pieces of celebrity data from a chunk of html and returns
    them as a list.

    Args:
        celeb_chunk: a bs4 object of celebrity data

    Returns:
        A list of strings containing celebrity data
    """
    # find the data attached to the name
    data_points = celeb_chunk.find_all("td")[1::]
    clean_data_val = []
    for n in data_points:
        if n.find("a") is not None:
            clean_data_val.append(str(n.find("a").get_text(strip=True)))
        else:
            clean_data_val.append(str(n.get_text(strip=True)))
    return clean_data_val


def clean_all_data(data_dict):
    """
    Iterates through passed dictionary and cleans the data within

    Args:
        data_dict: A dictionary with string keys and a list of strings
        as the items"""
    for key in data_dict:
        clean_data(data_dict[key])


def clean_data(data_list):
    """
    Converts a list of celebrity data into usable number strings.

    Args: A list of celebrity data
    """
    # miles
    clean_number(data_list, 2)
    # gallons
    clean_number(data_list, 4)
    # co2
    clean_number(data_list, 6)
    clean_time(data_list)


def clean_number(data_list, index):
    """
    Extracts the miles a celebrity's private jet has flown as a pure number.

    Args: A list of celebrity data
    """
    value = ""
    for char in data_list[index]:
        if char.isdigit():
            value = value + char

    data_list[index] = value


def clean_time(data_list):
    """
    Extracts the hours of flight time the celebrity has flown in their private
    jet as a pure number and directly inserts that into the mutable dictionary
    that is passed.

    Args: A list of celebrity data
    """
    index = 5
    dirty_time = data_list[index]
    days = ""
    hours = ""
    minutes = ""

    start_index = 0
    number_end_index = 0
    in_words = False

    for i, char in enumerate(data_list[index]):
        if in_words is False and (char.isalpha() or char == " "):
            in_words = True
            number_end_index = i
        if (in_words is True and char.isdigit()) or (
            i == (len(dirty_time) - 1)
        ):
            tslice = dirty_time[start_index:i]
            if tslice.find("day") != -1:
                days = dirty_time[start_index:number_end_index]
            if tslice.find("hour") != -1:
                hours = dirty_time[start_index:number_end_index]
            if tslice.find("minute") != -1:
                minutes = dirty_time[start_index:number_end_index]
            start_index = i
            in_words = False

    if days == "":
        days = 0
    if hours == "":
        hours = 0
    if minutes == "":
        minutes = 0

    days = int(days)
    hours = int(hours)
    minutes = int(minutes)

    in_hours = (days * 24) + hours + (minutes / 60)
    data_list[index] = in_hours


def combine_duplicates(celeb_dict):
    """
    Merges personalities with multiple jets into one profile with
    all their flight data

    Args:
        celeb_dict: dictionary of "string": list of strings containing
        duplicate celebrities.

    Returns:
        A dictionary where all of a celebrity's flight data is assigned
        under their name, not under their jets. "Celeb Name": [5x1 Floats]
    """
    combined_dict = {}
    for name, data in celeb_dict.items():
        match = False
        just_name = name
        if name is None:
            continue
        if name.find("(") != -1:
            index = name.find("(") - 1
            just_name = name[:index]

        # check if there is a match
        for c_dict_name, _ in combined_dict.items():
            if just_name.find(c_dict_name) != -1:
                match = True
                for i in range(len(combined_dict[c_dict_name])):
                    combined_dict[c_dict_name][i] = float(
                        combined_dict[c_dict_name][i]
                    ) + float(data[i + 2])
        if match is False:
            combined_dict[just_name] = data[2::]

    return combined_dict


def get_celeb_info_wapi(data_dict):
    """
    Access data from apininjas for each celebrity and write them into a
    json file.

    Args:
    data_dict: A dictionary containing data about celebrity's jet usage
    """
    # Combine any duplicate entries in the provided data dictionary
    fix_dict = combine_duplicates(data_dict)
    fix_name = list(fix_dict.keys())

    # Open the file to write raw API data to it
    with open("Data/raw_api_info.csv", "w", encoding="utf-8") as f:
        for name in fix_name:
            # Fetch the API response for each celebrity
            response = get_apininjas_data(name)

            # Write the response to the file, or write an empty string if no data is returned
            if response is not None:
                f.write(response)
            else:
                f.write("")
            f.write("\n")


def get_jet_owner_info(data_dict):
    """
    Process and organize celebrity data into a json file

    Args:
    data_dict: A dictionary containing data about celebrity's jet usage
    """
    # Combine duplicate entries in the data dictionary
    fix_dict = combine_duplicates(data_dict)
    fix_name = list(fix_dict.keys())

    # Open the file to write celebrity information in JSON format
    with open("Data/jet_owners_info.json", "w") as f:
        for name in fix_name:
            # Get and parse the celebrity's Wikipedia infobox (if available)
            try:
                content = wptools.page(name).get_parse()
                infobox = content.data["infobox"]
            except LookupError:
                continue

            # Get the celebrity's occupations and categorize them
            try:
                occupations = scrap.get_occupations(infobox)
            except AttributeError:
                occupations = None
            category = scrap.decide_occupation(name, occupations)

            # Get the celebrity's age
            try:
                age = scrap.get_age(infobox)
            except AttributeError:
                age = None

            # Get the celebrity's net worth from the data dictionary
            net_worth_dict = scrap.get_net_worth()
            if name.lower() in net_worth_dict:
                net_worth = net_worth_dict[name.lower()]
            else:
                net_worth = "N/A"

            # Write the celebrity's information in JSON format to the file
            f.write(json.dumps([name, category, age, net_worth]) + "\n")


def create_dict(json_file_path):
    """
    Converts jet owner info from json to a dictionary

    Args:
    json_file_path: the file path of the json doc that stores original info

    Returns:
    A dictionary with each celebrity's name as keys and their information as values
    """
    # Create an empty dictionary to store the celebrity information
    info_dict = {}

    # Open the JSON file and process each line
    with open(json_file_path, "r") as f:
        for line in f:
            data = json.loads(line.strip())
            info_dict[data[0]] = [data[1], data[2], data[3]]

    return info_dict
