#!/usr/bin/python
#matching_game.py

import sys, os
import math, random
import pygame
from pygame.locals import *

BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
SCREEN_SIZE=[800,400]
FPS=60
WIDTH=130
HEIGHT=61
WAITING_TIME=1000
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

    def __init__(self):
        pygame.init()
        self.window=pygame.display.set_mode(SCREEN_SIZE)
        self.clock=pygame.time.Clock()

        self.score=[0,0]
        self.combo=0
        self.whose_turn=1
        pygame.display.set_caption("MATCHING GAME")

        self.f=pygame.font.match_font('ComicSans',"Arial")
        self.winning_font=pygame.font.Font(self.f,18)

        self.f=pygame.font.match_font("Arial",'ComicSans')
        self.score_font=pygame.font.Font(self.f,18)

        
        self.winning_text1=self.winning_font.render("COMBO: %s" %self.combo,True,BLACK)
        self.winning_text2=self.winning_font.render("Player Turn: %s" %self.whose_turn,True,BLACK)
        self.score_text1=self.score_font.render("Player 1: %s" %self.score[0],True,BLACK)
        self.score_text2=self.score_font.render("Player 2: %s" %self.score[1],True,BLACK)

        self.score_rect1=self.score_text1.get_rect()
        self.score_rect2=self.score_text2.get_rect()
        self.winning_rect1=self.winning_text1.get_rect()
        self.winning_rect2=self.winning_text2.get_rect()
        
        self.score_rect1.centerx = 200
        self.score_rect1.centery = 15

        self.winning_rect1.centerx = 350
        self.winning_rect1.centery = 15

        self.winning_rect2.centerx = 450
        self.winning_rect2.centery = 15

        self.score_rect2.centerx = 600
        self.score_rect2.centery = 15    

        pygame.event.set_allowed([QUIT,MOUSEBUTTONDOWN,MOUSEBUTTONUP])
        
        self.corresponding_position_list=[]
        self.drawBackground()

        self.sprites=pygame.sprite.RenderUpdates()

        self.value_list=[]
        for i in range(0,18,1):
            self.value_list.extend((i,i))
        #print position_list
        #instead of randomizing the position, just randomize the values while keeping position in order

        random.shuffle(self.value_list)
        ctr=-1
        self.card_list=[]

        for pos in range (0,36,1):
            val=(self.value_list[pos])+1
            self.card_list.append(Card(self.corresponding_position_list[pos],"%s.gif"%val,val))
                     
        for card in self.card_list:
            self.sprites.add(card)
        #sound
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
        self.background.fill(GREEN)

        #draw words
        self.background.blit(self.score_text1,self.score_rect1)
        self.background.blit(self.score_text2,self.score_rect2)
        self.background.blit(self.winning_text1,self.winning_rect1)
        self.background.blit(self.winning_text2,self.winning_rect2)

        #draw the blank cards
        self.blank_card=pygame.Surface((WIDTH,HEIGHT))
        self.blank_card.fill(WHITE)

        for x in range(5,788,WIDTH+1):
            for y in range (27,399,HEIGHT+1):
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
                for x in range(5,788,WIDTH+1):
                    for y in range (27,399,HEIGHT+1):
                        if x<=event.pos[0] and event.pos[0]<=x+WIDTH and y<=event.pos[1] and event.pos[1]<=y+HEIGHT:
                            if x<=self.clicked[0] and self.clicked[0]<=x+WIDTH and y<=self.clicked[1] and self.clicked[1]<=y+HEIGHT:
                                if not self.card_list[which_card] in self.sprites:
                                    print "This CARD",self.card_list[which_card]
                                    print "is not in",self.opened_cards
                                    print "ITS NOT HERE"
                                    self.opened_cards.append(self.card_list[which_card])
                                    self.drawCard(which_card)

                                    if len(self.opened_cards)==2:
                                        print "HI"
                                        if self.opened_cards[0].value==self.opened_cards[1].value:
                                            self.correct_sound.play()
                                            self.opened_cards=[]
                                            self.combo+=1
                                            self.score[self.whose_turn-1]+=self.combo
                                            self.winning_text1=self.winning_font.render("COMBO: %s" %self.combo,True,BLACK)
                                            self.score_text1=self.score_font.render("Player 1: %s" %self.score[0],True,BLACK)
                                            self.score_text2=self.score_font.render("Player 2: %s" %self.score[1],True,BLACK)
                                            #add to score,combo
                                            if len(self.sprites)==len(self.card_list):
                                                #compare scores
                                                if self.score[0]>self.score[1]:
                                                    self.winner="Player 1"
                                                elif self.score[0]>self.score[1]:
                                                    self.whose_turn="Player 2"
                                                else:
                                                    self.whose_turn="Everybody!"
                                                self.winning_text1=self.winning_font.render("WINNER:",True,BLACK)
                                                self.winning_text2=self.winning_font.render(self.winner,True,BLACK)
                                        else:
                                            self.wrong_sound.play()
                                            pygame.time.wait(WAITING_TIME)
                                            self.combo=0
                                            self.sprites.remove(self.opened_cards)
                        
                                            self.opened_cards=[]
                                            self.whose_turn=(self.whose_turn%2)+1
                                            print "ITS",self.whose_turn
                                            self.winning_text1=self.winning_font.render("COMBO: %s" %self.combo,True,BLACK)
                                            self.winning_text2=self.winning_font.render("Player Turn: %s" %self.whose_turn,True,BLACK)

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
                #check if position is card
                #if yes, update
                #count number of cards opened
                #if 2, wait 2 seconds then either keep or close
                    #if keep, +to combo and score
                    #if not, next player
        return True
            

if __name__=="__main__":
    game=Game()
    game.run()
