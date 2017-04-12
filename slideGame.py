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
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 30
BLANK = None

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
BLUE =          (0,0,240)

SCREEN_SIZE = [WINDOWWIDTH,WINDOWHEIGHT]
WIDTH = 100
HEIGHT = 100
WAITING_TIME = 1000

BGCOLOR = BLUE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 28

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = 0
YMARGIN = 0


pygame.mixer.init()
bg_sound = pygame.mixer.Sound("plant.wav")
click_sound = pygame.mixer.Sound('click.wav')

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
pygame.init()
BASICFONT = pygame.font.Font('gkai00mp.ttf', BASICFONTSIZE)

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(u'8421')

DISPLAYSURF.fill(WHITE)
#pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)
background = pygame.Surface([600,500])
background.fill([0,0,255])
DISPLAYSURF.blit(background,(0,0))

def bgSoundPlay():
    pygame.mixer.init()
    bg_sound = pygame.mixer.Sound("plant.wav")
    bg_sound.play(loops=3)

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

# Store the option buttons and their rectangles in OPTIONS.
exit1_SURF, exit1_RECT = makeText(u'退出', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 120)
help_SURF, help_RECT = makeText(u'帮助', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 120)
RESET_SURF, RESET_RECT = makeText(u'设置', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 90)
NEW_SURF, NEW_RECT = makeText(u'新游戏', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 60)
SOLVE_SURF, SOLVE_RECT = makeText(u'破解', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 90, WINDOWHEIGHT - 30)
next_SURF, next_RECT = makeText(u'继续', TEXTCOLOR, TILECOLOR, 100, 0)
exit_SURF, exit_RECT = makeText(u'返回', TEXTCOLOR, TILECOLOR, 200, 0)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


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

        mainBoard, solutionSeq = self.generateNewPuzzle(2)
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
                            mainBoard, solutionSeq = self.generateNewPuzzle(10) # clicked on New Game button
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
        return

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