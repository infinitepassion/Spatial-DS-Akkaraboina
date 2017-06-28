"""
Program:
--------
     Program 4 - GeoJson.
      To generate 1000_countries_geo_json.geojson
Description:
------------
    Read a JSON file and create a GEOJSON file for 1000 country objects.
    
Name: Manju Yadav Akkaraboina
Date: 29 Jun 2016
"""


import os,sys,json
import collections 


path=os.getcwd()+"\WorldData\\countries.geo.json"
f=open (path,"r")

data=f.read()

data=json.loads(data)

counter=0

for d in data:
    if counter<1000:
        pass
    else:
        data.pop()

fp=open("Z:\\MS\MWSU\\Summer 1 2017\\program_4\\geo_json\\1000_countries_geo_json.geojson","w")

fp.write(json.dumps(data, sort_keys=False,indent=4, separators=(',', ': ')))

fp.close()