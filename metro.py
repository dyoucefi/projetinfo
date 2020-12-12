#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 08:55:18 2020

@author: dalilyoucefi
"""


#Installation des items 

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
import tempfile
import zipfile
import json
import matplotlib.pyplot as plt
import math

#Représentation des points dans la carte à partir de folium  
#!pip install folium 
import folium

url = 'https://www.data.gouv.fr/fr/datasets/r/07b7c9a2-d1e2-4da6-9f20-01a7b72d4b12'
temporary_location = tempfile.gettempdir()

def download_unzip(url, dirname = tempfile.gettempdir(), destname = "borders"):
    myfile = requests.get(url)
    open(dirname + '/' + destname + '.zip', 'wb').write(myfile.content)
    with zipfile.ZipFile(dirname + '/' + destname + '.zip', 'r') as zip_ref:
        zip_ref.extractall(dirname + '/' + destname)
        
download_unzip(url)
communes = gpd.read_file(temporary_location + "/borders/communes-20190101.json")
communes.head()

paris = communes[communes.insee.str.startswith("75")]
ax = paris.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
#ctx.add_basemap(ax, crs = paris.crs.to_string())
ax


#ajout des arrondissement
arrondissements = gpd.read_file("https://opendata.paris.fr/explore/dataset/arrondissements/download/?format=geojson&timezone=Europe/Berlin&lang=fr")
print(arrondissements)
arrondissements.dtypes

arrondissements = arrondissements.rename(columns = {"c_arinsee": "insee"})
arrondissements['insee'] = arrondissements['insee'].astype(str)
communes = communes[~communes.insee.str.startswith("75")].append(arrondissements)

paris = communes[communes.insee.str.startswith("75")]
ax = paris.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
ax


stations = open("/Users/dalilyoucefi/Downloads/emplacement-des-gares-idf.geojson", "r")
stations_2 = gpd.read_file(stations)
stations_2

stations= stations_2[["gares_id","nomlong","mode","ligne","geometry"]]

#Ajout base de donnée des trotinnettes 

df = pd.read_csv("/Users/dalilyoucefi/Desktop/TierBase9HLu.csv")
df



#Affichage de la carte sous module folium

coords = (46.539758, 2.430331)
map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
map

for i in range(len(df)):
    folium.CircleMarker(
        location = (df['Lat'][i], df['Lng'][i]),
        color = 'crimson',
        fill = True,
        fill_color = 'crimson'
    ).add_to(map)

sf = lambda x :{'fillColor':'#E88300', 'fillOpacity':0.5, 'color':'#E84000', 'weight':1, 'opacity':1}
folium.GeoJson(
    data=arrondissements,
    name="idf",
    style_function= sf
).add_to(map)
map



# Représentation des trotinettes avec geopandas
import descartes
from shapely.geometry import Point, polygon
df['geometry'] = [Point(xy) for xy in zip(df['Lat'], df['Lng'])]
#crs= {'init' : 'epsg : 4326'}

df['geometry'] = gpd.GeoDataFrame(df['geometry'], geometry = gpd.points_from_xy(df['Lat'], df['Lng']))
                                      
df.dtypes
df1 = gpd.read_file("/Users/dalilyoucefi/Desktop/GeoTierLu.shp")
df1

df1["x"]=df1["geometry"].x
df1["y"]=df1["geometry"].y
stations["x"]=stations["geometry"].x
stations["y"]=stations["geometry"].y


def distance(x1,y1,x2,y2):
    R = 6373.0
    
    
    lat1 = math.radians(y1)

    lon1 = math.radians(x1)
    lat2 = math.radians(y2)
    lon2 = math.radians(x2)
    
    dlon = lon2 - lon1
    
    dlat = lat2 - lat1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return (distance)

min_distancei = float(1000000)
min_distance = []
station_min = []
ligne_min=[]
modemin=[]
for i in range(len(df1)):
    min_distancei = float(100000)
    station_min0 = "Essai"
    ligne_min0="Essai"
    mode_min0="Essai"
    for j in range(len(stations)):
        
        if distance(df1["x"][i],df1["y"][i],stations["x"][j],stations["y"][j]) <= min_distancei :
                min_distancei = distance(df1["x"][i],df1["y"][i],stations["x"][j],stations["y"][j])
                station_min0 = stations['nomlong'][j]
                ligne_min0=stations["ligne"][j]
                ligne_min0=stations["mode"][j]
           

    min_distance.append(min_distancei)
    station_min.append(station_min0)
    ligne_min.append(ligne_min0)
    modemin.append(mode_min0)



        




df1["station_min"] = station_min
df1["min_distance"] = min_distance
df1["ligne_min"]=ligne_min
df1["mode_min"]=modemin


df1.to_file("/Users/dalilyoucefi/Desktop/TierMetroLu.shp")