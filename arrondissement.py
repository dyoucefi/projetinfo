#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:32:15 2020

@author: dalilyoucefi
"""


import geopandas as gpd
import pandas as pd

gdf = gpd.read_file('/Users/dalilyoucefi/Downloads/arrondissements.geojson').sort_values(by="c_ar").reset_index()
gdf2=gpd.read_file('/Users/dalilyoucefi/Downloads/quartier_paris.geojson')


gdf.head()


df_Tier=pd.read_csv("/Users/dalilyoucefi/Desktop/TierBase9HSa.csv")


import geopandas



clc = geopandas.GeoDataFrame(df_Tier, geometry=geopandas.points_from_xy(clc.Lng, clc.Lat))

gdf_Tier["geometry"][0].within(gdf["geometry"][19])
gdf_Tier["Arrondissement"]= 0
gdf_Tier["densité"]=0
gdf_Tier["nomquartier"]=0
gdf_Tier["id_quartier"]=0

def arrondissementappartenance(point):
    for i in range(20):
        if point.within(gdf["geometry"][i]):
            return int(i+1)


def quartierappartenance2(point):
    for i in range(80):
        if point.within(gdf2["geometry"][i]):
            return gdf2["c_qu"][i]
clc["Arrondissement"]= clc["geometry"].apply(arrondissementappartenance)


clc["id_quartier"]=clc["geometry"].apply(quartierappartenance2)


 
