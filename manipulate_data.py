import requests
from bs4 import BeautifulSoup
from opensky_api import OpenSkyApi  # pylint:disable=E401


def get_flighttracking(
    url="https://celebrityprivatejettracker.com/leaderboard/",
    file_path="flighttracking_data.html",
):
    """
    Makes a request to the url site to get all the html on that page and saves
    it to a file as formatted html.

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


def get_celeb_chunks(file="flighttracking_data.html"):
    """
    Gets the html chunk of data containing celebrity information from scraped
    celebrityflighttracker.com/leaderboards html and returns a list of all
    celebrity data.

    Args:
        file: file path to scraped data.
    """
    elements = None
    with open("sample_data_flighttracker.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        elements = soup.find_all("tr")  # [1] # The first one but can I get all?
    print(elements)
    # return elements


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
    pass


def get_individual_data(celeb_chunk):
    """
    Finds individual pieces of celebrity data from a chunk of html and returns
    them as a list.

    Args:
        celeb_chunk: a soup chunk of celebrity data

    Returns:
        A list of strings containing celebrity data
    """
    print(celeb_chunk)
