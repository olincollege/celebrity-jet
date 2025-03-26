from datetime import date
import json

# Get the current year to calculate age
current_date = date.today()
current_year = current_date.year

# Fix names got from jet usage website so that we can search it on wikipedia
def fix_names(name_list):
    '''
    Remove duplicate names and correct spelling mistakes

    Args:
    Name_list: a list of jet owners with repetitions and mistakes

    Returns:
    A cleaned list of names ready for wikipedia search
    '''
    cleaned_names = []
    correction_list = {'Alex Rodriquez':'Alex Rodriguez', 'Dr. Phil':'Phil McGraw', 'Drake':'Drake (musician)', 'Judge Judy':'Judy Sheindlin', 'Jay Z':'Jay-Z', 'Google':None, 'Caesars Palace Casino':None, 'Nike Corporation':None, 'Under Armour Corporation':None, 'Playboy Corporation':None}
    for name in name_list:
        cleaned_name = name.split(" (")[0]
        if cleaned_name in correction_list:
            cleaned_name = correction_list[cleaned_name]
        if cleaned_name and cleaned_name not in cleaned_names:
            cleaned_names.append(cleaned_name)
    return cleaned_names

# Get first two or three occupations
def get_occupations(infobox_data):
    """
    Get a celebrity's first two or three occupations on Wikipedia

    Args:
    Infobox: the infobox of the celebrity

    Returns:
    A list of the first two or three occupations on wiki page
    """
    all_occupations = infobox_data.get("occupation") or infobox_data.get("occupations")
    cleaned_occupations = all_occupations.replace("*", "|")
    raw_occupation_list = cleaned_occupations.split("|")
    occupation_list = []
    for occupation in raw_occupation_list:
        lower_occupation = occupation.strip().lower()
        cleaned_occupation = ''.join([char for char in lower_occupation if char.isalpha()])
        occupation_list.append(cleaned_occupation)
    return occupation_list[1:4]

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
    with open('Data/raw_api_data.json', 'r') as f:
        for line in f:
            if not line:  
                continue 
            data = json.loads(line.strip())
            return data[0]['net_worth']
