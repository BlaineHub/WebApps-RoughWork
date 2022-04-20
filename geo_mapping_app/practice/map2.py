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


map = folium.Map(location=[40.61,-109.81],zoom_start=5, titles="Stamen Terrain")

fgv = folium.FeatureGroup(name='Volcanoes')

for lt,ln,name,el,stat,type in zip(lat,lon,name,elev,stat,type):
    fgv.add_child(folium.CircleMarker(location=[lt,ln],radius=6, popup=str(el)+'m',
        fill_color=color_producer(el),color='grey',fill=True,fill_opacity=0.7))

fgp = folium.FeatureGroup(name='Population')
fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 25000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map2.html")