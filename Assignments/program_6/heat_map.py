"""
Program:
--------
    Program 5 - Heat Map

Description:
------------
    Generate a heat style map showing terrorist hotspots around the world.

Name: Manju Yadav Akkaraboina
Date: 07 JUL 2017
"""



import pygame
import json
import pprint as pp
import os,sys,time
import math
from math import radians, cos, sin, asin, sqrt

import time


class Heat_Map(object):
    """
     This class has all the heat map related methods
    """

    def __init__(self):
        
        """
        This is used to initialize all the parameters

        Input:
            None
        """
       
        
        self.screen_height=512
        self.screen_width=1024

        self.colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)] 
        self.interval=30
        self. color=[]
        self.range_band=[]
        self.city_color_key = []
        self.radius_range = []
        self.radius_key = []
        self.EPSILON = sys.float_info.epsilon 
    
    def mercX(self,lon,zoom = 1):
        """
        To adjust the lon for the coordinates

        Input:
            lon:longitude
        """
        lon = math.radians(lon)
        a = (256 / math.pi) * pow(2, zoom)
        b = lon + math.pi
        return int(a * b)

    def mercY(self,lat,zoom = 1):
        """
        To adjust the lat for the coordinates

        Input:
            lat:latitude
        """
        lat = math.radians(lat)
        a = (256.0 / math.pi) * pow(2, zoom)
        b = math.tan(math.pi / 4 + lat / 2)
        c = math.pi - math.log(b)
        return int(a * c)   

    def adjust_cord(self,points):
        """
        Adjust the volcano/earthquakes/meteorites points

        Input:
            points: coordinates list

        """
        ad=[]
        for p in points:
            
            lon,lat = p
            x = (self.mercX(lon) / 1024 * self.screen_width)
            scale = 1 / math.cos(math.radians(lat))             # not used
            y = (self.mercY(lat) / 512 * self.screen_height) - (self.screen_height/2)
            ad.append([x,y])
        return ad
    
    def calculateColor(self,cmin,cmax):

        """
        To calculate the intensity

        Input:
            cmin: count of minimum numner of attacks for cities
            cmax: count of maximum numner of attacks for cities
        """
        change_factor=float(cmax-cmin) / self.interval
       
        for i in range(self.interval+1):
            val = cmin + i*change_factor
            r, g, b = self.convert_to_rgb(cmin, cmax, val, self.colors)
            self.range_band.append(val)
            self.color.append((r,g,b))

    def convert_to_rgb(self,cmin, cmax, val, colors):

        """
        To assign color to the pixels.

        Input:
            cmin: count of minimum numner of attacks for cities
            cmax: count of maximum numner of attacks for cities
            val: change factor calculation
            colors: colors

        """


        fi = float(val-cmin) / float(cmax-cmin) * (len(colors)-1)
        i = int(fi)
        f = fi - i
        if f < self.EPSILON:
            return colors[i]
        else:
            (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
            return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))


    def calculateBand(self,city_coord_adjusted,city_cnt):

        """
        To calculate the intensity of the pixel.

        Input:
            city_coord_adjusted: adjusted city geometry points.
            city_cnt: the number of attacks in the cities.
        """

        for i in range (len(self.range_band)):
            self.radius_range.append(i+1)
    
        for i in range (len(city_coord_adjusted)):
            for j in range (len(self.range_band)-1):
                if city_cnt[i] >= self.range_band[j] and city_cnt[i] < self.range_band[j+1]:     
                    self.city_color_key.append(self.color[j])
                    self.radius_key.append(self.radius_range[j])

    def display(self,city_coord_adjusted):
        """
        To start the screen and display.
        
        Input:
            city_coord_adjusted: adjusted city geometry points.

        """
        screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption('Terrorism Heat Map by City')
        image=os.getcwd()+"/1024x512.png"
        bg = pygame.image.load (image)
        pygame.display.flip()

        running = True
        while running:

            screen.blit(bg, (0, 0))

            for i in range (len(city_coord_adjusted)):
                x,y = city_coord_adjusted[i]
                pygame.draw.circle(screen, self.city_color_key[i], (int(x), int(y)), self.radius_key[i],int(self.radius_key[i]))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()        
if __name__=='__main__':
    
    #main method
    hm=Heat_Map()
    path=os.getcwd()+"/attacks.JSON"

    f=open (path,"r")

    data=f.read()

    #pp.pprint(data)
    city_cnt=[]
    city_coord=[]

    data=json.loads(data)


    for key,values in data.items():
        for k,v in values.items():
            city_cnt.append(v['count'])
            city_coord.append(v['geometry']['coordinates'])
    cnt_min=min(city_cnt)
    cnt_max=max(city_cnt)

    # print (city_cnt)
    # print(city_coord)
    city_coord_adjusted=[]
    city_coord_adjusted=hm.adjust_cord(city_coord)

    #print (city_coord_adjusted)

    hm.calculateColor(cnt_min,cnt_max)
    hm.range_band.append(cnt_max+1)

    hm.calculateBand(city_coord_adjusted,city_cnt)

    hm.display(city_coord_adjusted)

    


