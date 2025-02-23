import requests

API_KEY = "AIzaSyCh0iR9Y1LdzZijx91xWFmJUNBRDVnMI_0"
#address = '1600 Amphitheatre Parkway, Mountain View, CA'
address = '266 Ferst Dr NW, Atlanta, GA'
url = f"https://maps.googleapis.com/maps/api/staticmap?center={address.replace(' ', '+')}&zoom=20&size=600x600&maptype=satellite&key={API_KEY}"

response = requests.get(url)

if (response.status_code == 200):
  with open("satellite_image.png", "wb") as file:
    file.write(response.content)
    print("File successfully saved")
else:
  print("ERROR: " + response.status_code)