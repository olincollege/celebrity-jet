# Library to get data ready for visualization

# Categorize by occupation
def get_emissions_for_occupation(celeb_info, jet_info, occupation):
    """Gets the emissions for a given occupation."""
    celebs = [
        name for name, info in celeb_info.items() if info[0] == occupation
    ]

    emissions = []
    for name in celebs:
        if name in jet_info and jet_info[name][6]:
            emissions.append(int(jet_info[name][6]))

    avg_emissions = sum(emissions) / len(emissions) if emissions else 0
    return avg_emissions


def get_all_occupation_emissions(celeb_info, jet_info):
    """Runs the emissions calculation for all occupations."""
    occupations = [
        "Music",
        "Movie",
        "Business & Politics",
        "TV & Media",
        "Sports",
    ]
    emissions = []
    for occupation in occupations:
        emissions.append(get_emissions_for_occupation(celeb_info, jet_info, occupation))
    return occupations, emissions


# Categorize by age group
def get_emissions_for_age_group(celeb_info, jet_info, age_range):
    """Gets the emissions for a given occupation."""
    celebs = [
        name for name, info in celeb_info.items() if age_range[0] <= int(info[1]) <= age_range[1]
    ]

    emissions = []
    for name in celebs:
        if name in jet_info and jet_info[name][6]:
            emissions.append(int(jet_info[name][6]))

    avg_emissions = sum(emissions) / len(emissions) if emissions else 0
    return avg_emissions


def get_all_age_emissions(celeb_info, jet_info):
    """Runs the emissions calculation for all occupations."""
    age_groups = {
        "Below 40":[0, 39],
        "40-49":[40, 49],
        "50-59":[50, 59],
        "60-69":[60, 69],
        "70-79":[70, 79],
        "Above 79":[80, 100]
    }
    emissions = []
    age_group_list = []
    for age_group, age_range in age_groups.items():
        age_group_list.append(age_group)
        emissions.append(get_emissions_for_age_group(celeb_info, jet_info, age_range))
    return age_group_list, emissions


# # Categorize by net worth
# def get_emissions_for_net_worth(celeb_info, jet_info, net_worth_range):
#     """Gets the emissions for a given occupation."""
#     celebs = [
#         name for name, info in celeb_info.items() if net_worth_range[0] <= int(info[1]) <= net_worth_range[1]
#     ]

#     emissions = []
#     for name in celebs:
#         if name in jet_info and jet_info[name][6]:
#             emissions.append(int(jet_info[name][6]))

#     avg_emissions = sum(emissions) / len(emissions) if emissions else 0
#     return avg_emissions


# def get_all_net_worth_emissions(celeb_info, jet_info):
#     """Runs the emissions calculation for all occupations."""
#     age_groups = {
#         "Below 40":[0, 39],
#         "40-49":[40, 49],
#         "50-59":[50, 59],
#         "60-69":[60, 69],
#         "70-79":[70, 79],
#         "Above 79":[80, 100]
#     }
#     emissions = []
#     age_group_list = []
#     for age_group, age_range in age_groups.items():
#         age_group_list.append(age_group)
#         emissions.append(get_emissions_for_age_group(celeb_info, jet_info, age_range))
#     return age_group_list, emissions
