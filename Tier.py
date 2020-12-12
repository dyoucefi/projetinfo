#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 11:19:45 2020

@author: dalilyoucefi
"""

import requests

r=requests.get("https://platform.tier-services.io/v2/vehicle?zoneId=PARIS",headers={"X-Api-Key": "bpEUTJEBTf74oGRWxaIcW7aeZMzDDODe1yBoSxi2"})
print(r.json()["data"][1])

import pandas as pd

df= pd.DataFrame(data=r.json()["data"])
BatteryLevel=[r.json()["data"][i]["attributes"]["batteryLevel"] for i in range(len(r.json()["data"]))]
Lat=[r.json()["data"][i]["attributes"]["lat"] for i in range(len(r.json()["data"]))]
Lng=[r.json()["data"][i]["attributes"]["lng"] for i in range(len(r.json()["data"]))]
Type=[r.json()["data"][i]["attributes"]["vehicleType"] for i in range(len(r.json()["data"]))]
Status=[r.json()["data"][i]["attributes"]["state"] for i in range(len(r.json()["data"]))]
ID=[r.json()["data"][i]["id"] for i in range(len(r.json()["data"]))]

df_Tier=pd.DataFrame(columns=["ID","BatteryLevel","Lat","Lng","Type","Status"])
df_Tier = df_Tier.fillna(0)
df_Tier["ID"]=ID
df_Tier["BatteryLevel"]=BatteryLevel
df_Tier["Lat"]=Lat
df_Tier["Lng"]=Lng
df_Tier["Type"]=Type
df_Tier["Status"]=Status
df_Tier["Heure"]="19h"
df_Tier["Jour"]="Lundi"



df_Tier.to_csv("/Users/dalilyoucefi/Desktop/TierBase9HSa.csv")
