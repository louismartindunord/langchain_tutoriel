from math import nan
import os
import requests
from dotenv import load_dotenv
from os.path import join
load_dotenv()


def clean_json_data(data):
    ### Permet de supprimer les valeurs non utiles du Json afin d'éviter de les tokenizer et faire des économies
    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            if k not in ["people_also_viewed", "certifications"] and v not in ([], "", None, " None"):
                new_data[k] = clean_json_data(v)
        return new_data
    elif isinstance(data, list):
        return [clean_json_data(v) for v in data if v not in ([], "", None, " None")]
    else:
        return data


def scrape_linkedin_profile(linkedin_profile_url: str):
    """
    Scrape information from Linkedin profile, 
    Manually scrape information from the linkedin profile 
    """
    nubela_api_key = os.environ.get("NUBELA")
    headers = {'Authorization': 'Bearer ' + nubela_api_key}
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    params = {
        'linkedin_profile_url': linkedin_profile_url,
        'extra': 'include',
        'personal_contact_number': 'include',
        'personal_email': 'include',
        'inferred_salary': 'include',
        'skills': 'include',
        'use_cache': 'if-present',
        'fallback_to_cache': 'on-error',
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=headers)  
       
    data = response.json()
    #data = requests.get("https://gist.githubusercontent.com/louismartindunord/954c045282addcee4b9689f23b0cfc99/raw/c0f9a7cf7438419117d394cb2f45fc1aa5da2e57/louis_mn.json").json()
    data = clean_json_data(data)
    return data
          
 