import pandas as pd
import spacy
from tqdm import tqdm
import folium
from folium.plugins import HeatMap
import geonamescache
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import json
import os

nlp = spacy.load("en_core_web_sm")

gc = geonamescache.GeonamesCache()
valid_cities = set(city["name"].lower() for city in gc.get_cities().values())
valid_countries = set(country["name"].lower() for country in gc.get_countries().values())

df = pd.read_csv("risk_classified_reddit_posts.csv")

def extract_location(text):
    if pd.isna(text):
        return None
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            name = ent.text.strip().lower()
            if name in valid_cities or name in valid_countries:
                return ent.text
    return None

tqdm.pandas()
df["location_mentioned"] = df["cleaned_content"].progress_apply(extract_location)

geolocator = Nominatim(user_agent="RedditCrisisMapper (contact@example.com)")

def get_coordinates(place):
    try:
        if pd.isna(place):
            return [None, None]
        time.sleep(1.1) 
        location = geolocator.geocode(place, timeout=10)
        if location:
            return [location.latitude, location.longitude]
    except GeocoderTimedOut:
        time.sleep(2)
        return get_coordinates(place)
    except Exception as e:
        print(f"Error fetching {place}: {e}")
    return [None, None]

cache_file = "geocache.json"
if os.path.exists(cache_file):
    with open(cache_file, "r") as f:
        location_coords = json.load(f)
else:
    location_coords = {}

unique_locations = df["location_mentioned"].dropna().unique()
for loc in tqdm(unique_locations, desc="Geocoding"):
    if loc not in location_coords:
        location_coords[loc] = get_coordinates(loc)

with open(cache_file, "w") as f:
    json.dump(location_coords, f)

df[["lat", "lon"]] = df["location_mentioned"].apply(
    lambda loc: pd.Series(location_coords.get(loc, [None, None]))
)

df_geo = df.dropna(subset=["lat", "lon"])

m = folium.Map(location=[20, 0], zoom_start=2)
heat_data = df_geo[["lat", "lon"]].values.tolist()
HeatMap(heat_data).add_to(m)
m.save("crisis_heatmap.html")

top_locations = df["location_mentioned"].value_counts().head(5)
print("\n🔝 Top 5 Locations with Highest Crisis Mentions:")
print(top_locations)

df.to_csv("crisis_geolocation_results_validated.csv", index=False)