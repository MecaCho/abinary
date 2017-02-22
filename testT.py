#-*-coding=UTF-8-*-
import pygame
import time
import sys
from pygame.color import THECOLORS

class background(pygame.sprite.Sprite):
    def __init__(self,filename,inittial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect  = self.image.get_rect()
        self.rect.bottomright = inittial_position

bg_location = ([500,300],[500,200],[500,100])
bg_Group = pygame.sprite.Group()
bg_Group.add(background('exit.png',bg_location[0]))
bg_Group.add(background('help.png',bg_location[1]))
bg_Group.add(background('knowcard.png',bg_location[2]))


screenCaption = pygame.display.set_caption('Fuhsi')
screen = pygame.display.set_mode([600,400])
screen.fill([255,255,255])
pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)

for bg in bg_Group.sprites():
    screen.blit(bg.image,bg.rect)
print time.ctime()
print time.clock()
print pygame.time.Clock()

pygame.display.flip()
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            print event.pos
            clickxy = event.pos
        elif event.type==pygame.MOUSEBUTTONUP:
            if clickxy[0]<

