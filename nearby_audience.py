import requests
import time
import math
import sys
from datetime import datetime, timedelta
from pprint import pprint


# Ensure the current directory is in the path to import store_target_audience.py
sys.path.append(".")


GOOGLE_API_KEY = "AIzaSyDhVgRxfBbURvJSiMpUPrGzi5qzHLGrN4Q"
API_KEY_SNAP = "O08DVAiFeIJWNEknkZSxk7Jel3W1dH23"

BUSINESS_AGE_INCOME_MAPPING = {
    "accounting": {"age": (25, 65), "income": (50000, 150000)},
    "airport": {"age": (18, 70), "income": (20000, 9999999999)},
    "amusement_park": {"age": (3, 60), "income": (20000, 100000)},
    "aquarium": {"age": (3, 70), "income": (20000, 100000)},
    "art_gallery": {"age": (18, 70), "income": (30000, 150000)},
    "atm": {"age": (18, 70), "income": (20000, 9999999999)},
    "bakery": {"age": (18, 70), "income": (20000, 80000)},
    "bank": {"age": (18, 70), "income": (40000, 150000)},
    "bar": {"age": (21, 60), "income": (20000, 90000)},
    "beauty_salon": {"age": (18, 60), "income": (20000, 100000)},
    "bicycle_store": {"age": (15, 50), "income": (30000, 90000)},
    "book_store": {"age": (18, 50), "income": (30000, 90000)},
    "bowling_alley": {"age": (10, 50), "income": (20000, 80000)},
    "bus_station": {"age": (18, 70), "income": (20000, 70000)},
    "cafe": {"age": (18, 50), "income": (20000, 80000)},
    "campground": {"age": (10, 70), "income": (30000, 100000)},
    "car_dealer": {"age": (25, 70), "income": (40000, 200000)},
    "car_rental": {"age": (21, 70), "income": (30000, 120000)},
    "car_repair": {"age": (18, 70), "income": (20000, 80000)},
    "car_wash": {"age": (18, 70), "income": (20000, 80000)},
    "casino": {"age": (21, 70), "income": (30000, 200000)},
    "cemetery": {"age": (40, 80), "income": (30000, 120000)},
    "church": {"age": (18, 80), "income": (20000, 100000)},
    "city_hall": {"age": (25, 70), "income": (40000, 150000)},
    "clothing_store": {"age": (15, 60), "income": (20000, 120000)},
    "convenience_store": {"age": (18, 60), "income": (20000, 80000)},
    "courthouse": {"age": (25, 70), "income": (50000, 200000)},
    "dentist": {"age": (5, 70), "income": (40000, 200000)},
    "department_store": {"age": (18, 70), "income": (30000, 120000)},
    "doctor": {"age": (5, 80), "income": (40000, 200000)},
    "drugstore": {"age": (18, 80), "income": (20000, 90000)},
    "electrician": {"age": (18, 60), "income": (30000, 90000)},
    "electronics_store": {"age": (18, 45), "income": (40000, 120000)},
    "embassy": {"age": (25, 70), "income": (50000, 200000)},
    "fire_station": {"age": (18, 60), "income": (30000, 90000)},
    "florist": {"age": (18, 70), "income": (20000, 90000)},
    "funeral_home": {"age": (40, 80), "income": (30000, 120000)},
    "furniture_store": {"age": (25, 70), "income": (30000, 150000)},
    "gas_station": {"age": (18, 70), "income": (20000, 80000)},
    "gym": {"age": (18, 50), "income": (40000, 100000)},
    "hair_care": {"age": (18, 60), "income": (20000, 100000)},
    "hardware_store": {"age": (18, 70), "income": (30000, 120000)},
    "hindu_temple": {"age": (18, 80), "income": (20000, 100000)},
    "home_goods_store": {"age": (25, 70), "income": (30000, 120000)},
    "hospital": {"age": (5, 80), "income": (40000, 200000)},
    "insurance_agency": {"age": (25, 70), "income": (50000, 200000)},
    "jewelry_store": {"age": (25, 70), "income": (50000, 200000)},
    "laundry": {"age": (18, 70), "income": (20000, 80000)},
    "lawyer": {"age": (25, 70), "income": (60000, 300000)},
    "library": {"age": (10, 70), "income": (20000, 100000)},
    "liquor_store": {"age": (21, 70), "income": (30000, 120000)},
    "lodging": {"age": (18, 70), "income": (30000, 200000)},
    "mosque": {"age": (18, 80), "income": (20000, 100000)},
    "movie_theater": {"age": (10, 70), "income": (20000, 100000)},
    "museum": {"age": (10, 70), "income": (20000, 150000)},
    "nightclub": {"age": (21, 40), "income": (30000, 90000)},
    "park": {"age": (3, 80), "income": (20000, 100000)},
    "pet_store": {"age": (18, 70), "income": (30000, 100000)},
    "pharmacy": {"age": (18, 80), "income": (30000, 100000)},
    "police": {"age": (18, 60), "income": (40000, 100000)},
    "restaurant": {"age": (18, 60), "income": (20000, 80000)},
    "school": {"age": (5, 18), "income": (30000, 100000)},
    "shopping_mall": {"age": (18, 70), "income": (30000, 150000)},
    "spa": {"age": (18, 70), "income": (30000, 150000)},
    "stadium": {"age": (10, 70), "income": (20000, 120000)},
    "store": {"age": (18, 70), "income": (20000, 120000)},
    "supermarket": {"age": (18, 70), "income": (30000, 90000)},
    "tourist_attraction": {"age": (3, 70), "income": (1000, 9999999999)},
    "train_station": {"age": (18, 70), "income": (20000, 90000)},
    "university": {"age": (18, 30), "income": (20000, 80000)},
    "veterinary_care": {"age": (18, 70), "income": (30000, 120000)},
    "zoo": {"age": (3, 70), "income": (20000, 100000)}
}


