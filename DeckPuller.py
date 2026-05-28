import requests
import urllib

def get_deck_data(public_id: str):
    api_url = f"https://api.moxfield.com/v2/decks/all/{public_id}"
    headers = {"User-Agent": "PersonalDeckAnalyzer"}
    response = requests.get(api_url, headers=headers)
    SUCCESS = 200
    if response.status_code == SUCCESS:
        return response.json()
    else:
        raise Exception(f"Failed to fetch deck: HTTP {response.status_code}")

def extract_deck_id(deck_url: str) -> str:
    deck_sections = deck_url.split("/")
    deck_id = deck_sections[len(deck_sections) - 1]
    return deck_id

def is_url(str: str) -> bool:
    min_components = ('scheme', 'netloc')
    present_url_components = urllib.parse.urlparse(str)
    
    for component in min_components:
        if(getattr(present_url_components, component) == ""):
            return False
    
    return True

def get_deck_info(deck_url: str):
    if not is_url(deck_url):
        return None
    deck_id = extract_deck_id(deck_url)
    deck_data = get_deck_data(deck_id)
    return deck_data