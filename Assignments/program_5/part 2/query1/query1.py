"""
Program:
--------
    Program 5 - Query 1: Find Interesting Features along some path

Description:
------------
    Select a starting point: X and a destination point Y. This can be done by mouse click, or by entering airport codes via sys.argv (e.g. python query1.py DFW MNL 500 to run query from Dallas / Fort Worth to Manilla Philippines with a 500 mile radius to look for interesting features).

    
Name: Manju Yadav Akkaraboina
Date: 05 JUL 2017
"""


from pymongo import MongoClient
import pprint as pp
import os,sys,time
from math import radians, cos, sin, asin, sqrt
import display
import time

class mongoHelper(object):
    def __init__(self):
        
        """
        This is used to get all the data documents from mongoDB and intialize all the variables
        """
        self.client = MongoClient()

        self.db_airports = self.client.world_data.airports
        self.db_states = self.client.world_data.states
        self.db_volcano= self.client.world_data.volcanos
        self.db_cities=self.client.world_data.cities
        self.db_states=self.client.world_data.states
        self.db_earthquakes=self.client.world_data.earthquakes
        self.db_meteorites=self.client.world_data.meteorites
        self.db_terror=self.client.world_data.terrorism

    def get_nearest_volcanos(self,path,r):
        """
        Get the nearest volcanos near the airport 
        Input:
            path: airport points in the path
            r: radius 
        """
        volcanos=[]
        for p in path:
            lon1=float(p[0])
            lat1=float(p[1])
            vol_res = self.db_volcano.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon1, lat1 ]  , 200 / 3963.2 ] } }} )
            
            for  vol in vol_res:
                lon2 = vol['geometry']['coordinates'][0]
                lat2 = vol['geometry']['coordinates'][1]
            
                d = self._haversine(lon1,lat1,lon2,lat2)
                if d<r:
                    volcanos.append(vol['geometry']['coordinates'])

        return volcanos
    def get_nearest_earthquake(self,path,r):
        
        """
        Get the nearest earthquakes near the airport 
        Input:
            path: airport points in the path
            r: radius 
        """
        
        earthquakes=[]
        for p in path:
            lon1=float(p[0])
            lat1=float(p[1])
            eq_res = self.db_earthquakes.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon1, lat1 ]  , 200 / 3963.2 ] } }} )
            
            for  eq in eq_res:
                lon2 = eq['geometry']['coordinates'][0]
                lat2 = eq['geometry']['coordinates'][1]
            
                d = self._haversine(lon1,lat1,lon2,lat2)
                if d<r:
                    earthquakes.append(eq['geometry']['coordinates'])

        return earthquakes

    def get_nearest_meteorite(self,path,r):
        """
        Get the nearest meteorites near the airport 
        Input:
            path: airport points in the path
            r: radius 
        """
        meteorites=[]
        for p in path:
            lon1=float(p[0])
            lat1=float(p[1])
            met_res = self.db_meteorites.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon1, lat1 ]  , 200 / 3963.2 ] } }} )
            
            for  m in met_res:
                lon2 = m['geometry']['coordinates'][0]
                lat2 = m['geometry']['coordinates'][1]
            
                d = self._haversine(lon1,lat1,lon2,lat2)
                if d<r:
                    meteorites.append(m['geometry']['coordinates'])

        return meteorites
    def get_nearest_airport(self,lon,lat,r,dlon,dlat,line,dist):
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        max=0
        next_ap={}
        for ap in air_res:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1]
            var=True
            for l in line:
                if float(lon2)==l[0] and float(lat2)==l[1]:
                    var=False
            if not var:
                pass
            else:

                if(float(lon2)==dlon and float(lat2)==dlat):
                    next_ap = ap
                    return next_ap
                else:
                    d = self._haversine(lon,lat,lon2,lat2)
                    d1=self._haversine(dlon,dlat,lon2,lat2)
                    if d <= r and d>max and d1<dist:
                        max = d
                        next_ap = ap
        if len(next_ap)==0:
            return "False"
        else:   
            return next_ap 

        # return closest_ap    
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
    
    def get_path(self,line,s_lon,s_lat,d_lon,d_lat,radius):
        """
        Get the  airport  points from source to destination
        Input:
            line: src to dest path points
            s_lon: src longitude
            s_lat: src latitude
            d_lon: dest longitude
            d_lat: dest latitude
            r: radius 

        """
        r=radius
        ap=True
        while ap:
            d = mh._haversine( s_lon,s_lat, d_lon,d_lat)
            
            if d>radius:
                next_ap=mh.get_nearest_airport(float(s_lon),float(s_lat),float(radius),float(d_lon),float(d_lat),line,d)
                if next_ap=='False':
                    #ap=False
                    radius+=100
                    print ("No more airports within the distance:", radius, "from the airport ", prev_ap,"increasing r to: ", radius)
                else:
                    line.append(next_ap['geometry']['coordinates'])
                    #print (next_ap['properties']['ap_name'])
                    s_lon=next_ap['geometry']['coordinates'][0]
                    s_lat=next_ap['geometry']['coordinates'][1]
                    prev_ap=next_ap['properties']['ap_name']
                    radius=r
                
            else:
                
                ap=False
      
        return line