# def analyze_nearby_audience(address):
#     from store_target_audience import predict_target_age_income  # Lazy import to prevent circular dependency
#     address = address.replace(" ", "+")
#     lat, lng = get_lat_long(address)
#     if lat is None or lng is None:
#         print("Error: Unable to fetch latitude/longitude")
#         return
    
#     state_fips, county_fips = get_fips_codes(lat, lng)
#     if state_fips is None or county_fips is None:
#         print("Error: Unable to fetch local FIPS codes")
#         return
    
#     store_audience = predict_target_age_income(address, state_fips, county_fips)
#     local_audience = get_census_data(state_fips, county_fips)

#     if local_audience:
#         print(f"\n📍 **Store vs Nearby Audience for {address}**")
#         print(f"  - Store Target Age Range: {store_audience['age']}")
#         print(f"  - Nearby Median Age: {local_audience['median_age']} years")
#         print(f"  - Store Target Income Range: {store_audience['income']}")
#         print(f"  - Nearby Median Income: ${local_audience['median_income']}")

#         age_match = (
#             max(0, min(store_audience["age"][1], local_audience["median_age"]) - 
#                 max(store_audience["age"][0], local_audience["median_age"])) /
#             (store_audience["age"][1] - store_audience["age"][0]) if store_audience["age"] != "Unknown" else 0
#         )

#         income_match = (
#             max(0, min(store_audience["income"][1], local_audience["median_income"]) - 
#                 max(store_audience["income"][0], local_audience["median_income"])) /
#             (store_audience["income"][1] - store_audience["income"][0]) if store_audience["income"] != "Unknown" else 0
#         )

#         total_match_score = (age_match + income_match) / 2 * 100
#         print(f"  - **Match Score: {total_match_score:.2f}%**")


#------------------
#address = "Tin Drum Asian Kitchen & Boba Tea Bar, 88 5th St NW, Atlanta, GA 30308"
address = "Gyro Bros, 85 5th St NW B, Atlanta, GA 30332"

#Gets Latitude and Longitude
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

#Gets FIPS codes for census API
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

#Gets the business type
def get_business_type(address): 
    lat, lng = get_lat_long(address)
    if lat is None or lng is None:
        return None

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 5,  
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    # print((data["results"][0].get("types")))
    types = []
    if "results" in data and len(data["results"]) > 0:
        for place in data["results"]:
            #print((place["types"]))
            if "point_of_interest" not in place["types"]:
                continue
            business_types = place.get("types", [])
            types.append(business_types[0])

    return types

def generate_competitor_types(address):
    lat, lng = get_lat_long(address)
    if lat is None or lng is None:
        return None

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 100,  
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    types = []
    if "results" in data and len(data["results"]) > 0:
        for place in data["results"]:
            #print((place["types"]))
            if "point_of_interest" not in place["types"]:
                continue
            business_types = place.get("types", [])
            types.append(business_types[0])

    return types

def calculate_brand_score(store_type, competitor_types):
    all_comps = len(competitor_types)
    competitors = competitor_types.count(store_type)
    brand_score = ((all_comps - competitors) / all_comps) * 25
    return brand_score


#Gets nearest road from location
def get_road_location(lat, lng):
  offset_lng = lng + 0.0001  
  points = f"{lng},{lat};{offset_lng},{lat}"

  snap_url = f"https://api.tomtom.com/snapToRoads/1?key={API_KEY_SNAP}&points={points}"

  response = requests.get(snap_url)
  
  if (response.status_code == 200):
    data = response.json()
    if ("route" in data):
      print("Found Snapped Points")
      snapped_point = data["route"][0]["geometry"]["coordinates"][0]
      #print(snapped_point[1], snapped_point[0])
      return snapped_point[1], snapped_point[0]
    else:
      print("No snapped points found")
      return lat, lng
  else:
    print("Snap Bad Response " + str(response.status_code) + " " + response.text)
    return lat, lng


#Gets average traffic speed
def get_traffic_speed(lat, lng):
  traffic_url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={API_KEY_SNAP}&point={lat},{lng}&unit=mph"

  response = requests.get(traffic_url)
  if (response.status_code == 200):
    data = response.json()
    avg_speed = data["flowSegmentData"]["currentSpeed"]
    return avg_speed
  else:
    print("Traffic Data Error: " + str(response.status_code) + " " + response.text)
    return None

