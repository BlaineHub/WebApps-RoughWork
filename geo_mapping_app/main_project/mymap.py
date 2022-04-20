from importlib.metadata import distribution
from cv2 import DFT_COMPLEX_OUTPUT
import pandas
from math import cos, sin, sqrt, atan2
import folium
from geopy.geocoders import Nominatim


df = pandas.read_csv('takeaways.txt')
address = list(df['ADDRESS'])
name = list(df['NAME'])
rating = list(df['STARS'])
price = list(df['PRICE'])


#function calculate lat/lon from the address
lat = []
lon = []
for x in address:
  geolocator = Nominatim(user_agent="MyApp")
  location = geolocator.geocode(x)
  lat.append(location.latitude)
  lon.append(location.longitude)

df['LAT'] = lat
df['LON'] = lon

#function calculate distance to my home
dist = []
def distance():
    for x,y in zip(lat,lon):
        dlon = -6.3747-y
        dlat = 53.3232-x
        a = (sin(dlat/2))**2 + cos(53.3232) * cos(x) * (sin(dlon/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        d = 6373 * c
        dist.append(int(d))
distance()
df['distance'] = dist


#function to color based on rating
def color_rating(rating):
    if rating < 3:
        return 'red'
    elif rating <=4:
        return 'orange'
    else:
        return 'green'

#html style for the labels
html = """
Takeaway Name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
<div style="white-space: pre">
Rating: %s Stars 
Meal Price: €%s 
Distance From Me: %s m
</div>
"""

#creating map and feature/labels
map = folium.Map(location=[53.3232,-6.3747],zoom_start=11, titles="Stamen Terrain")
fg = folium.FeatureGroup(name='My Map')

for lat,lon,name,rating,price,dist in zip(lat,lon,name,rating,price,dist):
    iframe = folium.IFrame(html=html % (name, name, rating, price,dist), width=200, height=120)
    fg.add_child(folium.CircleMarker(location=[lat,lon],radius=6, 
        fill_color=color_rating(rating),color='grey',fill=True,fill_opacity=0.7).add_child(folium.Popup(iframe)))

map.add_child(fg)
map.save("MyMap.html")



