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
gdf_logements_soc = gpd.read_file(file)

#suppression de variables
gdf_logements_soc.drop(['nature_programme','arrdt','ville','n_livraison','adresse_programme','code_postal','annee','bs','nb_plai','nb_plus','nb_pluscd','nb_pls','mode_real','commentaires','coord_x_l93','coord_y_l93'], 1, inplace=True)

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


gdf_logements_soc["quartier"]=gdf_logements_soc["geometry"].apply(quartierappartenance)
gdf_logements_soc["numquartier"]=gdf_logements_soc["geometry"].apply(numquartierappartenance)
gdf_logements_soc
# on va indiquer le nombre de logement qu'on a par quartier administratif

gdf_logements_sociaux = gdf_logements_soc.groupby(['numquartier'],as_index=False).sum()
gdf_logements_sociaux.columns

# on importe les données
file_name='logement-encadrement-des-loyers.geojson'
file = open(file_name)
gdf_l = gpd.read_file(file)


# suppression de variables
gdf_l.drop(['ville','epoque','meuble_txt','code_grand_quartier','piece','max','min','id_zone','annee'],1,inplace=True)

# on va calculer la moyenne des loyers dans chaque quartier administratif
gdf_loyer=gdf_l.groupby(['id_quartier'],as_index=False).mean()
g1 = gdf_loyer.rename(columns={'id_quartier':'numquartier'})
g1

# on importe les données sur les commerces parisiens
file_name='coronavirus-commercants-parisiens-livraison-a-domicile.geojson'
file = open(file_name)
gdf_co = gpd.read_file(file)

gdf_co['quartier']=0

# on va indiquer à quel quartier administratif appartient le commerce 
gdf_co["quartier"]=gdf_co["geometry"].apply(quartierappartenance)
gdf_co['numquartier']=gdf_co['geometry'].apply(numquartierappartenance)
# on va supprimer des variables 
gdf_co.drop(['code_postal','description','nom_du_commerce','adresse','telephone','services','mail','type_de_commerce','site_internet','precisions'],1,inplace=True)

# on va créer une variable qui va indiquer le nombre total de commerce par quartier administratif
gdf_co['nombre_de_commerce']=1
gdf_commerce=gdf_co.groupby('numquartier',as_index=False).sum()
gdf_commerce

df1=pd.merge(g1,gdf_logements_sociaux,on="numquartier")

df_final = pd.merge(df1,gdf_commerce,on="numquartier")

df_final

