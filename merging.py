#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:08:56 2020

@author: dalilyoucefi
"""

import geopandas as gpd
import pandas as pd

gdf = gpd.read_file("/Users/dalilyoucefi/Desktop/GeoTier9HLu.shp")
gdf2=gpd.read_file("/Users/dalilyoucefi/Desktop/GeoTier14HLu.shp")
gdf3=gpd.read_file("/Users/dalilyoucefi/Desktop/GeoTier19HLu.shp")

gdf4=gdf.append(gdf2,ignore_index=True)
gdf5=gdf4.append(gdf3,ignore_index=True)

gdf5.to_file("/Users/dalilyoucefi/Desktop/GeoTierLu.shp")

gdf_quart=gpd.read_file("/Users/dalilyoucefi/Desktop/BaseQuarier.shp")





