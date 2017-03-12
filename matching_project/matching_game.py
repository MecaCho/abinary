#-*-coding=UTF-8-*-
#!/usr/bin/python
#matching_game.py

import sys, os
import math, random
import pygame
from pygame.locals import *

BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE = (0,0,255)
GREEN=(0,255,0)
SCREEN_SIZE=[800,600]
FPS=60
WIDTH=100
HEIGHT=100
WAITING_TIME=1000


def drawBoard(board, message, drawp=''):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = self.makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
    DISPLAYSURF.blit(exit1_SURF, exit1_RECT)
    if drawp:
        DISPLAYSURF.blit(next_SURF, next_RECT)
        DISPLAYSURF.blit(exit_SURF, exit_RECT)
class Card(pygame.sprite.Sprite):
    "It's the card to see matching game. Has 2 sides, check em"
    def __init__(self,xy,card_pic,value):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(card_pic)
        self.rect=self.image.get_rect()
        self.value=value
        self.rect.left,self.rect.top=xy
        self.rect.width,self.rect.height=WIDTH,HEIGHT
        self.is_displayed=False

class Game(object):
    "game object, where to show game"
#[2, 5, 0, 1, 4, 2, 6, 6, 5, 7, 0, 3, 3, 7, 4, 1]
    def __init__(self):
        pygame.init()
        self.window=pygame.display.set_mode(SCREEN_SIZE)
        self.clock=pygame.time.Clock()
        pygame.display.set_caption("伏羲")
        self.f=pygame.font.match_font('ComicSans',"Arial")
        self.winning_font=pygame.font.Font(self.f,18)
        pygame.event.set_allowed([QUIT,MOUSEBUTTONDOWN,MOUSEBUTTONUP])
        self.corresponding_position_list=[]
        self.drawBackground()
        self.sprites=pygame.sprite.RenderUpdates()

        self.value_list=[]
        for i in range(0,16,1):
            self.value_list.append(i)
        random.shuffle(self.value_list)
        print self.value_list
        ctr=-1

        self.card_list=[]
        for pos in range (0,16,1):
            val=(self.value_list[pos])+1
            self.card_list.append(Card(self.corresponding_position_list[pos],"%s.gif"%val,val))
        for card in self.card_list:
            self.sprites.add(card)
        self.correct_sound=pygame.mixer.Sound("winner_sound.wav")
        self.wrong_sound=pygame.mixer.Sound("loser_sound.wav")
        #display! the blank cards!
        self.sprites=pygame.sprite.RenderUpdates()
        
    def drawCard(self,position):
        "position is from 0 to 35, V then by >"
        self.sprites.add(self.card_list[position])
        self.sprites.draw(self.background)
        self.window.blit(self.background,(0,0))
        pygame.display.flip()

    def drawCards(self):
        self.sprites.draw(self.background)
        self.window.blit(self.background,(0,0))
        pygame.display.flip()
        
    def drawBackground(self):
        self.background=pygame.Surface(SCREEN_SIZE)
        self.background.fill(BLUE)
        self.bagua_image = pygame.image.load('bagua.png')
        self.background.blit(self.bagua_image,(0,0))
        #draw the blank cards
        self.blank_card=pygame.Surface((WIDTH,HEIGHT))
        self.blank_card.fill(GREEN)
        for x in range(200,600,WIDTH+1):
            for y in range (100,500,HEIGHT+1):
                self.corresponding_position_list.append((x,y))
                self.background.blit(self.blank_card,(x,y))
        self.window.blit(self.background,(0,0))
        pygame.display.flip()
    def run(self):
        "runs the game"
        print "starting"
        running =True
        #game will only change if event happens
        self.clicked=(-1,-1)
        self.opened_cards=[]
        while running:
            running=self.handleEvents()
        print "QUITTING"
        pygame.quit()
        sys.exit()
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                print event.pos
                self.clicked=event.pos
                #store position
            elif event.type==pygame.MOUSEBUTTONUP:
				#check which card is clicked
                which_card=0
                for x in range(200,600,WIDTH+1):
                    for y in range (100,500,HEIGHT+1):
                        if x<=event.pos[0] and event.pos[0]<=x+WIDTH and y<=event.pos[1] and event.pos[1]<=y+HEIGHT:
                            if x<=self.clicked[0] and self.clicked[0]<=x+WIDTH and y<=self.clicked[1] and self.clicked[1]<=y+HEIGHT:
                                if not self.card_list[which_card] in self.sprites:
                                    self.opened_cards.append(self.card_list[which_card])
                                    self.drawCard(which_card)
                                    if len(self.opened_cards)==2:
                                        if self.opened_cards[0].value%8==self.opened_cards[1].value%8:
                                            self.correct_sound.play()
                                            self.opened_cards=[]
                                            if len(self.sprites)==len(self.card_list):
                                                self.winning_text1=self.winning_font.render("WIN",True,BLACK)
                                        else:
                                            self.wrong_sound.play()
                                            pygame.time.wait(WAITING_TIME)
                                            self.combo=0
                                            self.sprites.remove(self.opened_cards)
                                            self.opened_cards=[]
                                            #change player turn, flip cards again, remove from update
                                        self.drawBackground()
                                        self.drawCards()
                                else:
                                    print "HI, something bad is happenind"
                                    
                            else:
                                which_card+=1
                        else:
                            which_card+=1
                self.clicked=(-1,-1)
        return True
            

if __name__=="__main__":
    game=Game()
    game.run()
