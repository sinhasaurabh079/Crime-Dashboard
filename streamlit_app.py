import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime

# Load JSON data with location data
with open("user_data_with_location.json", "r") as json_file:
    data = json.load(json_file)

# Create a pandas DataFrame for easier manipulation
df = pd.DataFrame(data)

# Extract the location information from the nested "position" dictionary
df["location"] = df["position"].apply(lambda x: x["location"])

# Extract date from the "time" field and create a new column "date"
df["date"] = df["time"].apply(
    lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f%z").date()
)

# Group data by location and calculate crime counts
location_counts = df["location"].value_counts().reset_index()
location_counts.columns = ["location", "crime_count"]

# Group data by date and calculate crime counts
datewise_counts = df["date"].value_counts().reset_index()
datewise_counts.columns = ["date", "crime_count"]

# Group data by crime type and calculate crime counts
crime_type_counts = df["crime_type"].value_counts().reset_index()
crime_type_counts.columns = ["crime_type", "crime_count"]

# Create the Streamlit App
st.title("Crime Dashboard")

# Display a filter for selecting location
locations = location_counts["location"]
selected_location = st.selectbox("Select Location", locations)

# Filter data based on selected location
filtered_count = location_counts[location_counts["location"] == selected_location][
    "crime_count"
].values[0]

# Display the selected location and its crime count
st.write(f"Crime Count in {selected_location}: {filtered_count}")

# Create a Plotly bar chart for location-wise crime counts
fig_location = px.bar(
    location_counts,
    x="location",
    y="crime_count",
    title="Crime Count by Location",
    labels={"location": "Location", "crime_count": "Crime Count"},
)

# Display the chart using Streamlit
st.plotly_chart(fig_location)

# Display a filter for selecting date
dates = datewise_counts["date"]
selected_date = st.selectbox("Select Date", dates)

# Filter data based on selected date
filtered_date_count = datewise_counts[datewise_counts["date"] == selected_date][
    "crime_count"
].values[0]

# Display the selected date and its crime count
st.write(f"Crime Count on {selected_date}: {filtered_date_count}")

# Create a Plotly line chart for date-wise crime counts
fig_date = px.line(
    datewise_counts,
    x="date",
    y="crime_count",
    title="Crime Count by Date",
    labels={"date": "Date", "crime_count": "Crime Count"},
)

# Display the chart using Streamlit
st.plotly_chart(fig_date)

# Display a filter for selecting crime type
crime_types = crime_type_counts["crime_type"]
selected_crime_type = st.selectbox("Select Crime Type", crime_types)

# Filter data based on selected crime type
filtered_crime_type_count = crime_type_counts[
    crime_type_counts["crime_type"] == selected_crime_type
]["crime_count"].values[0]

# Display the selected crime type and its count
st.write(f"Crime Count for {selected_crime_type}: {filtered_crime_type_count}")

# Create a Plotly pie chart for crime type distribution
fig_crime_type = px.pie(
    crime_type_counts,
    names="crime_type",
    values="crime_count",
    title="Crime Type Distribution",
)

# Display the chart using Streamlit
st.plotly_chart(fig_crime_type)

# Print the DataFrame to the terminal
print(df)
