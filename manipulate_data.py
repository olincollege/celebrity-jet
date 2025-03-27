import re
import requests
from bs4 import BeautifulSoup
import keys


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
    api_url = "https://api.api-ninjas.com/v1/celebrity?name={}".format(
        celeb_name
    )
    response = requests.get(
        api_url,
        headers={"X-Api-Key": api_key},
    )
    if response.status_code == requests.codes.ok:
        return response
    else:
        print("Error:", response.status_code, response.text)


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
    html = requests.get(url, headers=headers)
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
        A list of lists containing celebrity information (see above).
    """
    data_dict = {}
    for chunk in celeb_html:
        # get the name from chunk
        clean_name = get_individual_name(chunk)
        # get associated data from chunk
        clean_data = get_individual_data(chunk)
        # combine name and data into a dictionary
        data_dict[clean_name] = clean_data
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
    return clean_name


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
    clean_data = []
    for n in data_points:
        if n.find("a") is not None:
            clean_data.append(str(n.find("a").get_text(strip=True)))
        else:
            clean_data.append(str(n.get_text(strip=True)))
    return clean_data


def clean_all_data(data_dict):
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
    jet as a pure number

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
            slice = dirty_time[start_index:i]
            if slice.find("day") != -1:
                days = dirty_time[start_index:number_end_index]
            if slice.find("hour") != -1:
                hours = dirty_time[start_index:number_end_index]
            if slice.find("minute") != -1:
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
