import json
from geopy.geocoders import Nominatim

# Load the JSON data with correct geolocation
with open("user_data_with_correct_geolocation.json", "r") as json_file:
    data_list = json.load(json_file)

# Initialize the geolocator
geolocator = Nominatim(user_agent="geolocation_converter")

# Update each item in the data_list with location name
for item in data_list:
    latitude = item["position"]["latitude"]
    longitude = item["position"]["longitude"]
    
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    
    if location:
        item["position"]["location"] = location.address
    else:
        item["position"]["location"] = "Location not found"

# Save the updated data to a new JSON file
with open("user_data_with_location.json", "w") as json_file:
    json.dump(data_list, json_file, indent=4)

print("Updated data with location saved to user_data_with_location.json")
