"""
Program:
--------
     Program 4 - GeoJson.
     To generate 1000_airports_geo_json.geojson
Description:
------------
    Read a JSON file and create a GEOJSON file for 1000 airport objects.
    
Name: Manju Yadav Akkaraboina
Date: 29 Jun 2016
"""

import os,sys,json
import collections 

path=os.getcwd()+"\WorldData\\airports.json"
f=open (path,"r")

data=f.read()

#pp.pprint(data)

data=json.loads(data)

all_aiports=[]


for k,v in data.items():
    gj=collections.OrderedDict()
    gj['type']="Feature"
    gj['properties']=v
    lat=v['lat']
    lon=v['lon']
    lat=v['lat']
    lon=v['lon']
    del gj['properties']['lat']
    del gj['properties']['lon']
    gj['geometry']={}
    gj['geometry']['type']="Point"
    gj['geometry']['coordinates']=[
        lon,
        lat
        ]
    all_aiports.append(gj)


#pp.pprint(all_aiports[0])

fp=open("Z:\\MS\MWSU\\Summer 1 2017\\program_4\\geo_json\\1000_airports_geo_json.geojson","w")

fp.write(json.dumps(all_aiports,sort_keys=False,indent=4,separators=(',', ': ')))

fp.close()