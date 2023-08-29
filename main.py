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
        print(e)
        return -1
    
def get_completion_status(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()


    overall_status_element = root.find('overall_status')

    try:
        overall_status = overall_status_element.text
        return overall_status
    except Exception as e:
        print(e)
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

current_dir = os.getcwd()
folder_path = f'{current_dir}/data'

if os.path.exists(folder_path) and os.path.isdir(folder_path):

    file_names = os.listdir(folder_path)
    enrollment_tags_present, total_files, completed_status = 0, 0, 0
    enrollment_type_count = {}
    date_formats_for_duration = [0] * 3
    number_of_months = []
    for file_name in file_names:
        total_files += 1
        result = get_enrollment(f'{folder_path}/{file_name}')
        if result == -1:
            print(f'{file_name} -> Enrollment tag absent')
        else:
            enrollment_tags_present += 1
            if result[0] in enrollment_type_count:
                enrollment_type_count[result[0]] += 1
            else:
                enrollment_type_count[result[0]] = 1
            print(f'{file_name} -> {result[0]}, {result[1]} ')

        
        duration = get_completion_status(f'{folder_path}/{file_name}')


        if duration == 'Completed':
            completed_status += 1

        format = get_date_format(f'{folder_path}/{file_name}')
        if format[0] != -1:
            date_formats_for_duration[format[0]] += 1
            if format[0] == 2:
                number_of_months.append(get_average(format[1], format[2]))

            
    

print(f'Total files : {total_files}')
print(f'Number of Actual, Anticipated, None tags: {enrollment_type_count}')
print(f'Number of files with enrollment tag : {enrollment_tags_present}')

print(f'Completed studies : {completed_status}')

print(f'Date formats : {date_formats_for_duration}')

freq_of_months = np.bincount(number_of_months)

plt.hist(freq_of_months, bins=50, edgecolor='black')
# plt.bar(range(len(freq_of_months)), freq_of_months, tick_label=range(len(freq_of_months)))
plt.show()
print(min(number_of_months), max(number_of_months))