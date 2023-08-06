#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gpd
from shapely.geometry import Point
import requests, json

kakaoapikey = input('Kakao Rest Api key : ')
korea_gdf = gpd.read_file('data/HangJeongDong_ver20230701.geojson')

def get_location(address):
    global kakaoapikey
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    headers = {"Authorization": f"KakaoAK {kakaoapikey}"}
    api_json = json.loads(str(requests.get(url,headers=headers).text))
    address = api_json['documents'][0]['address']
    crd = {"lat": str(address['y']), "lng": str(address['x'])}
    return crd

def get_hjdong(address):
    global korea_gdf 
    location = get_location(address)
    point = Point(location['lng'], location['lat'])
    row = korea_gdf[korea_gdf.geometry.contains(point)]
    region_info = row.iloc[0] if not row.empty else None
    return region_info['adm_nm']


# In[ ]:




