import folium
from matplotlib.colors import Colormap
from numpy import True_
import pandas

data = pandas.read_csv('Volcanoes.txt')
lat = list(data['LAT'])
lon = list(data['LON'])
name = list(data['NAME'])
elev = list(data['ELEV'])
stat = list(data['STATUS'])
type = list(data['TYPE'])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif elevation <3000:
        return 'orange'
    else:
        return 'red'

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
<div style="white-space: pre">
Height: %s m 
Status: %s  
Type: %s 
</div>
"""

map = folium.Map(location=[40.61,-109.81],zoom_start=5, titles="Stamen Terrain")

fg = folium.FeatureGroup(name='My Map')

for lt,ln,name,el,stat,type in zip(lat,lon,name,elev,stat,type):
    iframe = folium.IFrame(html=html % (name, name, el, stat,type), width=200, height=100)
    fg.add_child(folium.CircleMarker(location=[lt,ln],radius=6, 
        fill_color=color_producer(el),color='grey',fill=True,fill_opacity=0.7).add_child(folium.Popup(iframe)))

map.add_child(fg)
map.save("Map1.html")



