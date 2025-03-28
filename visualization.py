# Library to visualize data
import manipulate_data as md
import celebrity_info_scrap as scrap
import matplotlib.pyplot as plt
import vis_prep as prep

celeb_info = md.create_dict("Data/jet_owners_info.json")

data_chunks = md.get_celeb_chunks()
jet_info = md.get_celeb_data(data_chunks)
md.clean_all_data(jet_info)


# jet_info:
# CELEBRITY OWNER
# 0 AIRCRAFT MODEL
# 1 REGISTRATION
# 2 TOTAL MILES FLOWN
# 3 TOTAL FLIGHTS
# 4 TOTAL FUEL USED
# 5 TOTAL FLIGHT TIME
# 6 TOTAL CO2 POLLUTION

names = list(jet_info.keys())
occupation = [info[0] for info in celeb_info.values()]
jet_miles = [info[2] for info in jet_info.values()]


# Pie chart of private jet miles by owner
def plot_jet_miles_distribution(names, jet_miles):
    """Generates a pie chart showing the proportion of private jet miles for each owner."""
    plt.figure(figsize=(8, 8))
    plt.pie(jet_miles, labels=names, autopct="%1.1f%%")
    plt.axis("equal")
    plt.title("Proportion of Private Jet Miles for Each Owner")
    plt.show()


# Pie chart of carbon emissions by occupation
def plot_emissions_by_occupation():
    """Generates a pie chart displaying the proportion of total carbon emissions by occupation category."""
    occupations, emissions = prep.get_all_occupation_emissions(celeb_info, jet_info)
    plt.figure(figsize=(10, 6))
    plt.bar(occupations, emissions, color="skyblue")
    plt.title("Average CO2 Emissions by Occupation")
    plt.xlabel("Occupation")
    plt.ylabel("Average CO2 Emissions (metric tons)")

    plt.show()

    
# Histogram of carbon emissions by age group
def plot_emissions_by_age():
    """Plots a histogram showing the distribution of carbon emissions across different age groups."""
    
    age_group_list, emissions = prep.get_all_age_emissions(celeb_info, jet_info)
    plt.figure(figsize=(10, 6))
    plt.bar(age_group_list, emissions, color="orchid")
    plt.title("Average CO2 Emissions by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Average CO2 Emissions (metric tons)")

    plt.show()


# Histogram of carbon emissions by net worth
def plot_emissions_by_net_worth():
    """Plots a histogram illustrating the distribution of carbon emissions based on individuals' net worth."""
    pass
