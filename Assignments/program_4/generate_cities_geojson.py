"""
Program:
--------
     Program 4 - GeoJson.
     To generate 1000_cities_geo_json.geojson
Description:
------------
    Read a JSON file and create a GEOJSON file for 1000 city objects.
    
Name: Manju Yadav Akkaraboina
Date: 29 Jun 2016
"""

import os,sys,json
import collections 


path=os.getcwd()+"\WorldData\\world_cities_large.json"
f=open (path,"r")

data=f.read()

data=json.loads(data)

all_cities=[]

counter=0

for k,v in data.items():
    for value in v:
        if counter<1000:
            counter+=1
            gj = collections.OrderedDict()
            gj['type'] = 'Feature'
            gj['properties'] = value
            lat = value['lat']
            lon = value['lon']
            if not lat and not lon:
                continue
            lat = float(lat)
            lon = float(lon)
            del gj['properties']['lat']
            del gj['properties']['lon']
            gj['geometry'] = {}
            gj['geometry']['type'] = 'Point'
            gj['geometry']['coordinates']=[lon,lat]
            all_cities.append(gj)
        else:
            continue


path=os.getcwd()+"\geo_json\\1000_cities_geo_json.geojson"

fp=open(path,"w")

fp.write(json.dumps(all_cities,sort_keys=False,indent=4,separators=(',', ': ')))

fp.close()