#Returns traffic score
def calculate_traffic_score(target_speed_range, average_speed, std_dev=5):
    target_mid = (target_speed_range[0] + target_speed_range[1]) / 2.0
    deviation = average_speed - target_mid
    abs_deviation = abs(deviation)

    if abs_deviation <= std_dev:
        return 30, deviation
    else:
        penalty = abs_deviation - std_dev
        score = 30 - penalty
        return max(0, score), deviation

#Gets Median Age in surrounding area
def get_census_age(state_fips, county_fips):
    url = "https://api.census.gov/data/2021/acs/acs5/profile"
    params = {
        "get": "DP05_0018E",  # Median Age
        "for": f"county:{county_fips}",
        "in": f"state:{state_fips}"
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1:
            return float(data[1][0])

    return None

#Returns Age Score
def calculate_age_match_score(target_age_range, nearby_median_age, std_dev=2):
    target_mid = (target_age_range[0] + target_age_range[1]) / 2.0
    deviation = nearby_median_age - target_mid
    abs_deviation = abs(deviation)
    
    if abs_deviation <= std_dev:
        return 30, deviation  # Maximum score
    else:
        penalty = abs_deviation - std_dev
        score = 30 - penalty
        return max(score, 0), deviation 

#Gets Median Income in surrounding area
def get_census_income(state_fips, county_fips):
    url = "https://api.census.gov/data/2021/acs/acs5/profile"
    params = {
        "get": "DP03_0062E",  # Median Household Income
        "for": f"county:{county_fips}",
        "in": f"state:{state_fips}"
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1:
            return int(float(data[1][1]))
             
    return None

#Returns income score
def calculate_income_match_score(target_income_range, nearby_median_income, std_dev=5000):
    
    target_mid = (target_income_range[0] + target_income_range[1]) / 2.0
    deviation = nearby_median_income - target_mid
    abs_deviation = abs(deviation)

    if abs_deviation <= 5000:
        return 15, deviation  # Maximum score
    else:
        penalty = int((abs_deviation - std_dev) / std_dev)
        score = 15 - penalty
        return max(score, 0), deviation  # Ensure the score is not negative
    
def calculate_final_score(address):
    lat, lng = get_lat_long(address)
    print(lat, lng)

    state_fips, county_fips = get_fips_codes(lat, lng)
    print(state_fips, county_fips)

    business_type = get_business_type(address)[0]
    competitor_types = generate_competitor_types(address)
    print("Business: " + business_type)

    median_age = get_census_age(state_fips, county_fips)
    target_age_range = BUSINESS_AGE_INCOME_MAPPING.get(business_type)["age"]
    age_score, age_deviation = calculate_age_match_score(target_age_range, median_age)
    
    median_income = get_census_income(state_fips, county_fips)
    target_income_range = BUSINESS_AGE_INCOME_MAPPING.get(business_type)["income"]
    income_score, income_deviation = calculate_income_match_score(target_income_range, median_income)

    road_lat, road_lng = get_road_location(lat, lng)
    average_speed = get_traffic_speed(road_lat, road_lng)
    traffic_range = (0, 60)
    traffic_score, traffic_deviation = calculate_traffic_score(traffic_range, average_speed)

    brand_score = calculate_brand_score(business_type, competitor_types)

    # print("Age Score: " + str(age_score))
    # print("Income Score: " + str(income_score))
    # print("Brand Score: " + str(brand_score))
    # print("Traffic Score: " + str(traffic_score) + "\n")

    total_score = age_score + income_score + traffic_score + brand_score

    print("Total Score: " + str(total_score) + "/100")

    arr_of_scores = [age_score, income_score, brand_score, traffic_score]
    score_names = ['Age Score', 'Income Score', 'Brand Score', 'Traffic Score']

    # Pairing each score with its name
    paired_scores = list(zip(score_names, arr_of_scores))

    # Sort by numerical value (lowest score has highest priority)
    sorted_scores = sorted(paired_scores, key=lambda x: x[1])

    # Determine improvement message based on lowest score
    lowest_score_name = sorted_scores[0][0]

    improvement_message = ""

    if lowest_score_name == 'Age Score':
        if age_deviation >= 0:
            improvement_message = "Your nearby age audience is too high! Make your target audience higher age"
        else:
            improvement_message = "Your nearby age audience is too low! Make your target audience lower age"

    elif lowest_score_name == 'Income Score':
        if income_deviation >= 0:
            improvement_message = "Your nearby audience makes too much money! They probably won't like your products... Make your products higher quality!"
        else:
            improvement_message = "Your nearby audience doesn't make that much money... Try to make your prices lower!"

    elif lowest_score_name == 'Traffic Score':
        if traffic_deviation >= 0:
            improvement_message = "The people passing by your shop are driving by too fast so they can't see your store!"
        else:
            improvement_message = "Error"

    elif lowest_score_name == 'Brand Score':
        if brand_score <= 12.5:
            improvement_message = "There are too many similar shops to your store! Try to either make your products stand out or go into a different industry"
        else:
            improvement_message = "Error"

    return total_score, improvement_message
