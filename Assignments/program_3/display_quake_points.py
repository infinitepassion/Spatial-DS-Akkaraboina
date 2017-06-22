

import pygame
import sys,os,time
import json
import mbrs

pygame.init()
epsilon = 3
min_pts = 5.0
mbr=[]
def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

def display():

    """
    This function takes all the adjusted points and then displays the earth quake data on the world map with a 1 sec delay for each year ranging from 1960-2017 with a min magnitude of 7
    """
    mbr=[]
    new_mbr=[]
    background_colour = (255,255,255)
    color = (255,0,0)
    (width, height) = (1024, 512)
    bg = pygame.image.load("Z:\\MS\MWSU\\Summer 1 2017\\program_3\\image.png")
    all_points=[]
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MBRs')
    screen.fill(background_colour)
    wait_check=0
    pygame.display.flip()
    for filename in os.listdir(os.getcwd()):
        screen.blit(bg, (0, 0))
        if filename.endswith("-adjusted.json"):
            f = open(filename,'r')
            points = json.loads(f.read())
            #print(filename)
            #print(len(points))
            for p in points:
                all_points.append(p)
            if wait_check==1:
                time.sleep(1)
            else:
                wait_check=1
            
            """
            The screen is refreshed with each year from here
            """
            running = True
            while running:
                print (filename)
                for p in all_points:
                    pygame.draw.circle(screen, color, p, 1,0)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pass
                        
                if filename=='quake-2017-adjusted.json':
                    #mbr = mbrs.calculate_mbrs(all_points, epsilon, min_pts)
                    pygame.image.save(screen, "screen_shot.png")
                else:
                    #mbr = mbrs.calculate_mbrs(all_points, epsilon, min_pts)
                    running=False
                pygame.display.flip()
            