import xml.etree.ElementTree as ET
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

import string

# # Your input text
# text = "Hello, this is an example text with some punctuation marks! How are you?"

# # Remove punctuation using string.punctuation
# translator = str.maketrans(' ', '', string.punctuation)
# cleaned_text = text.translate(translator)

# # Print the cleaned text
# print(cleaned_text)



# global variables

enrollment_tags_present, total_files, completed_status = 0, 0, 0
enrollment_type_count = {}
date_formats_for_duration = [0] * 3
number_of_months = []
count_facility_name, count_facility_address = 0, 0
countries_of_facilities = {}
gender_details = {}
min_age_details = {}
max_age_details = {}
gender_count = 0
min_age_count = 0
max_age_count = 0
min_age_NA = 0
max_age_NA = 0

file_name_list = []
enrollment_rate_list = []
duration_list = []
start_date_list = []
completion_date_list = []
text_data = []


def get_enrollment(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()

    enrollment_element = root.find('enrollment')
    try:
        enrollment_type = enrollment_element.get('type')
        enrollment_value = enrollment_element.text

        return (enrollment_type, enrollment_value)

    except Exception as e:
        # print(e)
        return -1
    
def get_completion_status(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()


    overall_status_element = root.find('overall_status')

    try:
        overall_status = overall_status_element.text
        return overall_status
    except Exception as e:
        # print(e)
        return -1
    
def get_average(date1, date2):
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    month1, year1 = date1.split()
    month2, year2 = date2.split()
    
    numerical_date1 = int(year1) * 12 + month_names.index(month1)
    numerical_date2 = int(year2) * 12 + month_names.index(month2)
    
    difference = abs(numerical_date1 - numerical_date2)
    
    return difference



def get_date_format(file_name):

    tree = ET.parse(f'{file_name}')
    root = tree.getroot()

    start_date_element = root.find('start_date')
    end_date_element = root.find('completion_date')
    end_date_completion_element = root.find('primary_completion_date')
    date_formats = ["%Y-%m", "%m/%Y", "%m-%Y","%Y %m", "%m %Y", "%m %Y","%m %d, %Y"]
    
    pattern = r"^(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}$"
    if root.find('completion_date') is None and root.find('primary_completion_date') is not None:
        end_date_element = end_date_completion_element

    # print(start_date_element.text)
    # print(end_date_element.text)
    flag=0
    for date_format in date_formats:
        try:
            date_obj = datetime.strptime(start_date_element.text, date_format)
            date_obj_end = datetime.strptime(end_date_element.text, date_format)

            start_date_list.append(date_obj)
            completion_date_list.append(date_obj_end)
            flag = 1
            return 2
        except ValueError:
                pass
    if (flag==0):
        start_date_list.append("00")
        completion_date_list.append("00")

    
        # if re.match(pattern, start_date_element.text) and re.match(pattern, end_date_element.text):
        #     start_date_list.append(start_date_element.text)
        #     completion_date_list.append(end_date_element.text)

        #     return (2, start_date_element.text, end_date_element.text)
        # elif re.match(pattern, start_date_element.text) or re.match(pattern, end_date_element.text):
        #     start_date_list.append(start_date_element.text)
        #     completion_date_list.append(end_date_element.text)
            
        #     return (1, start_date_element.text, end_date_element.text)
        # else:
        #     start_date_list.append(start_date_element.text)
        #     completion_date_list.append(end_date_element.text)

        #     return (0, start_date_element.text, end_date_element.text)
    # except Exception as e:

        # start_date_list.append("00")
        # completion_date_list.append("00")

        # return (-1, -1, -1)
    
def get_criteria(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()
    try:
        eligibility_details = root.find('eligibility')
        criteria = eligibility_details.find('criteria')
        text_data = criteria.find('textblock').text
        return text_data
        # if gender in gender_details:
        #     gender_details[gender] += 1
        # else:
        #     gender_details[gender] = 1
        # print(f'{file_name} -> {gender} ')

    except Exception as e:
        print(e)
        return ""


def get_address_of_trial(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()

    facility_element = root.find('location/facility')
    response = {}

    try:
        name_of_facility = facility_element.find('name').text
        response["name"] = name_of_facility
    except Exception as e:
        response["name"] = ""
    
    try:
        address_of_facility = facility_element.find('address')
        location_of_facility = {}
        for params in address_of_facility:
            location_of_facility[params.tag] = params.text
        response["address"] = location_of_facility
    except Exception as e:
        response["address"] = {}


    return response

def get_location_countries(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()

    location_country = root.find('location_countries')

    try:
        resp = {}
        for params in location_country:
            resp[params.tag] = params.text
        return resp
    except Exception as e:
        return {}

def get_eligibility_details(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()
    try:
        eligibility_details = root.find('eligibility')
        gender = eligibility_details.find('gender').text
        if gender in gender_details:
            gender_details[gender] += 1
        else:
            gender_details[gender] = 1
        # print(f'{file_name} -> {gender} ')

    except Exception as e:
        print(e)
        return -1
    
    try: 
        min_age = eligibility_details.find('minimum_age').text
        if min_age in min_age_details:
            min_age_details[min_age] += 1
        else:
            min_age_details[min_age] = 1
        # print(f'{file_name} -> {min_age} ')

    except Exception as e:
        print(e)
        return -1
    
    try:
        max_age = eligibility_details.find('maximum_age').text
        if max_age in max_age_details:
            max_age_details[max_age] += 1
        else:
            max_age_details[max_age] = 1
        # print(f'{file_name} -> {max_age} ')

    except Exception as e:
        print(e)
        return -1
    

current_dir = os.getcwd()
folder_path = f'{current_dir}/data'

if os.path.exists(folder_path) and os.path.isdir(folder_path):

    file_names = os.listdir(folder_path)
    for file_name in file_names:
        enrollment_count = 0
        num_of_days = 1

        if not file_name.endswith(".xml"):
            continue
        total_files += 1
        file_name_list.append(file_name)
        result = get_eligibility_details(f'{folder_path}/{file_name}')
        if result == -1:
            pass

        result = get_enrollment(f'{folder_path}/{file_name}')
        if result == -1:
            pass
            # print(f'{file_name} -> Enrollment tag absent')
        else:
            enrollment_tags_present += 1
            enrollment_count = result[1]
            if result[0] in enrollment_type_count:
                enrollment_type_count[result[0]] += 1
            else:
                enrollment_type_count[result[0]] = 1
            # print(f'{file_name} -> {result[0]}, {result[1]}')

        
        duration = get_completion_status(f'{folder_path}/{file_name}')

        if duration == 'Completed':
            completed_status += 1

        format = get_date_format(f'{folder_path}/{file_name}')
        # if format[0] != -1:
        #     date_formats_for_duration[format[0]] += 1
        #     if format[0] == 2:
        #         month_freq = get_average(format[1], format[2])
        #         number_of_months.append(month_freq)
        #         num_of_days = 30*month_freq
        #         num_of_days = max(num_of_days,1)
        
        enrollment_rate_list.append(int(enrollment_count)/num_of_days)
        duration_list.append(num_of_days)

        # Get Textual Data
        text_dt = get_criteria(f'{folder_path}/{file_name}')
        if text_dt !="":
            text_data.append(text_dt)
        else:
            print()

        # Get address
        facilities = get_address_of_trial(f'{folder_path}/{file_name}')
        if facilities["name"] != "":
            count_facility_name += 1
        if facilities["address"] != {}:
            count_facility_address += 1

        location_country = get_location_countries(f'{folder_path}/{file_name}')
        if "country" in location_country:
            if location_country["country"] in countries_of_facilities:
                countries_of_facilities[location_country["country"]] += 1
            else:
                countries_of_facilities[location_country["country"]] = 1
        # print(f'{file_name} -> {location_country}')

# print(len(file_name_list))
# print(len(enrollment_rate_list))
# print(len(start_date_list))
# print(len(completion_date_list))
dict = {'file_name': file_name_list, 'enrollment_rate': enrollment_rate_list, 'duration': duration_list, 'start_date': start_date_list, 'completion_date':completion_date_list}

df = pd.DataFrame(dict)
df.to_csv('file1.csv')
          

# print(f'Total files : {total_files}')
# print(f'Number of Actual, Anticipated, None tags: {enrollment_type_count}')
# print(f'Number of files with enrollment tag : {enrollment_tags_present}')

# print(f'Completed studies : {completed_status}')

# print(f'Date formats : {date_formats_for_duration}')

# freq_of_months = np.bincount(number_of_months)

# plt.title('Frequency of Trial Duration')
# plt.ylabel('Count')
# plt.xlabel('Number of Months')
# plt.hist(freq_of_months, bins=50, edgecolor='black')
# # plt.bar(range(len(freq_of_months)), freq_of_months, tick_label=range(len(freq_of_months)))
# plt.show()
# # print(min(number_of_months), max(number_of_months))


# print(f'Number of facilities with name -> {count_facility_name}, address -> {count_facility_address}')
# print(countries_of_facilities)


for key in gender_details:
    # print(key, gender_details[key])
    gender_count +=gender_details[key]

for key in min_age_details:
    # print(key, min_age_details[key])
    min_age_count +=min_age_details[key]

for key in max_age_details:
    # print(key, max_age_details[key])
    max_age_count +=max_age_details[key]

min_age_NA = min_age_details["N/A"]
max_age_NA = max_age_details["N/A"]

# print(f'Total gender count is : {gender_count}')
# print(f'Total min_age_count is : {max_age_count}')
# print(f'Total max_age_count is : {min_age_count}')
# print(f'Total min_age_N/A count is: {min_age_NA}')
# print(f'Total max_age_N/A count is: {max_age_NA}')