import os,sys
import math
import pygame
from pygame.locals import *
from pymongo import MongoClient
from map_icons import map_icon
from mongo_helper import MongoHelper
from map_helper import *
from color_helper import ColorHelper

BASE = os.path.dirname(os.path.realpath(__file__))

class PygameHelper(object):
    def __init__(self,width,height):
        self.screen_width = width
        self.screen_height = height
        self.keyval = 1000

        self.bg = pygame.image.load(os.path.join(BASE,"images/2048x1024.png"))

        self.polygons = []             # any polygon to be drawn
        self.points = []               # any point to be drawn

        self.map_event_functions = {}

        pygame.init()
        self.game_images = {}

    def Capture(self,name,pos,size): # (pygame Surface, String, tuple, tuple)
        image = pygame.Surface(size)  # Create image surface
        image.blit(self.screen,(0,0),(pos,size))  # Blit portion of the display to the image
        pygame.image.save(image,name)  # Save the image to the disk
        
    def load_image(self,key,path,coord):
        """
        Params:
            key: name to reference image with
            path: path to image 
            coord: location to place image on screen
        """
        self.game_images[key] = {'pyg_image':pygame.image.load(path),'coord':coord}

    def adjust_point(self,p,icon=None):
        if icon:
            size = self._get_icon_size(icon)
            voffset = size
            hoffset = size//2
        else:
            voffset = 0
            hoffset = 0
        lon,lat = p
        x = (mercX(lon) / 1024 * self.screen_width) - hoffset
        scale = 1 / math.cos(math.radians(lat))             # not used
        y = (mercY(lat) / 512 * self.screen_height) - (self.screen_height/2) - voffset
        return (x,y)

    def adjust_cord(self,points):
        ad=[]
        for p in points:
            
            lon,lat = p
            x = (mercX(lon) / 1024 * self.screen_width)
            scale = 1 / math.cos(math.radians(lat))             # not used
            y = (mercY(lat) / 512 * self.screen_height) - (self.screen_height/2)
            ad.append([x,y])
        return ad

    def add_polygon(self,polygon,color,width):
        """
        Add polygons to local list to be drawn
        """
        outofrange = [-180, -90, 180, 90]
        adjusted = []
        for p in polygon[0]:
            if math.floor(p[0]) in outofrange or p[1] in outofrange:
                continue
            adjusted.append(self.adjust_point(p))
        self.polygons.append({'poly':adjusted,'color':color,'width':width})

    def add_points(self,point,icon):
        """
        Add points to local list to be drawn
        """
        if type(point) is list:
            for p in point:
                coord = self.adjust_point(p,icon)
                self.load_image(self._unique_key(), icon, coord)

    def draw_polygons(self):
        for poly in self.polygons:
            if len(poly['poly']) < 3:
                continue
            pygame.draw.polygon(self.screen,poly['color'],poly['poly'],poly['width'])

    def add_event_function(self,type,fun):
        if not type in self.map_event_functions:
            self.map_event_functions[type] = []
        self.map_event_functions[type].append(fun)

    def start_display(self,path,volcanos,earthquakes,meteorites):
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.screen.blit(pygame.transform.scale(self.bg,(self.screen_width,self.screen_height)), (0, 0))

        for key,image in self.game_images.items():
            self.screen.blit(image['pyg_image'],image['coord'])

        pygame.display.flip()
        running= True
        while running:
            pygame.event.pump()
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONUP:
                pass
            if event.type == KEYUP:
                if event.key == 273:
                    pass
                if event.key == 274:
                    pass

            #self.draw_polygons()
            for pointList in path:
                # Only use the x and y components of the points.
                drawPath = [[l[0], l[1]] for l in path]
                # Assume 'screen' is your display surface.
                pygame.draw.lines(self.screen,(0,0,255), False, drawPath,2)
                
            time.sleep(2)
            for vol in volcanos:
                lon,lat=vol
                pygame.draw.circle(self.screen, (255,0,0), [int(lon),int(lat)], 1, 0)
            time.sleep(2)
            for eq in earthquakes:
                lon,lat=eq
                pygame.draw.circle(self.screen, (255,255,0), [int(lon),int(lat)], 1, 0)
            time.sleep(2)
            for met in meteorites:
                lon,lat=met
                pygame.draw.circle(self.screen, (0,255,0), [int(lon),int(lat)], 1, 0)
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            pygame.display.flip()
            if event.type == QUIT:
                pygame.display.quit()
            elif event.type == VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                self.screen.blit(pygame.transform.scale(self.bg, event.dict['size']), (0, 0))
                for key,image in self.game_images.items():
                    self.screen.blit(image['pyg_image'],image['coord'])
                pygame.display.flip()

    def _unique_key(self):
        key = self.keyval
        self.keyval += 1
        return key

    def _get_icon_size(self,icon):
        sizes = ['16x','32x','64x','128x']
        for size in sizes:
            if size in icon:
                return int(size.replace('x',''))

