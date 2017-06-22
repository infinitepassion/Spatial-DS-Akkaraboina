"""
Program:
--------
    Program 3 - DBscan - Earthquake Data

Description:
------------
    Create a json file with all the earthquakes that have a magnitude 7 and greater from the year 1960-2016 and using pygame to display each point representing an earthquake and save the ouput as an image.
    
Name: Manju Yadav Akkaraboina
Date: 22 Jun 2016
"""

import os ,sys
import json,glob
import get_quake_points
import adjust_quake_points
import display_quake_points

"""
The below code iterates for all years ranging from 1960 to 2017 and generates the quake-year.json file and quake-year-condenses.json files
"""
path = '/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Resources/EarthquakeData'
years = [x for x in range(1960,2018)]
months = [x for x in range(0,12)]
for y in years:
    #print("Year:%s" % (y))
    r = get_quake_points.get_earth_quake_data(y,[1,12],7,None,True)
    f = open('./quake-'+str(y)+'.json','w')
    f.write(json.dumps(r, sort_keys=True,indent=4, separators=(',', ': ')))
    f.close()
    r = get_quake_points.get_earth_quake_data(y,[1,12],7,None,True)
    rc = get_quake_points.condense_file(r)
    f = open('./quake-'+str(y)+'-condensed.json','w')
    f.write(json.dumps(rc, sort_keys=True,indent=4, separators=(',', ': ')))
    f.close()


"""
Open our condensed json file to extract points

"""
for filename in os.listdir(os.getcwd()):
        if filename.endswith("-condensed.json"):
            f = open(filename,'r')
            data = json.loads(f.read())
            
            allx = []
            ally = []
            points = []

            # Loop through converting lat/lon to x/y and saving extreme values. 
            for quake in data:
                #st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                lon = quake['geometry']['coordinates'][0]
                lat = quake['geometry']['coordinates'][1]
                x,y = (adjust_quake_points.mercX(lon),adjust_quake_points.mercY(lat))
                allx.append(x)
                ally.append(y)
                points.append((x,y))

            # Create dictionary to send to adjust method
            extremes = {}
            extremes['max_x'] = max(allx)
            extremes['min_x'] = min(allx)
            extremes['max_y'] = max(ally)
            extremes['min_y'] = min(ally)

            # Get adjusted points
            screen_width = 1024
            screen_height = 512
            adj = adjust_quake_points.adjust_location_coords(extremes,points,screen_width,screen_height)

            # Save adjusted points
            #print(filename)
            op_file=filename[:-14]+'adjusted.json'
            #print(op_file)
            f = open(op_file,'w')
            f.write(json.dumps(adj, sort_keys=True,indent=4, separators=(',', ': ')))
            f.close()

"""
the below function call displays all the quake year wise with 1 second delay between each year data
"""
display_quake_points.display()


