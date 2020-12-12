#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 15:54:21 2020

@author: dalilyoucefi
"""

import urllib
import bs4
import pandas as pd
from urllib import request
import geopandas as gpd
import numpy as np
liste_ageprop=[]
liste_ageabs=[]
for j in range(1,21):
    if j<10:
        arr="0"+str(j)
    else:
        arr=str(j)
    url_req="https://www.insee.fr/fr/statistiques/2011101?geo=COM-751"+arr
    request_text = request.urlopen(url_req).read()
    page = bs4.BeautifulSoup(request_text, "lxml")
    tableau_participants = page.find('table', {'id' : "produit-tableau-POP_T0"})
    table_body = tableau_participants.find('tbody')
    rows = table_body.find_all('tr')
    li1=[]
    li2=[]
    for i in range(len(rows)):
        if i>=2:
           
            cols = rows[i].find_all('td')
            cols = [ele.text.strip() for ele in cols]
            li1.append(cols[-1])
            li2.append(cols[-2])
    liste_ageprop.append(li1)
    liste_ageabs.append(li2)
        
        
gdf = gpd.read_file('/Users/dalilyoucefi/Downloads/arrondissements.geojson').sort_values(by="c_ar").reset_index()

liste2=np.array(liste_ageprop)
gdf["prop_0-14"]=liste2[:,0].tolist()
gdf["prop_15-29"]=liste2[:,1].tolist()
gdf["prop_30-44"]=liste2[:,2].tolist()
gdf["prop_45-59"]=liste2[:,3].tolist()
gdf["prop_60-74"]=liste2[:,4].tolist()
gdf["prop_75+"]=liste2[:,5].tolist()

liste3=np.array(liste_ageabs)
gdf["nombre_0-14"]=liste3[:,0].tolist()
gdf["nombre_15-29"]=liste3[:,1].tolist()
gdf["nombre_30-44"]=liste3[:,2].tolist()
gdf["nombre_45-59"]=liste3[:,3].tolist()
gdf["nombre_60-74"]=liste3[:,4].tolist()
gdf["nombre_75+"]=liste3[:,5].tolist()

gdf["pop"]=gdf["nombre_0-14"]+gdf["nombre_15-29"]+gdf["nombre_30-44"]+gdf["nombre_45-59"]+gdf["nombre_60-74"]+gdf["nombre_75+"]
li=[9863,21872,29638,17838,24817,21062,13936,10147,26888,323888,41341,8686,24896,23684,27201,9714,29166,31701,27274,32494]
gdf["densite"]=li
gdf2=gdf[["l_ar","c_ar",'prop_30-44', 'prop_45-59', 'prop_60-74', 'prop_75+', 'nombre_0-14',
       'nombre_15-29', 'nombre_30-44', 'nombre_45-59', 'nombre_60-74',
       'nombre_75+', 'pop', 'densite']]
gdf_quart=gpd.read_file('/Users/dalilyoucefi/Downloads/quartier_paris.geojson')
gdf3=gdf_quart.merge(gdf2, left_on="c_ar",right_on="c_ar")



stations = open("/Users/dalilyoucefi/Downloads/emplacement-des-gares-idf.geojson", "r")
stations_2 = gpd.read_file(stations)

stations= stations_2[["gares_id","nomlong","mode","ligne","geometry"]]

def nombrestation(x):
    li=[0 for i in range(80)]
    for j in range(len(x)):
        
        for i in range(80):
            if x["geometry"][j].within(gdf3["geometry"][i]):
                li[i]+=1
    return (li)

gdf3["nombretransport"]=nombrestation(gdf3)

gdf3.to_file("/Users/dalilyoucefi/Desktop/BaseQuartier.shp")
