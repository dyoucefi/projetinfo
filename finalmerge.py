#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 13:22:58 2020

@author: dalilyoucefi
"""

import geopandas as gpd
import pandas as pd

gdf_quart1= gpd.read_file("/Users/dalilyoucefi/Desktop/BaseQuartier.shp")[["c_qu","l_qu","c_ar","l_ar",'prop_30-44', 'prop_45-59', 'prop_60-74',
       'prop_75+', 'nombre_0-1', 'nombre_15-', 'nombre_30-', 'nombre_45-',
       'nombre_60-', 'nombre_75+', 'pop', 'densite', 'nombretran']]
gdf_quart2= gpd.read_file("/Users/dalilyoucefi/Downloads/bdd_quart.csv")
gdf_ent=gpd.read_file("/Users/dalilyoucefi/Desktop/entreprisefinal.csv")
gdf_Tier=gpd.read_file("/Users/dalilyoucefi/Desktop/TierMetroLu.shp").dropna()
gdf_quart1["c_qu"]=gdf_quart1["c_qu"].astype(str)
gdf_Tier["id_quartie"]=gdf_Tier["id_quartie"].astype(int)
gdf_Tier["id_quartie"]=gdf_Tier["id_quartie"].astype(str)
gdf_ent["id_quartier"]=gdf_ent["id_quartier"].astype(float)
gdf_ent["id_quartier"]=gdf_ent["id_quartier"].astype(int)
gdf_ent["id_quartier"]=gdf_ent["id_quartier"].astype(str)
gdf2=gdf_quart1.merge(gdf_quart2, left_on="c_qu",right_on="numquartier")
gdf2=gdf2[['c_qu', 'l_qu', 'c_ar', 'l_ar', 'prop_30-44', 'prop_45-59',
       'prop_60-74', 'prop_75+', 'nombre_0-1', 'nombre_15-', 'nombre_30-',
       'nombre_45-', 'nombre_60-', 'nombre_75+', 'pop', 'densite',
       'nombretran', 'field_1', 'numquartier', 'ref', 'nb_logmt_total',
       'nombre_de_commerce']]
gdf_ent=gdf_ent[["id_quartier","nombreent","CA 1"]]
gdf3=gdf2.merge(gdf_ent, left_on="c_qu",right_on="id_quartier")

gdf_Tierfin=gdf_Tier.merge(gdf3, left_on="id_quartie",right_on="c_qu")
gdf_Tierfin=gdf_Tierfin[['Unnamed_ 0', 'ID', 'BatteryLev', 'Lat', 'Lng', 'Type', 'Status',
       'Heure', 'Jour', 'Arrondisse', 'densité', 'nomquartie', 'id_quartie', 'station_mi', 'min_distan', 'ligne_min', 'mode_min',
       'geometry', 'c_qu', 'l_qu', 'c_ar', 'l_ar', 'prop_30-44', 'prop_45-59',
       'prop_60-74', 'prop_75+', 'nombre_0-1', 'nombre_15-', 'nombre_30-',
       'nombre_45-', 'nombre_60-', 'nombre_75+', 'pop', 'densite',
       'nombretran', 'field_1', 'numquartier', 'ref', 'nb_logmt_total',
       'nombre_de_commerce']]

gdf_Tier.to_file("/Users/dalilyoucefi/Desktop/Tierbasefin1geo.geojson", driver='GeoJSON')

gdf_Tier['nombrtrot']=1
trot=gdf_Tier.groupby('id_quartie',as_index=False).sum()
trot=trot[["id_quartie","nombrtrot"]]
gdf4=gdf3.merge(trot, left_on="c_qu",right_on="id_quartie")
gdf4.to_csv("/Users/dalilyoucefi/Desktop/Base2Quartier.csv")