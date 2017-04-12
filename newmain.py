#-*-coding=UTF-8-*-
import sys
import time
import random
import pygame
from pygame.locals import *
reload(sys)
sys.setdefaultencoding('utf-8')

tile_size = 100
window_width = 800
window_height = 600
screen_size = [window_width,window_height]
s_width = 100
s_height = 100
waiting_time = 1000

fps_ = 30
blank_ = None

black = (0,0,0)
white = (255,255,255)
bright_blue = (0,50,255)
green = (0,204,0)
blue = (0,0,240)

bg_color = blue
title_color = green
text_color = white
border_color = bright_blue

basicfontsize = 28
basicfont = pygame.font.Font("gkai00mp.ttf",basicfontsize)

pygame.mixer.init()
bg_sound = pygame.mixer.Sound("plant.wav")
slide_sound = pygame.mixer.Sound("")

display_surf = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption(u'伏羲')

if __name__ == '__main__':


