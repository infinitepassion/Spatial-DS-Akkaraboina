"""
Program:
--------
    Program 2 - DBscan.

Description:
------------
    Using Pygame to create a 2D scatterplot of locations of crimes in NYC and output showing all 5 buroughs in different colors and sav the ouput as an image.
    
Name: Manju Yadav Akkaraboina
Date: 19 Jun 2016
"""


import pygame
import random
from dbscan import *
import sys,os
import pprint as pp

pygame.init()



"""
All the  initializations for screen dimensions 

"""
background_colour = (255,255,255)
black = (0,0,0)

if len(sys.argv) == 1:
        width = 1000    # define width and height of screen
        height = 1000
else:
        # use size passed in by user
        width = int(sys.argv[1])
        height = int(sys.argv[2])

#(width, height) = (600, 400)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('All Buroughs NYC')
screen.fill(background_colour)

pygame.display.flip()


points = []
points_temp=[]

#changes are done here
keys = []
crimes = []

def draw(color,filename):
    """
    Opens all the files from in the input files directory
    Retrives each file and then appends creates tuples with (x,y) cordinates
    Each tuple cordinate is rescaled and the y cordinates are inversed
    Then we draw the each buroughs with the specified colors codes provided.


    Args: 
        color: the color of the burough.
        filename: the burough name.

    Returns: None
    
    """
    got_keys = False
    with open(fname) as f:
        for line in f:
            line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
            line = line.strip().split(',')
            if not got_keys:
                keys = line
                #print(keys)
                got_keys = True
                continue
            crimes.append(line)
    for crime in crimes:
    # print(crime[19],crime[20])
        if len(crime[19])==0 or len(crime[20])==0:
            pass
        else :
            x=int(crime[19].strip())
            y=int(crime[20].strip())
            points_temp.append((x,y))

    #xmax,ymax=map(max, zip(*points_temp))
    #xmin,ymin=map(min, zip(*points_temp))

    xmax=1067226
    xmin=913357
    ymax=271820
    ymin=121250
    #print (xmax,ymax,xmin,ymin)
    for p in points_temp:
        x,y=p
        x=int(width*((x-xmin)/(xmax-xmin)))
        #print(x)
        y=int(height*(1-((y-ymin)/(ymax-ymin))))
        # print(y)
        #x=int(x/1000)
        #y=int(y/1000)
        points.append((x,y))    
    # print (x,y)
    running = True
    while running:
        #text = str('Manju Yadav Akkaraboina')
        #font = pygame.font.Font('freesansbold.ttf', 40)
        #text = font.render(text, True, (0,0,0))
        #screen.blit(text, (0, 0))
        for p in points:
            #print (p)
            pygame.draw.circle(screen, color, p, 3, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        running = False
        pygame.display.flip()


#with open(DIRPATH+'/../NYPD_CrimeData/Nypd_Crime_01') as f:

for filename in os.listdir(os.getcwd()+'/files'):
   
    fname=os.getcwd()+'/files/'+filename
    while len(points)>0:
            points.pop()
    while len(points_temp)>0:
            points_temp.pop()
    while len(crimes)>0:
            crimes.pop()
    if filename=='filtered_crimes_bronx.csv':
        color=(2,120,120)
        draw(color,filename)
    elif filename=='filtered_crimes_brooklyn.csv': 
        color=(128,22,56)
        draw(color,filename)
    elif filename=='filtered_crimes_manhattan.csv': 
        color=(194,35,38)
        draw(color,filename)
    elif filename=='filtered_crimes_queens.csv': 
        color=(243,115,56)
        draw(color,filename)
    else:
        color=(253,182,50)
        draw(color,filename)
   
    #fp=open(fname,'r')
    
pygame.image.save(screen, "all_buroughs_screen_shot.png")
