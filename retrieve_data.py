import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase app
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)  # Replace with your database URL

db = firestore.client()
collection_ref = db.collection("sos_generation")

# Get all documents from the collection
docs = collection_ref.stream()

# Create a list to store retrieved data
data_list = []

# Iterate through documents and add data to the list
for doc in docs:
    data = doc.to_dict()

    # Convert GeoPoint to dictionary
    if 'geolocation' in data and isinstance(data['geolocation'], firestore.GeoPoint):
        data['position'] = {
            'latitude': data['geolocation'].latitude,
            'longitude': data['geolocation'].longitude
        }
        del data['geolocation']

    data_list.append(data)

# Save the retrieved data to a JSON file
with open("user_data_with_geolocation.json", "w") as json_file:
    json.dump(data_list, json_file, indent=4, default=str)

print("Data retrieved and saved to user_data_with_geolocation.json")
