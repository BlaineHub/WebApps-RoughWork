
from importlib.metadata import distribution
from cv2 import DFT_COMPLEX_OUTPUT
import pandas
from math import cos, sin, sqrt, atan2
import folium
from geopy.geocoders import Nominatim


df = pandas.read_csv('takeaways.txt')
name = list(df['ADDRESS'])
rating = list(df['STARS'])
price = list(df['PRICE'])


lat = []
lon = []
for x in name:
  geolocator = Nominatim(user_agent="MyApp")
  location = geolocator.geocode(x)
  lat.append(location.latitude)
  lon.append(location.longitude)

df['LAT'] = lat
df['LON'] = lon

