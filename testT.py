#-*-coding=UTF-8-*-
import pygame
import random
import time
import sys
import pygame, sys, random
from pygame.locals import *
reload(sys)
sys.setdefaultencoding('utf-8')

# Create the constants (go ahead and experiment with different values)
TILESIZE = 100
WINDOWWIDTH = 600
WINDOWHEIGHT = 500
FPS = 30
BLANK = None

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
BLUE =          (0,0,240)

BGCOLOR = BLUE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 28

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

pygame.mixer.init()
bg_sound=pygame.mixer.Sound("plant.wav")



UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
pygame.init()
BASICFONT = pygame.font.Font('gkai00mp.ttf', BASICFONTSIZE)

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(u'伏羲')

DISPLAYSURF.fill([255,255,255])
#pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)
background = pygame.Surface([600,500])
background.fill([0,0,255])
DISPLAYSURF.blit(background,(0,0))

class background(pygame.sprite.Sprite):
    def __init__(self,filename,inittial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect  = self.image.get_rect()
        self.rect.bottomright = inittial_position

tip_location = ([100,64],[210,64],[300,500],[410,500],[200,33],[310,33])
tip_Group = pygame.sprite.Group()
tip_Group.add(background('next.png',tip_location[4]))
tip_Group.add(background('reback.png',tip_location[5]))


DISPLAYSURF.blit(tip_Group.sprites()[0].image, tip_Group.sprites()[0].rect)
DISPLAYSURF.blit(tip_Group.sprites()[1].image, tip_Group.sprites()[1].rect)


SCREEN_SIZE = [WINDOWWIDTH,WINDOWHEIGHT]
WIDTH = 90
HEIGHT = 90
WAITING_TIME = 1000


class Card(pygame.sprite.Sprite):
    "It's the card to see matching game. Has 2 sides, check em"

    def __init__(self, xy, card_pic, value):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(card_pic)
        self.rect = self.image.get_rect()

        self.value = value
        self.rect.left, self.rect.top = xy
        self.rect.width, self.rect.height = WIDTH, HEIGHT
        self.is_displayed = False


class match_g(object):
    "game object, where to show game"

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        self.score = [0, 0]
        self.combo = 0
        self.whose_turn = 1
        ####################窗口标题
        pygame.display.set_caption("FuHsi")

        self.f = pygame.font.match_font('ComicSans', "Arial")
        self.winning_font = pygame.font.Font(self.f, 18)

        self.f = pygame.font.match_font("Arial", 'ComicSans')
        self.score_font = pygame.font.Font(self.f, 18)

        self.winning_text1 = self.winning_font.render("COMBO: %s" % self.combo, True, BLACK)
        self.winning_text2 = self.winning_font.render("Player Turn: %s" % self.whose_turn, True, BLACK)
        self.score_text1 = self.score_font.render("Player 1: %s" % self.score[0], True, BLACK)
        self.score_text2 = self.score_font.render("Player 2: %s" % self.score[1], True, BLACK)

        self.score_rect1 = self.score_text1.get_rect()
        self.score_rect2 = self.score_text2.get_rect()
        self.winning_rect1 = self.winning_text1.get_rect()
        self.winning_rect2 = self.winning_text2.get_rect()

        self.score_rect1.centerx = 200
        self.score_rect1.centery = 15

        self.winning_rect1.centerx = 350
        self.winning_rect1.centery = 15

        self.winning_rect2.centerx = 450
        self.winning_rect2.centery = 15

        self.score_rect2.centerx = 600
        self.score_rect2.centery = 15

        pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

        self.corresponding_position_list = []
        self.drawBackground()

        self.sprites = pygame.sprite.RenderUpdates()

        self.value_list = []
        for i in range(0, 18, 1):
            self.value_list.extend((i, i))
        # print position_list
        # instead of randomizing the position, just randomize the values while keeping position in order

        random.shuffle(self.value_list)
        ###################################################################################
        print self.value_list
        ctr = -1
        self.card_list = []

        for pos in range(0, 36, 1):
            val = (self.value_list[pos]) + 1
            self.card_list.append(Card(self.corresponding_position_list[pos], "%s.gif" % val, val))
        ##########################################################################
        print self.card_list
        for card in self.card_list:
            self.sprites.add(card)
        # sound
        self.correct_sound = pygame.mixer.Sound("winner_sound.wav")
        self.wrong_sound = pygame.mixer.Sound("loser_sound.wav")

        # display! the blank cards!
        self.sprites = pygame.sprite.RenderUpdates()

    def drawCard(self, position):
        "position is from 0 to 35, V then by >"
        self.sprites.add(self.card_list[position])
        self.sprites.draw(self.background)
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

    def drawCards(self):
        self.sprites.draw(self.background)
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

    def drawBackground(self):
        self.background = pygame.Surface(SCREEN_SIZE)
        self.background.fill(GREEN)

        # draw words
        self.background.blit(self.score_text1, self.score_rect1)
        self.background.blit(self.score_text2, self.score_rect2)
        self.background.blit(self.winning_text1, self.winning_rect1)
        self.background.blit(self.winning_text2, self.winning_rect2)

        # draw the blank cards
        self.blank_card = pygame.Surface((WIDTH, HEIGHT))
        self.blank_card.fill(WHITE)

        for x in range(5, 788, WIDTH + 1):
            for y in range(27, 399, HEIGHT + 1):
                self.corresponding_position_list.append((x, y))
                self.background.blit(self.blank_card, (x, y))

        self.window.blit(self.background, (0, 0))

        pygame.display.flip()

    def run(self):
        "runs the game"
        print "starting"

        running = True

        # game will only change if event happens
        self.clicked = (-1, -1)
        self.opened_cards = []
        while running:
            running = self.handleEvents()

        print "QUITTING"
        pygame.quit()
        sys.exit()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print event.pos
                self.clicked = event.pos
                # store position
            elif event.type == pygame.MOUSEBUTTONUP:

                # check which card is clicked
                which_card = 0
                for x in range(5, 788, WIDTH + 1):
                    for y in range(27, 399, HEIGHT + 1):
                        if x <= event.pos[0] and event.pos[0] <= x + WIDTH and y <= event.pos[1] and event.pos[
                            1] <= y + HEIGHT:
                            if x <= self.clicked[0] and self.clicked[0] <= x + WIDTH and y <= self.clicked[1] and \
                                            self.clicked[1] <= y + HEIGHT:
                                if not self.card_list[which_card] in self.sprites:
                                    print "This CARD", self.card_list[which_card]
                                    print "is not in", self.opened_cards
                                    print "ITS NOT HERE"
                                    self.opened_cards.append(self.card_list[which_card])
                                    self.drawCard(which_card)

                                    if len(self.opened_cards) == 2:
                                        print "HI"
                                        if self.opened_cards[0].value % 9 == self.opened_cards[1].value % 9:
                                            self.correct_sound.play()
                                            self.opened_cards = []
                                            self.combo += 1
                                            self.score[self.whose_turn - 1] += self.combo
                                            self.winning_text1 = self.winning_font.render("COMBO: %s" % self.combo,
                                                                                          True, BLACK)
                                            self.score_text1 = self.score_font.render("Player 1: %s" % self.score[0],
                                                                                      True, BLACK)
                                            self.score_text2 = self.score_font.render("Player 2: %s" % self.score[1],
                                                                                      True, BLACK)
                                            # add to score,combo
                                            if len(self.sprites) == len(self.card_list):
                                                # compare scores
                                                if self.score[0] > self.score[1]:
                                                    self.winner = "Player 1"
                                                elif self.score[0] > self.score[1]:
                                                    self.whose_turn = "Player 2"
                                                else:
                                                    self.whose_turn = "Everybody!"
                                                self.winning_text1 = self.winning_font.render("WINNER:", True, BLACK)
                                                self.winning_text2 = self.winning_font.render(self.winner, True, BLACK)
                                        else:
                                            self.wrong_sound.play()
                                            pygame.time.wait(WAITING_TIME)
                                            self.combo = 0
                                            self.sprites.remove(self.opened_cards)

                                            self.opened_cards = []
                                            self.whose_turn = (self.whose_turn % 2) + 1
                                            print "ITS", self.whose_turn
                                            self.winning_text1 = self.winning_font.render("COMBO: %s" % self.combo,
                                                                                          True, BLACK)
                                            self.winning_text2 = self.winning_font.render(
                                                "Player Turn: %s" % self.whose_turn, True, BLACK)

                                            # change player turn, flip cards again, remove from update
                                        self.drawBackground()
                                        self.drawCards()
                                else:
                                    print "HI, something bad is happenind"

                            else:
                                which_card += 1
                        else:
                            which_card += 1

                self.clicked = (-1, -1)
                # check if position is card
                # if yes, update
                # count number of cards opened
                # if 2, wait 2 seconds then either keep or close
                # if keep, +to combo and score
                # if not, next player
        return True

class slide_g(object):
    def __init__(self,BOARDHEIGHT=2,BOARDWIDTH=2):
        self.bw = BOARDWIDTH
        self.bh = BOARDHEIGHT
        self.XMARGIN = int((WINDOWWIDTH - (TILESIZE * self.bw + (self.bw - 1))) / 2)
        self.YMARGIN = int((WINDOWHEIGHT - (TILESIZE * self.bh + (self.bh - 1))) / 2)

    def main(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, next_SURF, next_RECT,exit_SURF, exit_RECT, exit1_SURF, exit1_RECT

        # Store the option buttons and their rectangles in OPTIONS.
        RESET_SURF, RESET_RECT = self.makeText(u'设置',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 90)
        NEW_SURF,   NEW_RECT   = self.makeText(u'新游戏', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 60)
        SOLVE_SURF, SOLVE_RECT = self.makeText(u'破解',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 30)
        exit1_SURF, exit1_RECT = self.makeText(u'退出', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 120)
        next_SURF, next_RECT = self.makeText(u'继续', TEXTCOLOR, TILECOLOR, 100, 0)
        exit_SURF, exit_RECT = self.makeText(u'返回', TEXTCOLOR, TILECOLOR, 200, 0)

        mainBoard, solutionSeq = self.generateNewPuzzle(20)
        SOLVEDBOARD = self.getStartingBoard() # a solved board is the same as the board in a start state.
        allMoves = [] # list of moves made from the solved configuration

        while True: # main game loop
            slideTo = None # the direction, if any, a tile should slide
            msg = u'点击数字或按下键盘的上下左右键滑动数字' # contains the message to show in the upper left corner.
            drawp = ''
            if mainBoard == SOLVEDBOARD:
                msg = u'成功!'
                #print u'成功',self.bw
                drawp = 'true'
                if self.bw == 4:
                    msg = u'恭喜你，通过第二关'
                    drawp = ''
                #self.drawBoard(mainBoard, msg)
                #DISPLAYSURF.blit(tip_Group.sprites()[0].image,tip_Group.sprites()[0].rect)
                #DISPLAYSURF.blit(tip_Group.sprites()[1].image, tip_Group.sprites()[1].rect)
                #pygame.display.flip()
                #pygame.display.update()
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        self.clickxy = event.pos
                    if event.type == MOUSEBUTTONUP:
                        if self.clickxy[0]<200 and self.clickxy[1]<34 and self.clickxy[0]>100 and self.clickxy[1]>0:
                            rank = self.bw + 1
                            newgame = slide_g(BOARDWIDTH=rank,BOARDHEIGHT=rank)
                            if rank < 5:
                                newgame.main()
                            else:
                                msg = u'恭喜你，通过第二关'
                        elif self.clickxy[0]<300 and self.clickxy[1]<34 and self.clickxy[0]>200 and self.clickxy[1]>0:
                            return
                #return True


            self.drawBoard(mainBoard, msg,drawp)

            self.checkForQuit()
            for event in pygame.event.get(): # event handling loop
                if event.type == MOUSEBUTTONUP:
                    spotx, spoty = self.getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                    if (spotx, spoty) == (None, None):
                        # check if the user clicked on an option button
                        if RESET_RECT.collidepoint(event.pos):
                            self.resetAnimation(mainBoard, allMoves) # clicked on Reset button
                            allMoves = []
                        elif NEW_RECT.collidepoint(event.pos):
                            mainBoard, solutionSeq = self.generateNewPuzzle(80) # clicked on New Game button
                            allMoves = []
                        elif SOLVE_RECT.collidepoint(event.pos):
                            self.resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
                            allMoves = []
                        elif exit1_RECT.collidepoint(event.pos):
                            return
                        elif exit_RECT.collidepoint(event.pos):
                            return
                    else:
                        # check if the clicked tile was next to the blank spot

                        blankx, blanky = self.getBlankPosition(mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            slideTo = LEFT
                        elif spotx == blankx - 1 and spoty == blanky:
                            slideTo = RIGHT
                        elif spotx == blankx and spoty == blanky + 1:
                            slideTo = UP
                        elif spotx == blankx and spoty == blanky - 1:
                            slideTo = DOWN

                elif event.type == KEYUP:
                    # check if the user pressed a key to slide a tile
                    if event.key in (K_LEFT, K_a) and self.isValidMove(mainBoard, LEFT):
                        slideTo = LEFT
                    elif event.key in (K_RIGHT, K_d) and self.isValidMove(mainBoard, RIGHT):
                        slideTo = RIGHT
                    elif event.key in (K_UP, K_w) and self.isValidMove(mainBoard, UP):
                        slideTo = UP
                    elif event.key in (K_DOWN, K_s) and self.isValidMove(mainBoard, DOWN):
                        slideTo = DOWN

            if slideTo:
                self.slideAnimation(mainBoard, slideTo, u'点击数字或按上下左右键移动数字', 8) # show slide on screen
                self.makeMove(mainBoard, slideTo)
                allMoves.append(slideTo) # record the slide
            pygame.display.update()
            FPSCLOCK.tick(FPS)


    def terminate(self):
        pygame.quit()
        sys.exit()


    def checkForQuit(self):
        for event in pygame.event.get(QUIT): # get all the QUIT events
            self.terminate() # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP): # get all the KEYUP events
            if event.key == K_ESCAPE:
                self.terminate() # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event) # put the other KEYUP event objects back

    def format_bin(self,number_, bw):
        bin_num = bin(number_).replace('0b', '')
        if len(bin_num) != bw:
            bin_num = (bw - len(bin_num)) * '0' + bin_num
        return bin_num
    def getStartingBoard(self):
        # Return a board data structure with tiles in the solved state.
        # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
        # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
        counter = 1
        board = []
        counter1 = self.format_bin(counter,self.bw)
        for x in range(self.bw):
            column = []
            for y in range(self.bh):
                column.append(counter1)
                counter += self.bw
                counter1 = self.format_bin(counter, self.bw)
            board.append(column)
            counter -= self.bw * (self.bh - 1) + self.bw - 1
            counter1 = self.format_bin(counter, self.bw)

        board[self.bw-1][self.bh-1] = BLANK
        print board
        return board


    def getBlankPosition(self,board):
        # Return the x and y of board coordinates of the blank space.
        for x in range(self.bw):
            for y in range(self.bh):
                if board[x][y] == BLANK:
                    return (x, y)


    def makeMove(self,board, move):
        # This function does not check if the move is valid.
        blankx, blanky = self.getBlankPosition(board)

        if move == UP:
            board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
        elif move == DOWN:
            board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
        elif move == LEFT:
            board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
        elif move == RIGHT:
            board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


    def isValidMove(self,board, move):
        blankx, blanky = self.getBlankPosition(board)
        return (move == UP and blanky != len(board[0]) - 1) or \
               (move == DOWN and blanky != 0) or \
               (move == LEFT and blankx != len(board) - 1) or \
               (move == RIGHT and blankx != 0)


    def getRandomMove(self,board, lastMove=None):
        # start with a full list of all four moves
        validMoves = [UP, DOWN, LEFT, RIGHT]

        # remove moves from the list as they are disqualified
        if lastMove == UP or not self.isValidMove(board, DOWN):
            validMoves.remove(DOWN)
        if lastMove == DOWN or not self.isValidMove(board, UP):
            validMoves.remove(UP)
        if lastMove == LEFT or not self.isValidMove(board, RIGHT):
            validMoves.remove(RIGHT)
        if lastMove == RIGHT or not self.isValidMove(board, LEFT):
            validMoves.remove(LEFT)

        # return a random move from the list of remaining moves
        return random.choice(validMoves)


    def getLeftTopOfTile(self,tileX, tileY):
        left = self.XMARGIN + (tileX * TILESIZE) + (tileX - 1)
        top = self.YMARGIN + (tileY * TILESIZE) + (tileY - 1)
        return (left, top)


    def getSpotClicked(self,board, x, y):
        # from the x & y pixel coordinates, get the x & y board coordinates
        for tileX in range(len(board)):
            for tileY in range(len(board[0])):
                left, top = self.getLeftTopOfTile(tileX, tileY)
                tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
                if tileRect.collidepoint(x, y):
                    return (tileX, tileY)
        return (None, None)


    def drawTile(self,tilex, tiley, number, adjx=0, adjy=0):
        # draw a tile at board coordinates tilex and tiley, optionally a few
        # pixels over (determined by adjx and adjy)
        left, top = self.getLeftTopOfTile(tilex, tiley)
        pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
        textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
        DISPLAYSURF.blit(textSurf, textRect)


    def makeText(self,text, color, bgcolor, top, left):
        # create the Surface and Rect objects for some text.
        textSurf = BASICFONT.render(text, True, color, bgcolor)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)


    def drawBoard(self,board, message,drawp=''):
        DISPLAYSURF.fill(BGCOLOR)
        if message:
            textSurf, textRect = self.makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
            DISPLAYSURF.blit(textSurf, textRect)


        for tilex in range(len(board)):
            for tiley in range(len(board[0])):
                if board[tilex][tiley]:
                    self.drawTile(tilex, tiley, board[tilex][tiley])

        left, top = self.getLeftTopOfTile(0, 0)
        width = self.bw * TILESIZE
        height = self.bh * TILESIZE
        pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

        DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
        DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
        DISPLAYSURF.blit(exit1_SURF, exit1_RECT)
        if drawp:
            DISPLAYSURF.blit(next_SURF, next_RECT)
            DISPLAYSURF.blit(exit_SURF, exit_RECT)


    def slideAnimation(self,board, direction, message, animationSpeed):
        # Note: This function does not check if the move is valid.

        blankx, blanky = self.getBlankPosition(board)
        if direction == UP:
            movex = blankx
            movey = blanky + 1
        elif direction == DOWN:
            movex = blankx
            movey = blanky - 1
        elif direction == LEFT:
            movex = blankx + 1
            movey = blanky
        elif direction == RIGHT:
            movex = blankx - 1
            movey = blanky

        # prepare the base surface
        self.drawBoard(board, message)
        baseSurf = DISPLAYSURF.copy()
        # draw a blank space over the moving tile on the baseSurf Surface.
        moveLeft, moveTop = self.getLeftTopOfTile(movex, movey)
        pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

        for i in range(0, TILESIZE, animationSpeed):
            # animate the tile sliding over
            self.checkForQuit()
            DISPLAYSURF.blit(baseSurf, (0, 0))
            if direction == UP:
                self.drawTile(movex, movey, board[movex][movey], 0, -i)
            if direction == DOWN:
                self.drawTile(movex, movey, board[movex][movey], 0, i)
            if direction == LEFT:
                self.drawTile(movex, movey, board[movex][movey], -i, 0)
            if direction == RIGHT:
                self.drawTile(movex, movey, board[movex][movey], i, 0)

            pygame.display.update()
            FPSCLOCK.tick(FPS)


    def generateNewPuzzle(self,numSlides):
        # From a starting configuration, make numSlides number of moves (and
        # animate these moves).
        sequence = []
        board = self.getStartingBoard()
        self.drawBoard(board, '')
        pygame.display.update()
        pygame.time.wait(500) # pause 500 milliseconds for effect
        lastMove = None
        for i in range(numSlides):
            move = self.getRandomMove(board, lastMove)
            self.slideAnimation(board, move, u'游戏初始化......', animationSpeed=int(TILESIZE / 3))
            self.makeMove(board, move)
            sequence.append(move)
            lastMove = move
        return (board, sequence)


    def resetAnimation(self,board, allMoves):
        # make all of the moves in allMoves in reverse.
        revAllMoves = allMoves[:] # gets a copy of the list
        revAllMoves.reverse()

        for move in revAllMoves:
            if move == UP:
                oppositeMove = DOWN
            elif move == DOWN:
                oppositeMove = UP
            elif move == RIGHT:
                oppositeMove = LEFT
            elif move == LEFT:
                oppositeMove = RIGHT
            self.slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
            self.makeMove(board, oppositeMove)




def startFlash():
    start0 = pygame.image.load("start0.jpeg").convert_alpha()
    start1 = pygame.image.load("start1.jpg").convert_alpha()
    '''start_location = [100,100]
    stbg_Group = pygame.sprite.Group()
    stbg_Group.add(background('exit.png', start_location))
    stbg_Group.add(background('reback.png', start_location))
    #stbg_Group.add(background('start2.png', start_location))
    for sf in stbg_Group.sprites():
        time.sleep(3)
        DISPLAYSURF.blit(sf.image,sf.rect)'''
    DISPLAYSURF.blit(start0, (0,0))
    pygame.display.flip()
    pygame.display.update()


def start0():
    start0 = pygame.image.load("start0.jpeg").convert_alpha()
    DISPLAYSURF.blit(start0, (0, 0))
    pygame.display.flip()
    pygame.display.update()
    start_board()

    #DISPLAYSURF.blit(start1, (0, 0))
    #time.sleep(3)
    #pygame.display.flip()
    #pygame.display.update()

def show_help(filename='1.png',imagelocation=[100,100]):
    print 'True'
    imagep = pygame.image.load(filename)
    rect = imagep.get_rect()
    rect.bottomright = imagelocation
    screen.blit(imagep,rect)

def start_board():
    bg_location = ([600,34],[600,69],[150,34],[600,500],[100,34],[200,34],[175,68],[150,103],[170,136])
    bg_Group = pygame.sprite.Group()
    bg_Group.add(background('help.png',bg_location[0]))
    bg_Group.add(background('know.png',bg_location[1]))
    bg_Group.add(background('game1.png',bg_location[2]))
    bg_Group.add(background('exit.png',bg_location[3]))
    bg_Group.add(background('game2.png', bg_location[6]))
    bg_Group.add(background('game3.png', bg_location[7]))
    bg_Group.add(background('game4.png', bg_location[8]))
    #bg_Group.add(background('next.png',bg_location[4]))
    #bg_Group.add(background('reback.png',bg_location[5]))



    for bg in bg_Group.sprites():
        DISPLAYSURF.blit(bg.image,bg.rect)

    pygame.display.flip()
    pygame.display.update()
startFlash()
start_board()
rank = 2
bg_sound.play(loops=3)
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            print event.pos
            clickxy = event.pos
        elif event.type==pygame.MOUSEBUTTONUP:
            if clickxy[0]<100 and clickxy[1]<34 and clickxy[0]>0 and clickxy[1]>0:
                slide = slide_g(BOARDHEIGHT=rank,BOARDWIDTH=rank)
                slide.main()
                startFlash()
                start_board()
            elif clickxy[0] < 100 and clickxy[1] < 68 and clickxy[0] > 0 and clickxy[1] > 34:
                slide = slide_g(BOARDHEIGHT=rank, BOARDWIDTH=rank)
                slide.main()
                startFlash()
                start_board()
            elif clickxy[0] < 100 and clickxy[1] < 102 and clickxy[0] > 0 and clickxy[1] > 68:
                slide = slide_g(BOARDHEIGHT=rank, BOARDWIDTH=rank)
                slide.main()
                startFlash()
                start_board()
            elif clickxy[0] < 100 and clickxy[1] < 136 and clickxy[0] > 0 and clickxy[1] > 102:
                slide = slide_g(BOARDHEIGHT=rank, BOARDWIDTH=rank)
                slide.main()
                startFlash()
                start_board()
                    #rank += 1
                #show_help()
'''if __name__ == "__main__":
    game1 = match_Game()
    game1.run()
    game2 = link_Game()
    game2.run()'''

