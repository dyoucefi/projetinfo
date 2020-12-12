#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 15:21:29 2020

@author: dalilyoucefi
"""
import requests, json
import urllib.parse
import pandas as pd
import geopandas as gpd

ent=pd.read_csv("/Users/dalilyoucefi/Downloads/entreprise.csv", sep=",")
ent["Code postal"]=ent["Code postal"].astype(str)
ent["fulladress"]=ent["Adresse"]+", "+ent["Code postal"]+ " "+ent["Ville"]
ent=ent.dropna().reset_index()
ent=ent.drop([13522]).reset_index()


def positionlon(adr):

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    api_url = "https://api-adresse.data.gouv.fr/search/?q="

    r = requests.get(api_url + urllib.parse.quote(adr),headers=headers)


    
    return(r.json()["features"][0]["geometry"]["coordinates"][0])

li=[]
i=0
for j in range(len(ent)):
    i+=1
    li.append(positionlon(ent["fulladress"][j]))
    print(i)

ent["lon"]=li
ent.to_csv("/Users/dalilyoucefi/Downloads/entrepriselon.csv")
ent3=pd.read_csv("/Users/dalilyoucefi/Downloads/entrepriselon.csv")


def positionla(adr):

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    api_url = "https://api-adresse.data.gouv.fr/search/?q="

    r = requests.get(api_url + urllib.parse.quote(adr),headers=headers)


    
    return(r.json()["features"][0]["geometry"]["coordinates"][1])

li1=[]
i=0
for j in range(len(ent3)):
    i+=1
    li1.append(positionla(ent3["fulladress"][j]))
    print(i)
ent3["la"]=li1
ent3.to_csv("/Users/dalilyoucefi/Downloads/entrepriselonlat.csv")


geoent = gpd.GeoDataFrame(ent3, geometry=gpd.points_from_xy(ent3.lon, ent3.la))
gdf2=gpd.read_file("/Users/dalilyoucefi/Downloads/quartier_paris.geojson")

def quartierappartenance(point):
    for i in range(80):
        print(i)
        if point.within(gdf2["geometry"][i]):
            return gdf2["l_qu"][i]
def quartierappartenance2(point):
    for i in range(80):
        print(i)
        if point.within(gdf2["geometry"][i]):
            return gdf2["c_qu"][i]
        
geoent["nomquartier"]=geoent["geometry"].apply(quartierappartenance)
geoent["id_quartier"]=geoent["geometry"].apply(quartierappartenance2)

geoent['nombreent']=1
ent1=geoent.groupby('id_quartier',as_index=False).sum()
ent1=ent1[["id_quartier","nombreent"]]

ent2=geoent.groupby('id_quartier',as_index=False).mean()
ent2=ent2[["id_quartier","CA 1"]]
df1=pd.merge(ent1,ent2,on="id_quartier")
df1.to_csv("/Users/dalilyoucefi/Desktop/entreprisefinal.csv")

        

    