import re
import pandas as pd
import numpy as np


def clean_sample_size(sample):
    # Extract the first number found in the string
    sample = str(sample)
    if sample == "192 users + 1700 control":
        return 192 + 1700
    if "Bipolar: 394 users, 992k tweets\nDepression: 441 users" in sample:
        return 394+441+244+159+5728
    if "327 depres-\nsion users, 246 PTSD users" in sample :
        return 1146+600
    else :
        match = re.search(r'\d+', sample)
        return int(match.group()) if match else 'Not specified'


def clean_percentage_male(percentage):
    # Extract the first number found in the string
    percentage = str(percentage)
    match = re.search(r'\d+', percentage)
    return int(match.group()) if match else 'Not specified'

# Function to clean age (mean /SD)
def clean_age(age):
    age = str(age)
    # Extract the mean and SD if available
    match = re.search(r'(\d+\.?\d*)\s*[^\d]*\s*(\d+\.?\d*)?', age)
    if match:
        mean = float(match.group(1))
        sd = float(match.group(2)) if match.group(2) else 'Not specified'
        return f'{mean} (SD {sd})'
    else:
        return 'Not specified'
    
def clean_n_PTSD(n_ptsd):
    n_ptsd = str(n_ptsd)
    if n_ptsd =="Average initial PCL score = 33.7; S . D. = 16.2":
        return "Continous Scale"
    if  "continous" in n_ptsd.lower():
        return "Continous Scale"
    if "7.3 +- A on the GPS scale" in n_ptsd:
        return "Continous Scale"
    if "Mean values" in n_ptsd:
        return "Continous Scale"
    
    # Extract the first number found in the string
    match = re.search(r'\b\d+\b', n_ptsd)
    return int(match.group()) if match else 'Not specified'

def compute_prevalence_PTSD(row):
    if row['cleaned_n_PTSD'] == 'Not specified' or row['cleaned_sample_size'] == 'Not specified':
        return 'Not specified'
    if row['cleaned_n_PTSD'] == 'Continous Scale':
        return 'Continous Scale'
    else:
        return int(row['cleaned_n_PTSD']) / int(row['cleaned_sample_size']) * 100
    

def identify_event_types(event_type: str) -> list:
    event_type = event_type.lower()
    types = []
    
    if any(keyword in event_type for keyword in ['terrorist', 'terrorism', 'terrorist attack', '13/11', '11/9']):
        types.append('Terrorism')
    if any(keyword in event_type for keyword in ['military', 'combat', 'war', 'deployment', 'veteran']):
        types.append('Military/War')
    if any(keyword in event_type for keyword in ['covid', 'pandemic']):
        types.append('Pandemic')
    if any(keyword in event_type for keyword in ['sexual', 'rape', 'assault', 'abuse', 'intimate partner violence', 'domestic violence']):
        types.append('Sexual/Physical Violence')
    if any(keyword in event_type for keyword in ['accident', 'traffic', 'motor vehicle', 'industrial', 'road']):
        types.append('Accidents')
    if any(keyword in event_type for keyword in ['childbirth', 'post-delivery']):
        types.append('Childbirth')
    if any(keyword in event_type for keyword in ['natural disaster', 'earthquake', 'hurricane', 'flood']):
        types.append('Natural Disasters')
    if any(keyword in event_type for keyword in ['genocide']):
        types.append('Genocide')
    if 'not specified' in event_type or 'various traumatic experiences' in event_type:
        types.append('Heterogeneous Events')
    
    return types

def categorize_event_2(event_type: str) -> str:
    types = identify_event_types(event_type)
    if len(types) >= 3:
        return 'Heterogeneous Events'
    elif "Military/War" in types : 
        return 'Military/War'
    elif "Sexual/Physical Violence" in types :
        return 'Sexual/Physical Violence'
    elif len(types) == 0:
        return 'Heterogeneous Events'
    else:
        return ', '.join(types)


def is_specified(date_str):
    if date_str is None:
        return 'Not Specified'
    if type(date_str) != str:
        return 'Not Specified'
    
    if 'not specified' in date_str.lower() or 'na' in date_str.lower() or date_str == "":
        return 'Not Specified'
    else:
        return 'Specified'
    
def normalize_exclusion_criteria(criteria):
    criteria = str(criteria)
    criteria = criteria.lower()
    if "psychosis" in criteria or "bipolar" in criteria:
        return "Psychiatric disorders"
    elif "alcohol" in criteria or "substance" in criteria:
        return "Substance use"
    elif "language" in criteria or "fluent" in criteria:
        return "Language fluency"
    elif "trauma" in criteria:
        return "Trauma experience"
    else:
        return "Other"
    
def normalize_recruitment_method(method):
    if type(method) != str:
        return "Not specified"
    method = method.lower()
    if "word of mouth" in method or "flyers" in method:
        return "Word of mouth / Flyers"
    elif "craigslist" in method or "mturk" in method:
        return "Online platforms"
    elif "online survey" in method:
        return "Online survey"
    elif "referrals" in method or "referred" in method:
        return "Referrals"
    elif "emergency department" in method or "hospital" in method:
        return "Hospital"
    elif "twitter" in method or "social media" in method:
        return "Social media"
    elif "not specified" in method:
        return "Not specified"
    else:
        return "Other"
    
def normalize_inclusion_criteria(criteria):
    criteria = str(criteria)
    criteria = criteria.lower()
    if "age" in criteria:
        return "Age"
    elif "diagnosis" in criteria or "diagnosed" in criteria:
        return "Diagnosis"
    elif "language" in criteria or "fluent" in criteria:
        return "Language fluency"
    elif "trauma" in criteria:
        return "Trauma experience"
    else:
        return "Other"
    
from utils import categories_recruitment_methods

def categorize_recruitment_method(method):
    for category, keywords in categories_recruitment_methods.items():
        if any(keyword in method for keyword in keywords):
            return category
    return "Miscellaneous and Not Specified"

def is_specified_criteria(criteria):
    if criteria is None:
        return 'Not Specified'
    if type(criteria) != str:
        return 'Not Specified'
    
    if 'not specified' in criteria.lower() or 'na' in criteria.lower() or criteria == "":
        return 'Not Specified'
    else:
        return 'Specified'