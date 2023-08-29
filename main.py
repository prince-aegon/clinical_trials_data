import xml.etree.ElementTree as ET
import os
import re
import matplotlib.pyplot as plt
import numpy as np

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

    pattern = r"^(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}$"
    try:
        if re.match(pattern, start_date_element.text) and re.match(pattern, end_date_element.text):
            return (2, start_date_element.text, end_date_element.text)
        elif re.match(pattern, start_date_element.text) or re.match(pattern, end_date_element.text):
            return (1, start_date_element.text, end_date_element.text)
        else:
            return (0, start_date_element.text, end_date_element.text)
    except Exception as e:
        return (-1, -1, -1)
    

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



    

current_dir = os.getcwd()
folder_path = f'{current_dir}/data'

if os.path.exists(folder_path) and os.path.isdir(folder_path):

    file_names = os.listdir(folder_path)
    enrollment_tags_present, total_files, completed_status = 0, 0, 0
    enrollment_type_count = {}
    date_formats_for_duration = [0] * 3
    number_of_months = []
    count_facility_name, count_facility_address = 0, 0
    countries_of_facilities = {}

    for file_name in file_names:
        if not file_name.endswith(".xml"):
            continue
        total_files += 1
        
        result = get_enrollment(f'{folder_path}/{file_name}')
        if result == -1:
            pass
            # print(f'{file_name} -> Enrollment tag absent')
        else:
            enrollment_tags_present += 1
            if result[0] in enrollment_type_count:
                enrollment_type_count[result[0]] += 1
            else:
                enrollment_type_count[result[0]] = 1
            # print(f'{file_name} -> {result[0]}, {result[1]}')

        
        duration = get_completion_status(f'{folder_path}/{file_name}')


        if duration == 'Completed':
            completed_status += 1

        format = get_date_format(f'{folder_path}/{file_name}')
        if format[0] != -1:
            date_formats_for_duration[format[0]] += 1
            if format[0] == 2:
                number_of_months.append(get_average(format[1], format[2]))

        
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
        print(f'{file_name} -> {location_country}')


            


print(f'Total files : {total_files}')
print(f'Number of Actual, Anticipated, None tags: {enrollment_type_count}')
print(f'Number of files with enrollment tag : {enrollment_tags_present}')

print(f'Completed studies : {completed_status}')

print(f'Date formats : {date_formats_for_duration}')

freq_of_months = np.bincount(number_of_months)

plt.title('Frequency of Trial Duration')
plt.ylabel('Count')
plt.xlabel('Number of Months')
plt.hist(freq_of_months, bins=50, edgecolor='black')
# plt.bar(range(len(freq_of_months)), freq_of_months, tick_label=range(len(freq_of_months)))
plt.show()
# print(min(number_of_months), max(number_of_months))


print(f'Number of facilities with name -> {count_facility_name}, address -> {count_facility_address}')
print(countries_of_facilities)
