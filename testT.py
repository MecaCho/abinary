#-*-coding=UTF-8-*-
import pygame
import time
import sys
from pygame.color import THECOLORS
screenCaption = pygame.display.set_caption('Fuhsi')
screen = pygame.display.set_mode([600,400])
screen.fill([255,255,255])
pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)
print time.ctime()
print time.clock()
print pygame.time.Clock()
pygame.display.flip()
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()