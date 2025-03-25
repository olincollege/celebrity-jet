from datetime import date
import wptools

# Get the current year to calculate age
current_date = date.today()
current_year = current_date.year


# Get first two occupations
def get_occupations(infobox_data):
    """
    Get a celebrity's first two occupations on Wikipedia

    Args:
    Infobox: the infobox of the celebrity

    Returns:
    A list of the first two occupations on wiki page
    """
    all_occupations = infobox_data.get("occupation")
    occupation_list = all_occupations.split("*")
    return occupation_list[1:3]


# Get age
def get_age(infobox_data):
    """
    Get a celebrity's current age

    Args:
    Infobox: the infobox of the celebrity

    Returns:
    A string representing their age
    """
    birth_date = infobox_data.get("birth_date")
    print(birth_date)
    split_info = birth_date.split("|")
    age = current_year - int(split_info[1])
    return age


celebrity_names = ["Taylor Swift"]

for name in celebrity_names:
    # Get and parse the infobox
    content = wptools.page(name).get_parse()
    infobox = content.data["infobox"]
    # Get their occupations and age
    occupations = get_occupations(infobox)
    age = get_age(infobox)

    print(occupations, age)
