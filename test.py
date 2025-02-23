import requests
import math

API_KEY_SATELLITE = "AIzaSyCh0iR9Y1LdzZijx91xWFmJUNBRDVnMI_0"
API_KEY_P_S = "AIzaSyBLoahDSc9lMcf7EHIMrV1k60cvICw3EYc"
API_KEY_SNAP = "O08DVAiFeIJWNEknkZSxk7Jel3W1dH23"

#Satellite Image Generator
def generate_satellite_image(address):
  satellite_url = f"https://maps.googleapis.com/maps/api/staticmap?center={address.replace(' ', '+')}&zoom=19&size=600x600&maptype=satellite&key={API_KEY_SATELLITE}"
  response = requests.get(satellite_url)

  if (response.status_code == 200):
    with open("satellite_image.png", "wb") as file:
      file.write(response.content)
      print("File successfully saved")
  else:
    print("ERROR: " + response.status_code)

#Get Place ID
def get_place_id(address):
  place_id_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={address.replace(' ', '+')}&inputtype=textquery&fields=place_id&key={API_KEY_P_S}"
  response = requests.get(place_id_url)
  data = response.json()

  if (data.get("candidates")):
    return data["candidates"][0]["place_id"]
  else:
    print("No place ID found")
    return None

#Get Place Latitude and Longitude
def get_place_location(place_id):
  place_location_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,geometry,formatted_address,url&key={API_KEY_P_S}"
  response = requests.get(place_location_url)
  data = response.json()

  if ("result" in data):
    details = data["result"]
    #print(details)
    location = details["geometry"]["location"]
    lat, lng = location["lat"], location["lng"]
    print(f"Coordinates Found: ({lat}, {lng})")
    return lat, lng
  else:
    print("No details found")
    return None

#Snap location to nearest road
def snap_to_road(lat, lng):
  offset_lng = lng + 0.0001  
  points = f"{lng},{lat};{offset_lng},{lat}"

  snap_url = f"https://api.tomtom.com/snapToRoads/1?key={API_KEY_SNAP}&points={points}"

  response = requests.get(snap_url)
  
  if (response.status_code == 200):
    data = response.json()
    if ("route" in data):
      print("Found Snapped Points")
      snapped_point = data["route"][0]["geometry"]["coordinates"][0]
      print(snapped_point[1], snapped_point[0])
      return snapped_point[1], snapped_point[0]
    else:
      print("No snapped points found")
      return lat, lng
  else:
    print("Snap Bad Response " + str(response.status_code) + " " + response.text)
    return lat, lng

#Calculate direction of camera
def calculate_bearing(lati1, long1, lati2, long2):
  lat1, lon1, lat2, lon2 = map(math.radians, [lati1, long1, lati2, long2])

  delta_lon = lon2 - lon1
  x = math.sin(delta_lon) * math.cos(lat2)
  y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon))
  bearing = math.atan2(x, y)
  
  return (math.degrees(bearing + 180) + 360) % 360

def get_traffic_data(lat, lng):
  traffic_url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={API_KEY_SNAP}&point={lat},{lng}&unit=mph"

  response = requests.get(traffic_url)
  if (response.status_code == 200):
    data = response.json()
    avg_speed = data["flowSegmentData"]["currentSpeed"]
    avg_time = data["flowSegmentData"]["currentTravelTime"]
    return avg_speed, avg_time
  else:
    print("Traffic Data Error: " + str(response.status_code) + " " + response.text)
    return None


#Generate Street View Image
def generate_street_image(lat, lng, slat, slon):
  heading = calculate_bearing(lat, lng, slat, slon)

  street_view_url = f"https://maps.googleapis.com/maps/api/streetview?size=600x300&location={slat},{slon}&fov=180&heading={heading - 90}&pitch=0&key={API_KEY_P_S}"
  
  response = requests.get(street_view_url)

  if (response.status_code == 200):
    with open("street_view_img.jpg", "wb") as file:
      file.write(response.content)
      print("File Successfully saved")
  else:
    print("Error Loading Image")

#Complete all three functions in succession
def get_storefront_img(address):
  place_id = get_place_id(address)
  if (not place_id):
    return

  lat, lng = get_place_location(place_id)
  if (lat is None or lng is None):
    return

  snapped_lat, snapped_lng = snap_to_road(lat, lng)

  avg_speed, avg_time_taken = get_traffic_data(snapped_lat, snapped_lng)

  print("Average Speed: " + str(avg_speed) + "mph")
  print("Average Time: " + str(avg_time_taken) + "s")

  generate_street_image(lat, lng, snapped_lat, snapped_lng)

#get_storefront_img("88 5th St NW, Atlanta, GA 30308")




  




