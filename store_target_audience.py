import requests
from pprint import pprint

GOOGLE_API_KEY = "AIzaSyDhVgRxfBbURvJSiMpUPrGzi5qzHLGrN4Q"

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

def get_business_type(address):
    """
    Retrieves business type using Google Places API.
    """
    from nearby_audience import get_lat_long  # Lazy import to prevent circular dependency
    
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
            print((place["types"]))
            if "point_of_interest" not in place["types"]:
                continue
            business_types = place.get("types", [])
            types.append(business_types[0])

    print(types)
    return types



def get_median_income(state_fips, county_fips):
    url = "https://api.census.gov/data/2021/acs/acs5/profile"
    params = {
        "get": "DP03_0062E",
        "for": f"county:{county_fips}",
        "in": f"state:{state_fips}"
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1:
            return int(data[1][0])
    return None

def predict_target_age_income(address, state_fips, county_fips):
    business_types = get_business_type(address)
    local_income = get_median_income(state_fips, county_fips)
    # print(local_income)
    
    if business_types:
        for t in business_types:
            if t not in BUSINESS_AGE_INCOME_MAPPING:
                continue
            
            base_data = BUSINESS_AGE_INCOME_MAPPING[t]
            print(f"{base_data=}")
            if local_income:
                adjusted_income = (
                    max(base_data["income"][0], local_income * 0.8),
                    min(base_data["income"][1], local_income * 1.2)
                )
            return {"age": base_data["age"], "income": adjusted_income}
            
    return {"age": "Unknown", "income": "Unknown"}
