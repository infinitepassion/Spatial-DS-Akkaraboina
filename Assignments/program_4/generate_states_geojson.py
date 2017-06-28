"""
Program:
--------
     Program 4 - GeoJson.
     To generate 1000_states_geo_json.geojson
Description:
------------
    Read a JSON file and create a GEOJSON file for 1000 state objects.
    
Name: Manju Yadav Akkaraboina
Date: 29 Jun 2016
"""

import os,sys,json
import collections 


path=os.getcwd()+"\WorldData\\state_borders.json"
f=open (path,"r")

data=f.read()

#pp.pprint(data)

data=json.loads(data)

all_states=[]

counter=0
for v in data:
    if counter<1000:
            
        gj=collections.OrderedDict()
        gj['type']="Feature"
        gj['properties']=v
        k=v['borders']
        counter+=1
        del gj['properties']['borders']
        gj['geometry']={}
        gj['geometry']['type']="Polygon"
        gj['geometry']['coordinates']=k
        all_states.append(gj)
    else:
        continue
            


path=os.getcwd()+"\geo_json\\1000_states_geo_json.geojson"

fp=open(path,"w")

fp.write(json.dumps(all_states,sort_keys=False,indent=4,ensure_ascii = False))

fp.close()