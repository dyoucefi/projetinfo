#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:32:15 2020

@author: dalilyoucefi
"""


import geopandas as gpd
import pandas as pd

gdf = gpd.read_file('/Users/dalilyoucefi/Downloads/arrondissements.geojson')
gdf2=gpd.read_file('/Users/dalilyoucefi/Downloads/quartier_paris.geojson')


gdf.head()


df_Tier=pd.read_csv("/Users/dalilyoucefi/Desktop/TierBase9HLu.csv")

import geopandas



gdf_Tier = geopandas.GeoDataFrame(df_Tier, geometry=geopandas.points_from_xy(df_Tier.Lng, df_Tier.Lat))

gdf_Tier["geometry"][0].within(gdf["geometry"][19])
gdf_Tier["Arrondissement"]= 0
gdf_Tier["densité"]=0
gdf_Tier["quartier"]=0

def arrondissementappartenance(point):
    for i in range(20):
        if point.within(gdf["geometry"][i]):
            return int(i+1)
def densitearr(point):
    li=[9863,21872,29638,17838,24817,21062,13936,10147,26888,323888,41341,8686,24896,23684,27201,9714,29166,31701,27274,32494]
    for i in range(20):
        if point.within(gdf["geometry"][i]):
            return(li[i])
def quartierappartenance(point):
    for i in range(80):
        if point.within(gdf2["geometry"][i]):
            return gdf2["l_qu"][i]
gdf_Tier["Arrondissement"]= gdf_Tier["geometry"].apply(arrondissementappartenance)
gdf_Tier["densité"]=gdf_Tier["geometry"].apply(densitearr)
gdf_Tier["quartier"]=gdf_Tier["geometry"].apply(quartierappartenance)

gdf_Tier.to_file("/Users/dalilyoucefi/Desktop/GeoTier9HLu.shp")
