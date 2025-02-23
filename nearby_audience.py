import requests
import time
import math
import sys
from datetime import datetime, timedelta
from pprint import pprint

# Ensure the current directory is in the path to import store_target_audience.py
sys.path.append(".")

GOOGLE_API_KEY = "AIzaSyDhVgRxfBbURvJSiMpUPrGzi5qzHLGrN4Q"

def get_lat_long(address):
    """
    Converts a street address to latitude/longitude using the Google Geocoding API.
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None, None

def get_fips_codes(lat, lng):
    url = f"https://geo.fcc.gov/api/census/block/find?latitude={lat}&longitude={lng}&format=json"
    response = requests.get(url)
    data = response.json()

    if "Block" in data and "FIPS" in data["Block"]:
        block_fips = data["Block"]["FIPS"]
        state_fips = block_fips[:2]
        county_fips = block_fips[2:5]
        return state_fips, county_fips
    return None, None

def get_census_data(state_fips, county_fips):
    url = "https://api.census.gov/data/2021/acs/acs5/profile"
    params = {
        "get": "DP05_0018E,DP03_0062E",
        "for": f"county:{county_fips}",
        "in": f"state:{state_fips}"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if len(data) > 1:
            return {
                "median_age": float(data[1][0]),
                "median_income": int(float(data[1][1]))
            }
    return None

def analyze_nearby_audience(address):
    from store_target_audience import predict_target_age_income  # Lazy import to prevent circular dependency
    address = address.replace(" ", "+")
    lat, lng = get_lat_long(address)
    if lat is None or lng is None:
        print("Error: Unable to fetch latitude/longitude")
        return
    
    state_fips, county_fips = get_fips_codes(lat, lng)
    if state_fips is None or county_fips is None:
        print("Error: Unable to fetch local FIPS codes")
        return
    
    store_audience = predict_target_age_income(address, state_fips, county_fips)
    local_audience = get_census_data(state_fips, county_fips)

    if local_audience:
        print(f"\n📍 **Store vs Nearby Audience for {address}**")
        print(f"  - Store Target Age Range: {store_audience['age']}")
        print(f"  - Nearby Median Age: {local_audience['median_age']} years")
        print(f"  - Store Target Income Range: {store_audience['income']}")
        print(f"  - Nearby Median Income: ${local_audience['median_income']}")

        age_match = (
            max(0, min(store_audience["age"][1], local_audience["median_age"]) - 
                max(store_audience["age"][0], local_audience["median_age"])) /
            (store_audience["age"][1] - store_audience["age"][0]) if store_audience["age"] != "Unknown" else 0
        )

        income_match = (
            max(0, min(store_audience["income"][1], local_audience["median_income"]) - 
                max(store_audience["income"][0], local_audience["median_income"])) /
            (store_audience["income"][1] - store_audience["income"][0]) if store_audience["income"] != "Unknown" else 0
        )

        total_match_score = (age_match + income_match) / 2 * 100
        print(f"  - **Match Score: {total_match_score:.2f}%**")

if __name__ == "__main__":
    address = "Tin Drum Asian Kitchen & Boba Tea Bar, 88 5th St NW, Atlanta, GA 30308"
    analyze_nearby_audience(address)
