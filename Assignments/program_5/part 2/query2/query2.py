"""
Program:
--------
    Program 5 - Query 2: Nearest Neighbor:

Description:
------------
    Click on the world map and get the nearest feature within XXX miles, possibly with specific feature values, further filtering the query (magnitude of earthquake, etc.) where features are listed below:
            Volcanos
            Earthquakes
            Meteors

Name: Manju Yadav Akkaraboina
Date: 05 JUL 2017
"""

import pygame
from pygame.locals import *
import json
import os,sys
import math 
from pymongo import MongoClient
from math import radians, cos, sin, asin, sqrt

"""
This example based on a 1024x512 screen size. If you screen size is different, then 
you need to adjust. Mercator expects 1024x768 ratio (I'm pretty sure) that's why
I subtract 256 from the 'y' before I plot it. So you need to add that back to the 
'y' when you get a Lon/Lat. 
"""

# BASE = os.path.dirname(os.path.realpath(__file__))

# RADIUS_KM = 6371  # in km
# RADIUS_MI = 3959  # in mi

class mouse_event_feature:
    def __init__(self):
        self.BASE = os.path.dirname(os.path.realpath(__file__))
        self.RADIUS_KM = 6371  # in km
        self.RADIUS_MI = 3959  # in mi
        self.screen_width=1024
        self.screen_height=512

        self.client = MongoClient()

        self.db_airports = self.client.world_data.airports
        self.db_states = self.client.world_data.states
        self.db_volcano= self.client.world_data.volcanos
        self.db_cities=self.client.world_data.cities
        self.db_states=self.client.world_data.states
        self.db_earthquakes=self.client.world_data.earthquakes
        self.db_meteorites=self.client.world_data.meteorites
        self.db_terror=self.client.world_data.terrorism

    def mercX(self,lon,zoom = 1):
        """
        """
        lon = math.radians(lon)
        a = (256 / math.pi) * pow(2, zoom)
        b = lon + math.pi
        return int(a * b)

    def mercY(self,lat,zoom = 1):
        """
        """
        lat = math.radians(lat)
        a = (256.0 / math.pi) * pow(2, zoom)
        b = math.tan(math.pi / 4 + lat / 2)
        c = math.pi - math.log(b)
        return int(a * c)

    def mercToLL(self,point):
        lng,lat = point
        lng = lng / 256.0 * 360.0 - 180.0
        n = math.pi - 2.0 * math.pi * lat / 256.0
        lat = (180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
        return (lng, lat)
        
    def toLLtest(self,point):
        ans = []
        x,y = point
        for i in range(1,5):
            print(i)
            ans.append(mercToLL((x/i,y/i)))
        ans.append(mercToLL((x/4,y)))
        return ans

    def toLL(self,point):
        ans = []
        x,y = point
        y += 256
        return self.mercToLL((x/4,y/4))

    def _haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956 # Radius of earth in kilometers. Use 6371 for km
        return c * r
    def find_volcanos(self,x,y,r,field_value=None,min_max=None,max_results=None,flag=None):
        
        """
        Get the nearest volcanos near the point x,y 
        Input:
            x: longitude
            y: latitude
            r: radius 
            field_value: value for altitude
            min_max: min/max
            max_results: value for min/max
            flag: to identify the positional params and execute the query based on them 
        """
        
        volcanos=[]
        
        lon1=float(x)
        lat1=float(y)
        if flag==1:
            vol_res = self.db_volcano.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon1, lat1 ]  , r / 3963.2 ] } } ,"properties.Altitude": {'$gt' : field_value}} )
            i=0   
            for  vol in vol_res:
                i+=1
                if i>=max_results :
                    continue
                else:

                    lon2 = vol['geometry']['coordinates'][0]
                    lat2 = vol['geometry']['coordinates'][1]
                
                    d = self._haversine(lon1,lat1,lon2,lat2)
                    if d<r:
                        volcanos.append(vol['geometry']['coordinates'])
        else:
            vol_res = self.db_volcano.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon1, lat1 ]  , r / 3963.2 ] } }} )
         
            for  vol in vol_res:
                

                    lon2 = vol['geometry']['coordinates'][0]
                    lat2 = vol['geometry']['coordinates'][1]
                
                    d = self._haversine(lon1,lat1,lon2,lat2)
                    if d<r:
                        volcanos.append(vol['geometry']['coordinates'])

        return volcanos   
    def find_earthquake(self,x,y,r,field_value=None,min_max=None,max_results=None,flag=None):
        """
        Get the nearest earthquakes near the point x,y 
        Input:
            x: longitude
            y: latitude
            r: radius 
            field_value: value for magnitude
            min_max: min/max
            max_results: value for min/max
            flag: to identify the positional params and execute the query based on them 
        """
        earthquakes=[]
       
        
        lon1=float(x)
        lat1=float(y)
        
        if flag==1:
            eq_res = self.db_earthquakes.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon1, lat1 ]  , r / 3963.2 ] } } ,"properties.rms": {'$gt' : field_value}} )
            i=0   
            for  eq in eq_res:
                i+=1
                if i>=max_results :
                    continue
                else:

                    lon2 = eq['geometry']['coordinates'][0]
                    lat2 = eq['geometry']['coordinates'][1]
                
                    d = self._haversine(lon1,lat1,lon2,lat2)
                    if d<r:
                        earthquakes.append(eq['geometry']['coordinates'])
        else:
            eq_res = self.db_earthquakes.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon1, lat1 ]  , r / 3963.2 ] } }} )
         
            for  eq in eq_res:
                

                    lon2 = eq['geometry']['coordinates'][0]
                    lat2 = eq['geometry']['coordinates'][1]
                
                    d = self._haversine(lon1,lat1,lon2,lat2)
                    if d<r:
                        earthquakes.append(eq['geometry']['coordinates'])


        return earthquakes

    def find_meteorites(self,x,y,r,field_value=None,min_max=None,max_results=None,flag=None):
        """
        Get the nearest meteorites near the point x,y 
        Input:
            x: longitude
            y: latitude
            r: radius 
            field_value: value for mass
            min_max: min/max
            max_results: value for min/max
            flag: to identify the positional params and execute the query based on them 
        """
        meteorites=[]
        lon1=float(x)
        lat1=float(y)
        if flag==1:
            met_res = self.db_meteorites.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon1, lat1 ]  , r / 3963.2 ] } } ,"properties.mass": {'$gt' : field_value}} )
            i=0   
            for  m in met_res:
                i+=1
                if i>=max_results :
                    continue
                else:

                    lon2 = m['geometry']['coordinates'][0]
                    lat2 = m['geometry']['coordinates'][1]
                
                    d = self._haversine(lon1,lat1,lon2,lat2)
                    if d<r:
                        meteorites.append(m['geometry']['coordinates'])
        
        
        else:
            met_res = self.db_meteorites.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon1, lat1 ]  , r / 3963.2 ] } }} )
            
            for  m in met_res:
                lon2 = m['geometry']['coordinates'][0]
                lat2 = m['geometry']['coordinates'][1]
            
                d = self._haversine(lon1,lat1,lon2,lat2)
                if d<r:
                    meteorites.append(m['geometry']['coordinates'])

        return meteorites
    def clean_area(self,screen,origin,width,height,color):
        """
        Prints a color rectangle (typically white) to "erase" an area on the screen.
        Could be used to erase a small area, or the entire screen.
        """
        ox,oy = origin
        points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
        pygame.draw.polygon(screen, color, points, 0)
        
    def mercX(self,lon,zoom = 1):
        """
        """
        lon = math.radians(lon)
        a = (256 / math.pi) * pow(2, zoom)
        b = lon + math.pi
        return int(a * b)

    def mercY(self,lat,zoom = 1):
        """
        """
        lat = math.radians(lat)
        a = (256.0 / math.pi) * pow(2, zoom)
        b = math.tan(math.pi / 4 + lat / 2)
        c = math.pi - math.log(b)
        return int(a * c)
    def adjust_cord(self,points):
        """
        To scale th coordinates
        Input:
            points: the points which we will be scaling
        """
        ad=[]
        for p in points:
            
            lon,lat = p
            x = (self.mercX(lon) / 1024 * self.screen_width)
            y = (self.mercY(lat) / 512 * self.screen_height) - (self.screen_height/2)
            ad.append([x,y])
        return ad

    def start_display(self,vflag,eq_flag,met_flag,r,flag=None,field_value=None,min_max=None,max_results=None,lon_lat=None):
            
            """
            To start the display screen 
            Input:
                vflag: volcano flag
                eq_flag: earthquake flag
                met_flag: meteorite flag
                r: radius
                flag: to identify the positional params and execute the query based on them 
                field_value=Altitude/Magnitude/Mass
                min_max=min/max
                max_results=min_max value
                lon_lat=lon_lat value
                
            """
            background_colour = (255,255,255)
            black = (0,0,0)
            (screen_width, screen_height) = (self.screen_width, self.screen_height)

            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption('Simple Map')

            bg = pygame.image.load(os.path.join(self.BASE,"1024x512.png"))

            screen = pygame.display.set_mode((screen_width,screen_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
            screen.blit(pygame.transform.scale(bg,(screen_width,screen_height)), (0, 0))

            # pygame.draw.circle(screen,(255,0,0),(int(self.mercX(131.6)),int(self.mercY(34.5))-256),2,0)
            # pygame.draw.circle(screen,(255,0,0),(int(self.mercX(140.29)),int(self.mercY(37.64))-256),2,0)
            # pygame.draw.circle(screen,(255,0,0),(int(self.mercX(139.2)),int(self.mercY(36.56))-256),2,0)
            # pygame.draw.circle(screen,(255,0,0),(self.mercX(-98.5034180),self.mercY(33.9382331)-256),2,0)

            pygame.display.flip()

            volcanos=[]
            earthquakes=[]
            meteorites=[]
            while True:
                
                event = pygame.event.wait()
                if event.type == MOUSEBUTTONUP:
                    #print(event.pos)
                    x,y = event.pos
                    x,y=(self.toLL((x,y)))
                    if v_flag==1:
                        if flag==1:
                            volcanos=self.find_volcanos(x,y,r,field_value,min_max,max_results,1)
                        else:
                            volcanos=self.find_volcanos(x,y,r)
                        volcanos_adjusted=self.adjust_cord(volcanos)
                        for vol in volcanos_adjusted:
                            lon,lat=vol
                            pygame.draw.circle(screen, (255,0,0), [int(lon),int(lat)], 1, 0)
                    if eq_flag==1:
                        if flag==1:
                            earthquakes=self.find_earthquake(x,y,r,field_value,min_max,max_results,1)
                        else:
                            earthquakes=self.find_earthquake(x,y,r)
                        earthquakes_adjusted=self.adjust_cord(earthquakes)
                        for eq in earthquakes_adjusted:
                            lon,lat=eq
                            pygame.draw.circle(screen, (255,255,0), [int(lon),int(lat)], 1, 0)
                    if met_flag==1:
                        if flag==1:
                            meteorites=self.find_meteorites(x,y,r,field_value,min_max,max_results,1)
                        else:
                            meteorites=self.find_meteorites(x,y,r)
                        meteorites_adjusted=self.adjust_cord(meteorites)
                        for m in meteorites_adjusted:
                            lon,lat=m
                            pygame.draw.circle(screen, (0,255,0), [int(lon),int(lat)], 1, 0)

                

                pygame.display.flip()

                if event.type == QUIT:
                    pygame.display.quit()


if __name__=='__main__':
    v_flag=0
    eq_flag=0
    met_flag=0
    mef=mouse_event_feature()
    lon_lat=0
    if len(sys.argv)>=7:
        feature=sys.argv[1].upper()
        
        field=sys.argv[2]
        field_value=float(sys.argv[3])
        min_max=sys.argv[4]
        if min_max=="min":
            min_max="min"
        else:
            min_max="max"
        max_results=float(sys.argv[5])
        if max_results==0:
            v_count=mef.db_volcano.count()
            e_count=mef.db_earthquakes.count()
            m_count=mef.db_meteorites.count()
            max_results=max(v_count,e_count,m_count)
            
            #print(max_results,v_count,e_count,m_count)
        radius=float(sys.argv[6])
        if len(sys.argv)==8:
            lon_lat=sys.argv[7]
        
        if feature=='VOLCANOS':
            v_flag=1
            v_alt_flag=1
            mef.start_display(v_flag,eq_flag,met_flag,radius,v_alt_flag,field_value,min_max,max_results,lon_lat)
        elif feature=='EARTHQUAKES':
            eq_flag=1
            eq_mag_flag=1
            mef.start_display(v_flag,eq_flag,met_flag,radius,eq_mag_flag,field_value,min_max,max_results,lon_lat)
        else:
            met_flag=1
            met_mass_flag=1
            mef.start_display(v_flag,eq_flag,met_flag,radius,met_mass_flag,field_value,min_max,max_results,lon_lat)
    elif len(sys.argv)==2:
        radius=float(sys.argv[1])
        
        v_flag=1
        eq_flag=1
        met_flag=1

        mef.start_display(v_flag,eq_flag,met_flag,radius)
    else:
        print ("Invalid number of paramneters: run in the following format")
        print()
        print("python query2.py [feature] [field] [field value] [min/max] [max results] [radius] [lon,lat]")
        print()
        print("feature = volcano, earthquake, meteor")
        print("field = some field in the 'properties' to compare against")
        print("field_value = the value in wich to compare with")
        print("min/max = whether we want all results greater than or less than the field_value.")
        print("radius (in miles) = radius to apply our query with.")
        print("lon,lat (optional) = Some point coords to act as a mouse click instead of actually clicking the screen.")
        print ("                    or")
        print( "python query2.py [radius]")
    


    