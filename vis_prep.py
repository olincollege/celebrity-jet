"""Functions that prepare data for visualization"""


# Categorize by occupation
def get_emissions_for_occupation(celeb_info, jet_info, occupation):
    """Gets the emissions for a given occupation."""
    # Filter celebrities by occupation
    celebs = [
        name for name, info in celeb_info.items() if info[0] == occupation
    ]

    emissions = []
    # Collect emissions data for celebrities in the given occupation
    for name in celebs:
        if name in jet_info and jet_info[name][6]:
            emissions.append(int(jet_info[name][6]))

    # Calculate the average emissions for this occupation
    avg_emissions = sum(emissions) / len(emissions) if emissions else 0
    return avg_emissions


def get_all_occupation_emissions(celeb_info, jet_info):
    """Runs the emissions calculation for all occupations."""
    # Define the occupations for which emissions will be calculated
    occupations = [
        "Music",
        "Movie",
        "Business & Politics",
        "TV & Media",
        "Sports",
    ]
    emissions = []
    # Calculate emissions for each occupation
    for occupation in occupations:
        emissions.append(
            get_emissions_for_occupation(celeb_info, jet_info, occupation)
        )
    return occupations, emissions


# Categorize by age group
def get_emissions_for_age_group(celeb_info, jet_info, age_range):
    """Gets the emissions for a given age group."""
    # Filter celebrities by the specified age range
    celebs = [
        name
        for name, info in celeb_info.items()
        if age_range[0] <= int(info[1]) <= age_range[1]
    ]

    emissions = []
    # Collect emissions data for celebrities in the given age range
    for name in celebs:
        if name in jet_info and jet_info[name][6]:
            emissions.append(int(jet_info[name][6]))

    # Calculate the average emissions for this age group
    avg_emissions = sum(emissions) / len(emissions) if emissions else 0
    return avg_emissions


def get_all_age_emissions(celeb_info, jet_info):
    """Runs the emissions calculation for all age groups."""
    # Define the age groups to categorize emissions
    age_groups = {
        "Below 40": [0, 39],
        "40-49": [40, 49],
        "50-59": [50, 59],
        "60-69": [60, 69],
        "70-79": [70, 79],
        "Above 79": [80, 100],
    }
    emissions = []
    age_group_list = []
    # Calculate emissions for each age group
    for age_group, age_range in age_groups.items():
        age_group_list.append(age_group)
        emissions.append(
            get_emissions_for_age_group(celeb_info, jet_info, age_range)
        )
    return age_group_list, emissions


# Categorize by net worth
def get_emissions_for_net_worth(celeb_info, jet_info, net_worth_range):
    """Gets the emissions for a given net worth range."""
    celebs = []
    # Filter celebrities by net worth range
    for name, info in celeb_info.items():
        if (
            info[2] != "N/A"
            and net_worth_range[0] <= int(info[2]) <= net_worth_range[1]
        ):
            celebs.append(name)

    emissions = []
    # Collect emissions data for celebrities in the specified net worth range
    for name in celebs:
        if name in jet_info and jet_info[name][6]:
            emissions.append(int(jet_info[name][6]))

    # Calculate the average emissions for this net worth range
    avg_emissions = sum(emissions) / len(emissions) if emissions else 0
    return avg_emissions


def get_all_net_worth_emissions(celeb_info, jet_info):
    """Runs the emissions calculation for all net worth ranges."""
    # Define net worth ranges to categorize emissions
    net_worth_groups = {
        "Below 100M": [0, 100000000],
        "100M - 500M": [100000001, 500000000],
        "500M - 1B": [500000001, 1000000000],
        "1B - 10B": [1000000001, 10000000000],
        "10B - 50B": [10000000001, 50000000000],
        "Above 50B": [50000000001, 10000000000000000],
    }
    emissions = []
    net_worth_group_list = []
    # Calculate emissions for each net worth group
    for net_worth_group, net_worth_range in net_worth_groups.items():
        net_worth_group_list.append(net_worth_group)
        emissions.append(
            get_emissions_for_net_worth(celeb_info, jet_info, net_worth_range)
        )
    return net_worth_group_list, emissions
