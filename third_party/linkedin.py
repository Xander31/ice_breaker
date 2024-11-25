import os
from http.client import responses

import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    """
    scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile
    """
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/Xander31/42bc34f7cf26b3a70332beea2b5dd5a1/raw/06a5b291fde63a1641eb3046715473f3a3a0f708/alvaro_espinoza.json"
        response = requests.get(
            url=linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        headers = {'Authorization':f'Bearer {os.getenv("PROXYCURL_API_KEY")}'}
        params = {
            'linkedin_profile_url' : linkedin_profile_url
        }
        response = requests.get(
            url=api_endpoint,
            headers=headers,
            params=params,
            timeout=10,
        )
    data = response.json()

    #Removing the empty fields (to save tokens when passing the info to the LLM
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], " ", "", None)
           and k not in ("people_also_viewed", "certifications")
    }
    #Removing profiles picture from the groups as they are not needed
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return  data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/alvaro-espinoza-h/",
            #linkedin_profile_url="https://www.linkedin.com/in/rafael-pachon-a3704710/",
            mock=True
        )
    )





