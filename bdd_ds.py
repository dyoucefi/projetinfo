# -*- coding: utf-8 -*-
"""bdd ds.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tDMgrBn8CQ_xM2zjPYZWFFoeeQYR028j
"""

!pip install git+git://github.com/geopandas/geopandas.git

from google.colab import files

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

import pandas as pd
import geopandas as gpd
import json
import io

#importation des données des logements sociaux à Paris
file_name='logements-sociaux-finances-a-paris.geojson'
file = open(file_name)
gdf_logements_sociaux = gpd.read_file(file)

#suppression de variables
gdf_logements_sociaux.drop(['nature_programme','arrdt','ville','n_livraison','adresse_programme','code_postal','annee','bs','nb_plai','nb_plus','nb_pluscd','nb_pls','mode_real','commentaires','coord_x_l93','coord_y_l93'], 1, inplace=True)

# on importe les données
file_name='quartier_paris.geojson'
file = open(file_name)
gdf = gpd.read_file(file)

def quartierappartenance(point):
    for i in range(80):
        if point.within(gdf["geometry"][i]):
            return gdf["l_qu"][i]

def numquartierappartenance(point):
    for i in range(80):
        if point.within(gdf["geometry"][i]):
            return gdf["c_qu"][i]


gdf_logements_sociaux["quartier"]=gdf_logements_sociaux["geometry"].apply(quartierappartenance)
gdf_logements_sociaux["numquartier"]=gdf_logements_sociaux["geometry"].apply(numquartierappartenance)

gdf333=gdf_logements_sociaux.sort_values(by=['numquartier'])
gdf333

# importation des données de open data paris sur les loyers à paris
df_l= pd.read_csv(io.StringIO(uploaded['logement-encadrement-des-loyers.csv'].decode('utf-8')),sep=';')

# suppression de variables
df_l.drop(['Nombre de pièces principales','Secteurs géographiques','Epoque de construction','Type de location','Loyers de référence majorés','Loyers de référence minorés','Année','Ville','Numéro INSEE du quartier'],1,inplace=True)

# On trie la table par le numéro du quartier administratif
df_loyer = df_l.sort_values(by=['Numéro du quartier'])

# on remarque que chaque quartier est représenté 32 fois on va donc calculer la moyenne des loyers de références de chaque quartier

# Tout d'abord on crée la variable moyenne loyer
df_loyer['Moyenne loyer']=0

#on convertit la colonne loyers de référence en valeur numérique
df_lf=df_loyer['Loyers de référence'].apply(pd.to_numeric)

for i in range(0,80):
    a = 32*i
    b = 32*(i+1)
    c = 0
    d = 0
    for j in range (a,b,1):
        c += df_lf.iloc[j]
    d = c/32
    for k in range (a,b,1):
        df_loyer.iloc[[k],[5]]=d #on affecte à chaque ligne sa moyenne de loyer associé à son quartier afdministartif
        
# On va supprimer la colonne 'Loyers de référence'
df_loyer.drop(['Loyers de référence'],1,inplace=True)

# On va supprimer des lignes du data frame de telles sortes qu'on obtienne avec un data frame avec 80 lignes = nombre de quartier administratif

#on va créer la liste des lignes à supprimer 
g = []
for m in range(0,80):
    a = 32*m+1
    b = 32*(m+1)
    for n in range(a,b,1):
        g.append(n)
        
# on retire les lignes de df3_tri
df_loyer.drop(df_loyer.index[g],0,inplace=True)

df_loyer
# on remarque que le numéro du quartier et le nom du quartier n'est pas associé de la même façon que dans gdf on va donc changer cela
df_loyer



# on importe les données sur les commerces parisiens
file_name='coronavirus-commercants-parisiens-livraison-a-domicile.geojson'
file = open(file_name)
gdf_commerce = gpd.read_file(file)

gdf_commerce['quartier']=0

# on va indiquer à quel quartier administratif appartient le commerce

gdf_commerce["quartier"]=gdf_commerce["geometry"].apply(quartierappartenance)

gdf_commerce



