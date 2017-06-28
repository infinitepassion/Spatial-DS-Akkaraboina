"""
Program:
--------
     Program 4 - GeoJson.
     To generate 1000earthquakes_geojson.geojson
Description:
------------
    Read a JSON file and create a GEOJSON file for 1000 earthquake objects.
    
Name: Manju Yadav Akkaraboina
Date: 29 Jun 2016
"""

import os,sys,json
import collections 

path=os.getcwd()+"\WorldData\\earthquakes-1960-2017.json"
f=open (path,"r")




data=f.read()

#pp.pprint(data)

data=json.loads(data)

all_quakes=[]


counter=0
for k,v in data.items():
    for l in v:
        if counter<1000:
            gj=collections.OrderedDict()
            gj['type']="Feature"
            gj['properties']=l
            lon=l['geometry']['coordinates'][0]
            lat=l['geometry']['coordinates'][1]
            depth=l['geometry']['coordinates'][2]
            gj['properties']['depth']=depth
            del gj['properties']['geometry']
            gj['depth']=depth
            gj['geometry']={}
            gj['geometry']['type']="Point"
            gj['geometry']['coordinates']=[
                lon,
                lat
                ]
            counter+=1
            all_quakes.append(gj)
        else:
            continue



fp=open("Z:\\MS\MWSU\\Summer 1 2017\\program_4\\geo_json\\1000_earthquakes_geojson.geojson","w")

fp.write(json.dumps(all_quakes,sort_keys=False,indent=4,separators=(',', ': ')))

fp.close()