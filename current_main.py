import xml.etree.ElementTree as ET
import os
import pandas as pd
from datetime import datetime

def get_start_date(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()

    start_date_element = root.find('start_date')
    try:
        return start_date_element.text
    except Exception as e:
        return None

def get_end_date(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()

    end_date_element = root.find('completion_date')
    end_date_completion_element = root.find('primary_completion_date')
    try:
        if end_date_element is not None:
            return end_date_element.text
        elif end_date_completion_element is not None:
            return end_date_completion_element.text
        else:
            return None
    except Exception as e:
        return None

def get_location(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()

    location_country = root.find('location_countries/country')

    try:
        return location_country.text
    except Exception as e:
        return None
    


def get_text_data(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()

    brief_summary_element = root.find('brief_summary/textblock')
    detailed_desc_element = root.find('detailed_description/textblock')
    eligibility_element = root.find('eligibility/criteria/textblock')

    text = ""

    try:
        text += brief_summary_element.text
    except Exception as e:
        text += ""

    try:
        text += detailed_desc_element.text
    except Exception as e:
        text += ""

    try:
        text += eligibility_element.text
    except Exception as e:
        text += ""
    return text


def get_enrollment_data(file_name):
    tree = ET.parse(f'{file_name}')
    root = tree.getroot()

    enrollment_element = root.find('enrollment')
    try:
        enrollment_type = enrollment_element.get('type')
        enrollment_value = enrollment_element.text

        if enrollment_type == "Actual":
            return int(enrollment_value)
        else:
            return 0
    except Exception as e:
        return 0


column= ['file_id', 'start_date', 'end_date', 'location', 'text', 'enrollment']
current_dir = os.getcwd()
folder_path = f'{current_dir}/data'

if os.path.exists(folder_path) and os.path.isdir(folder_path):

    file_names = os.listdir(folder_path)
    data = []
    for file_name in file_names:
        if not file_name.endswith(".xml"):
            continue

        file_path = f'{folder_path}/{file_name}'
        start_date = get_start_date(file_path)
        end_date = get_end_date(file_path)

        location = get_location(file_path)
        
        text_data = get_text_data(file_path)
        enrollment = get_enrollment_data(file_path)

        data.append([file_name, start_date, end_date, location, text_data, enrollment])

df = pd.DataFrame(data = data, columns=column)

df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')

df['DaysBetween'] = (df['end_date'] - df['start_date']).dt.days.where(df['start_date'].notna() & df['end_date'].notna())
df['Enrollment_rate'] = df['enrollment'] / df['DaysBetween']
df['Enrollment_rate'] = df['Enrollment_rate'].fillna(0)
df.to_csv('output.csv', index=False)
