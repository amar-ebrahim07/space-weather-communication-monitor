import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("NASA_API_KEY")

def get_flr(start, end):
    raw = requests.get("https://api.nasa.gov/DONKI/FLR", params={"startDate": start, "endDate": end, "api_key": API_KEY })
    raw.raise_for_status()
    return raw.json()



def get_cme(start, end):
    raw = requests.get("https://api.nasa.gov/DONKI/CME", params={"startDate": start, "endDate": end, "api_key": API_KEY})
    raw.raise_for_status()
    return raw.json()





def get_gst(start, end):
    raw = requests.get("https://api.nasa.gov/DONKI/GST", params={"startDate": start, "endDate": end, "api_key": API_KEY})
    raw.raise_for_status()
    return raw.json()
