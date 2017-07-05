

import pygame
import sys,os,time


pygame.init()

def display(points):

    """
    This function takes all the adjusted points and then displays the earth quake data on the world map with a 1 sec delay for each year ranging from 1960-2017 with a min magnitude of 7
    """
    background_colour = (255,255,255)
    color = (148,204,0)
    (width, height) = (1024, 512)
    bg = pygame.image.load("Z:\\MS\MWSU\\Summer 1 2017\\program_5\\image.png")
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Query1')
    screen.fill(background_colour)
    pygame.display.flip()
    screen.blit(bg, (0, 0))
    while len(points)>1:
        pygame.draw.line(screen, (76, 153, 0), points[0],points[1])
        points.pop(0)
    pygame.image.save(screen, "screen_shot.png")
    
    
    

   