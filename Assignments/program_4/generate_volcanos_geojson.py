"""
Program:
--------
     Program 4 - GeoJson.
     To generate 1000_volcanos_geo_json.geojson
Description:
------------
    Read a JSON file and create a GEOJSON file for 1000 volcano objects.
    
Name: Manju Yadav Akkaraboina
Date: 29 Jun 2016
"""

import os,sys,json
import collections 


path=os.getcwd()+"\WorldData\\world_volcanos.json"
f=open (path,"r")

data=f.read()

#pp.pprint(data)

data=json.loads(data)

all_volcanos=[]


counter=0

for i,v in enumerate(data):
    if counter<1000:
        counter+=1
        gj=collections.OrderedDict()
        gj['type']="Feature"
        gj['properties']=v
        if not v['Lat'] and not v['Lon']:
            continue
        lat=float(v['Lat'])
        lon=float(v['Lon'])
        del gj['properties']['Lat']
        del gj['properties']['Lon']
        gj['geometry']={}
        gj['geometry']['type']="Point"
        gj['geometry']['coordinates']=[
            lon,
            lat
            ]
        all_volcanos.append(gj)
    else:
        continue

fp=open("Z:\\MS\MWSU\\Summer 1 2017\\program_4\\geo_json\\1000_volcanos_geo_json.geojson","w")

fp.write(json.dumps(all_volcanos,sort_keys=False,indent=4,separators=(',', ': ')))

fp.close()