class MapFacade(object):
    def __init__(self,width,height):
        self.screen_width = width
        self.screen_height = height
        self.mh = MongoHelper()
        self.pyg = PygameHelper(width,height)
    
    def run(self,path,volcanos,earthquakes,meteorites):
        self.pyg.start_display(path,volcanos,earthquakes,meteorites)

    def draw_country(self,codes,color=(255,168,0),width=1):
        for code in codes:
            country = self.mh.get_country_poly(code)
            if country is not None:
                break

        if country['type'] == 'MultiPolygon':
            for polygon in country['coordinates']:
                self.pyg.add_polygon(polygon,color,width)
        else:
            self.pyg.add_polygon(country['coordinates'],color,width)


    def draw_airports(self,icon):
        airports = self.mh.get_all('airports')
        points = []
        for ap in airports:
            points.append(ap['geometry']['coordinates'])
        self.pyg.add_points(points,icon)

    def pin_the_map(self,points,icon):
        self.pyg.add_points(points,icon)
    def draw_cord(self,points):
        ad=self.pyg.adjust_cord(points)
        return ad


    def draw_all_countries(self,border=0):
        c  = ColorHelper()
        unique_list = []
        for i in range(14):
            unique_list.append(c.get_unique_random_color())

        
        countries = self.mh.get_all('countries',{},{'_id':0,'properties.MAPCOLOR13':1,'properties.ISO_A3':1,'properties.ADM0_A3_US':1, 'properties.SU_A3':1, 'properties.GU_A3':1})
        for country in countries:
            codes = []
            color = int(country['properties']['MAPCOLOR13'])-1
            for c in ['ISO_A3','ADM0_A3_US','SU_A3','GU_A3']:
                if not str(c) == '-99':
                    codes.append(country['properties'][c])
            if color < 0:
                color = 13
            self.draw_country(codes,unique_list[color],border)

screen_width = 1024
screen_height = 512

if __name__=='__main__':
    path=[]
    volcanos=[]
    earthquakes=[]
    meteorites=[]
    """
    check for all the paramters
    """

    if len(sys.argv) == 4:
        src=sys.argv[1].upper()
        dest=sys.argv[2].upper()
        radius=float(sys.argv[3])
        mh = mongoHelper()
        

        for ap in mh.db_airports.find():
            if ap['properties']['ap_iata']==src:
                s_lon,s_lat=ap['geometry']['coordinates']
                
            if ap['properties']['ap_iata']==dest:
                d_lon,d_lat=ap['geometry']['coordinates']
                
                
        
        path.append([ s_lon,s_lat])
        mh.get_path(path,s_lon,s_lat,d_lon,d_lat,radius)
        path.append([ d_lon,d_lat])
        
        volcanos=mh.get_nearest_volcanos(path,radius)
        earthquakes=mh.get_nearest_earthquake(path,radius)
        meteorites=mh.get_nearest_meteorite(path,radius)
        


        mf = MapFacade(screen_width,screen_height)
        
        path_adjusted=(mf.draw_cord(path))
        volcanos_adjusted=mf.draw_cord(volcanos)
        earthquakes_adjusted=mf.draw_cord(earthquakes)
        meteorites_adjusted=(mf.draw_cord(meteorites))

        mf.pin_the_map(path,map_icon('Centered','Pink',32,''))
        mf.draw_all_countries(1)

       
       


        mf.run(path_adjusted,volcanos_adjusted,earthquakes_adjusted,meteorites_adjusted)

    else:
        print ("invalid number of parameters")   
    