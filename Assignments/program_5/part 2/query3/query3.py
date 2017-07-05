"""
Program:
--------
    Program 5 - Query 3: Clustering

Description:
------------
    Use dbscan to find the top 3-5 clusters of volcanoes, earthquakes, and meteors.

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
from dbscan import *

class clustering(object):
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
    
        self.BASE = os.path.dirname(os.path.realpath(__file__))
        self.screen_width=1024
        self.screen_height=512

    def calculate_mbrs(self,points, epsilon, min_pts):
        """
        Find clusters using DBscan and then create a list of bounding rectangles
        to return.
        """
        mbrs = []
    
        clusters =  dbscan(points, epsilon, min_pts)

        """
        Traditional dictionary iteration to populate mbr list
        Does same as below
        """
        # for id,cpoints in clusters.items():
        #     xs = []
        #     ys = []
        #     for p in cpoints:
        #         xs.append(p[0])
        #         ys.append(p[1])
        #     max_x = max(xs) 
        #     max_y = max(ys)
        #     min_x = min(xs)
        #     min_y = min(ys)
        #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
        # return mbrs

        """
        Using list index value to iterate over the clusters dictionary
        Does same as above
        """
        for id in range(len(clusters)-1):
            xs = []
            ys = []
            for p in clusters[id]:
                xs.append(p[0])
                ys.append(p[1])
            max_x = max(xs) 
            max_y = max(ys)
            min_x = min(xs)
            min_y = min(ys)
            mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
            print (mbrs)
        return mbrs
    
    def get_volcanos(self):
        """
        get all the volcano coordinate points
        """
        volcanos=[]
    
    
        vol_res = self.db_volcano.find()
        
        for  vol in vol_res:
            volcanos.append(vol['geometry']['coordinates'])

        return volcanos   
    
    
    def get_earthquakes(self):
        """
        get all the earthquake coordinate points
        """
        
        earthquakes=[]
       
        eq_res = self.db_earthquakes.find()

        for  eq in eq_res:
            earthquakes.append(eq['geometry']['coordinates'])

        return earthquakes

    def get_meteorites(self):
        
        """
        get all the meteorites coordinate points
        """
        meteorites=[]
        
        met_res = self.db_meteorites.find()

        for  m in met_res:
            meteorites.append(m['geometry']['coordinates'])

        return meteorites

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
        Adjust the volcano/earthquakes/meteorites points
        """
        ad=[]
        for p in points:
            
            lon,lat = p
            x = (self.mercX(lon) / 1024 * self.screen_width)
            scale = 1 / math.cos(math.radians(lat))             # not used
            y = (self.mercY(lat) / 512 * self.screen_height) - (self.screen_height/2)
            ad.append([x,y])
        return ad
    def calculate_mbrs(self,points, epsilon, min_pts):
        """
        Find clusters using DBscan and then create a list of bounding rectangles
        to return.
        """
        mbrs = []
        clusters =  dbscan(points, epsilon, min_pts)

        """
        Traditional dictionary iteration to populate mbr list
        Does same as below
        """
        # for id,cpoints in clusters.items():
        #     xs = []
        #     ys = []
        #     for p in cpoints:
        #         xs.append(p[0])
        #         ys.append(p[1])
        #     max_x = max(xs) 
        #     max_y = max(ys)
        #     min_x = min(xs)
        #     min_y = min(ys)
        #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
        # return mbrs

        """
        Using list index value to iterate over the clusters dictionary
        Does same as above
        """
        for id in range(len(clusters)-1):
            xs = []
            ys = []
            for p in clusters[id]:
                xs.append(p[0])
                ys.append(p[1])
            max_x = max(xs) 
            max_y = max(ys)
            min_x = min(xs)
            min_y = min(ys)
            mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
        return mbrs
    def clean_area(self,screen,origin,width,height,color):
        """
        Prints a color rectangle (typically white) to "erase" an area on the screen.
        Could be used to erase a small area, or the entire screen.
        """
        ox,oy = origin
        points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
        pygame.draw.polygon(screen, color, points, 0)



    def start_display(self,points,eps,min_pts):
            """
            To start the screen
            Input:
            points :volcanos/earthquakes/meteorites points
            eps: epsilon
            min_pts: no of points in a cluster
            """
            background_colour = (255,255,255)
            points_color = (255,0,0)
            mbr_color=(0,255,0)
            (screen_width, screen_height) = (self.screen_width, self.screen_height)

            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption('Query 3 Simple Map')

            bg = pygame.image.load(os.path.join(self.BASE,"1024x512.png"))

            screen = pygame.display.set_mode((screen_width,screen_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
            screen.blit(pygame.transform.scale(bg,(screen_width,screen_height)), (0, 0))

            

            pygame.display.flip()

            
            mbrs=self.calculate_mbrs(points,eps,min_pts)
            sorted(mbrs, key=len) 

            new_mbr=[]

            for x in range(0,5):
                new_mbr.append(mbrs[x])


            running = True
            while running:

                for p in points:
                    x=int(p[0])
                    y=int(p[1])
                    pygame.draw.circle(screen, points_color, [x,y], 1, 0)
                for mbr in new_mbr:
                    pygame.draw.polygon(screen, mbr_color, mbr, 2)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            
                   
                pygame.display.flip()

            
                
              



if __name__=='__main__':

    c=clustering()

    if len(sys.argv)==4:
        feature=sys.argv[1]
        min_pts=int(sys.argv[2])
        eps=float(sys.argv[3])
        if feature=='volcanos':
            volcanos=c.get_volcanos()
            volcanos_adjusted=c.adjust_cord(volcanos)
            c.start_display(volcanos_adjusted,eps,min_pts)
        elif feature=='earthquakes':
            earthquakes=c.get_earthquakes()
            earthquakes_adjusted=c.adjust_cord(earthquakes)
            c.start_display(earthquakes_adjusted,eps,min_pts)
        else:
            meteorites=c.get_meteorites()
            meteorites_adjusted=c.adjust_cord(meteorites)
            c.start_display(meteorites_adjusted,eps,min_pts)
    else:
        print("invalid  number of arguments")







