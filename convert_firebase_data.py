import json
import geohash2

# Load the original JSON data
with open("user_data_with_geolocation.json", "r") as json_file:
    data_list = json.load(json_file)

# Update each item in the data_list with latitude and longitude
for item in data_list:
    geohash = item["position"]["geohash"]
    latitude, longitude = geohash2.decode(geohash)
    
    item["position"]["latitude"] = latitude
    item["position"]["longitude"] = longitude

# Save the updated data to a new JSON file
with open("user_data_with_correct_geolocation.json", "w") as json_file:
    json.dump(data_list, json_file, indent=4)

print("Updated data saved to user_data_with_correct_geolocation.json")
