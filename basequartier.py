#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 16:12:50 2020

@author: dalilyoucefi
"""

import geopandas as gpd
import pandas as pd

# importation des données des logements sociaux à Paris

df2= gpd.read_file("/Users/dalilyoucefi/Downloads/logements-sociaux-finances-a-paris/logements-sociaux-finances-a-paris.shp")
# suppression de variables
df2.drop(['nature_prog','arrdt','ville','n_livraison','adresse_pro','code_postal','annee','bs','nb_plai','nb_plus','nb_pluscd','nb_pls','mode_real','commentaire','coord_x_l93','coord_y_l93'],1, inplace=True)

# on va attribuer à chaque geo_point un quartier administratif


# importation des données de open data paris sur les loyers à paris
df3 = gpd.read_file('/Users/dalilyoucefi/Downloads/logement-encadrement-des-loyers/logement-encadrement-des-loyers.shp')

# suppression de variables
df3.drop(['piece','id_zone','epoque','meuble_txt','max','min','annee','ville'],1,inplace=True)

# On trie la table par le numéro du quartier administratif
df3_tri = df3.sort_values(by=['id_quartier'])

# on remarque que chaque quartier est représenté 32 fois on va donc calculer la moyenne des loyers de références de chaque quartier

# Tout d'abord on crée la variable moyenne loyer
df3_tri['Moyenne loyer']=0

#on convertit la colonne loyers de référence en valeur numérique
df3_trif=df3_tri['ref'].apply(pd.to_numeric)

for i in range(0,80):
    a = 32*i
    b = 32*(i+1)
    c = 0
    d = 0
    for j in range (a,b,1):
        c += df3_trif.iloc[j]
    d = c/32
    for k in range (a,b,1):
        df3_tri.iloc[[k],[5]]=d #on affecte à chaque ligne sa moyenne de loyer associé à son quartier afdministartif
        
# On va supprimer la colonne 'Loyers de référence'
df3_tri.drop(['ref'],1,inplace=True)

# On va supprimer des lignes du data frame de telles sortes qu'on obtienne avec un data frame avec 80 lignes = nombre de quartier administratif

#on va créer la liste des lignes à supprimer 
l = []
for m in range(0,80):
    a = 32*m+1
    b = 32*(m+1)
    for n in range(a,b,1):
        l.append(n)
        
# on retire les lignes de df3_tri
df3_tri.drop(df3_tri.index[l],0,inplace=True)


gdf2=gpd.read_file('/Users/dalilyoucefi/Downloads/quartier_paris.geojson')

def quartierappartenance(point):
    for i in range(80):
        if point.within(gdf2["geometry"][i]):
            return gdf2["l_qu"][i]
def quartierappartenance2(point):
    for i in range(80):
        if point.within(gdf2["geometry"][i]):
            return gdf2["c_qu"][i]
df2["quartier"]=0
df2["quartier"]=df2["geometry"].apply(quartierappartenance)
df2["id_quartier"]=df2["geometry"].apply(quartierappartenance)






