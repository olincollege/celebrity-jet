import manipulate_data as md
import wptools
import celebrity_info_scrap as scrap
import json

manipulate_data.get_flighttracking()
celebrity_data_chunks = manipulate_data.get_celeb_chunks()
celebrity_data = manipulate_data.get_celeb_data(celebrity_data_chunks)
manipulate_data.clean_all_data(celebrity_data)
print(manipulate_data.combine_duplicates(celebrity_data))
