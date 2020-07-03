#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# ----
# 
# ### Analysis
# * Of the cities tested, cities positioned at 0 degrees latitude experienced a smaller range of humidity than other cities, with a humidity no lower than 45%.
# 
# * Far more cities experienced 0% cloudiness as opposed to 100% cloudiness, outnumbering the latter by the dozens.
# 
# * Wind speeds cluster between 0 and 10 mph, regardless of location.

# In[2]:


# Native library
import requests
import time
import json

# Third party
import numpy as np
import pandas as pd
from citipy import citipy
from ratelimit import limits
import matplotlib.pyplot as plt

# Custom
import api_keys # Uses the openweathermap.org API


# In[3]:


# Output File (CSV)
output_data_file = "Resources/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# ## Generate Cities List

# In[4]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

# In[5]:


# Components of api endpoint(s)
url = "http://api.openweathermap.org/data/2.5/weather?"
unit = "units=Imperial"
api = "&APPID=" + api_keys.api_key

# Creates variable for response code then prints response code to the console
response = requests.get(url + unit + api).json()
print(response)

# Creates dictionary for data to be stored from the api calls
city_data = {"City": [],
              "Lat": [],
              "Lng": [],
              "Max Temp": [],
              "Humidity": [],
              "Cloudiness": [],
              "Wind Speed": [],
              "Country": [],
              "Date": []}

MINUTE = 60

# Decorator that limits "call_api" function to 60 api calls per minute
@limits(calls=60, period=MINUTE)
def call_api():
    
    # A loop that repeats an api call with dynamic endpoints then adds data retrieved from each api call into "city_data" dictionary
    for i, city in enumerate(cities):
        city = requests.get(url + unit + "&q=" + cities[i] + api).json()

        try:
            print("Processing city " + str(i) + ": " + city["name"])

            city_data["City"].append(city["name"])
            city_data["Lat"].append(city["coord"]["lat"])
            city_data["Lng"].append(city["coord"]["lon"])
            city_data["Max Temp"].append(city["main"]["temp_max"])
            city_data["Humidity"].append(city["main"]["humidity"])
            city_data["Cloudiness"].append(city["clouds"]["all"])
            city_data["Wind Speed"].append(city["wind"]["speed"])
            city_data["Country"].append(city["sys"]["country"])
            city_data["Date"].append(city["dt"])

        except:
            print("Incomplete record. Skipping city instance...")
            pass
    print("Data retrieval is complete.")
    
call_api()


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[6]:


# Creates table/DataFrame from the "city_data" dictionary
city_data_df = pd.DataFrame(city_data)

# Exports DataFrame as a csv file
city_data_df.to_csv(output_data_file, index_label="City_ID")

# Previews table/DataFrame
city_data_df


# In[7]:


# Creates variables for relevant table columns
lat = city_data_df["Lat"]
max_temp = city_data_df["Max Temp"]
humidity = city_data_df["Humidity"]
cloudiness = city_data_df["Cloudiness"]
wind_speed = city_data_df["Wind Speed"]


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[8]:


# Establishes size for the next visualization/graph
plt.figure(figsize=(10,8))

# Establishes type, data, and configuration for visualization/graph
plt.scatter(lat, max_temp, linewidths=1, marker="o")

# Creates labels and grid for graph
plt.title("City Latitude vs. Max Temperature (%s)" % time.strftime("%x"))
plt.xlabel("Latitude")
plt.ylabel("Max Temperature (F)")
plt.grid(True)

# Exports graph as a png image file (steps are repeated for the rest of the script...)
plt.savefig("Images/Fig1.png")


# #### Latitude vs. Humidity Plot

# In[9]:


plt.figure(figsize=(10,8))

plt.scatter(lat, humidity, linewidths=1, marker="o")

plt.title("City Latitude vs. Humidity (%s)" % time.strftime("%x"))
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")
plt.grid(True)

plt.savefig("Images/Fig2.png")


# #### Latitude vs. Cloudiness Plot

# In[10]:


plt.figure(figsize=(10,8))

plt.scatter(lat, cloudiness, linewidths=1, marker="o")

plt.title("City Latitude vs. Cloudiness (%s)" % time.strftime("%x"))
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.grid(True)

plt.savefig("Images/Fig3.png")


# #### Latitude vs. Wind Speed Plot

# In[11]:


plt.figure(figsize=(10,8))

plt.scatter(lat, wind_speed, linewidths=1, marker="o")

plt.title("City Latitude vs. Wind Speed (%s)" % time.strftime("%x"))
plt.xlabel("Latitude")
plt.ylabel("Wind Speed (mph)")
plt.grid(True)

plt.savefig("Images/Fig4.png")

