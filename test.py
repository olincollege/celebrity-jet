import manipulate_data as md
import wptools
import celebrity_info_scrap as scrap
import json


def get_celeb_info_wapi():
    with open("Data/raw_api_data.json", "w") as f:
        for name in cleaned_names:
            try:
                response = md.get_apininjas_data(name)
                if not response:
                    json.dump([], f)
                else:
                    json.dump(response, f)
                f.write("\n")
            except Exception:
                pass


def get_jet_owner_info(cleaned_names):
    with open("Data/jet_owners_info.csv", "w") as f:
        for name in cleaned_names:
            # Get and parse the infobox, if applicable
            try:
                content = wptools.page(name).get_parse()
                infobox = content.data["infobox"]
            except LookupError:
                f.write("Wikipage of {name} not found")
                continue

            # Get their occupations and age, if applicable
            try:
                occupations = scrap.get_occupations(infobox)
            except AttributeError:
                occupations = None
            try:
                age = scrap.get_age(infobox)
            except AttributeError:
                age = None

            # Get their net worth, if applicable
            try:
                net_worth = scrap.get_net_worth()
            except AttributeError:
                net_worth = None

            f.write(f"{name}, {occupations}, {age}, {net_worth}\n")


data_chunks = md.get_celeb_chunks()
name_list = md.get_celeb_data(data_chunks)
cleaned_names = scrap.fix_names(name_list)
# get_celeb_info_wapi()
get_jet_owner_info(cleaned_names)
