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

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE



UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
class slide_g(object):
    def __init__(self,BOARDHEIGHT=2,BOARDWIDTH=2):
        self.bw = BOARDWIDTH
        self.bh = BOARDHEIGHT
        self.XMARGIN = int((WINDOWWIDTH - (TILESIZE * self.bw + (self.bw - 1))) / 2)
        self.YMARGIN = int((WINDOWHEIGHT - (TILESIZE * self.bh + (self.bh - 1))) / 2)

    def main(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('FuHsi')
        BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

        # Store the option buttons and their rectangles in OPTIONS.
        RESET_SURF, RESET_RECT = self.makeText('set',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
        NEW_SURF,   NEW_RECT   = self.makeText('neagame', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
        SOLVE_SURF, SOLVE_RECT = self.makeText('sloved',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

        mainBoard, solutionSeq = self.generateNewPuzzle(10)
        SOLVEDBOARD = self.getStartingBoard() # a solved board is the same as the board in a start state.
        allMoves = [] # list of moves made from the solved configuration

        while True: # main game loop
            slideTo = None # the direction, if any, a tile should slide
            msg = u'点击数字或按下键盘的上下左右键滑动数字' # contains the message to show in the upper left corner.
            if mainBoard == SOLVEDBOARD:
                msg =u'成功!'

            self.drawBoard(mainBoard, msg)

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
                self.slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) # show slide on screen
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


    def getStartingBoard(self):
        # Return a board data structure with tiles in the solved state.
        # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
        # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
        counter = 1
        board = []
        for x in range(self.bw):
            column = []
            for y in range(self.bh):
                column.append(counter)
                counter += self.bw
            board.append(column)
            counter -= self.bw * (self.bh - 1) + self.bw - 1

        board[self.bw-1][self.bh-1] = BLANK
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


    def drawBoard(self,board, message):
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
            self.slideAnimation(board, move, 'y游戏初始化......', animationSpeed=int(TILESIZE / 3))
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



class background(pygame.sprite.Sprite):
    def __init__(self,filename,inittial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect  = self.image.get_rect()
        self.rect.bottomright = inittial_position


def startFlash():
    start_location = [0,0]
    stbg_Group = pygame.sprite.Group()
    stbg_Group.add(background('start1.png', start_location))
    stbg_Group.add(background('start2.png', start_location))
    stbg_Group.add(background('start3.png', start_location))
    for sf in stbg_Group.sprites():
        time.sleep(3)
        screen.blit(sf.image,sf.rect)

def show_help(filename='1.png',imagelocation=[100,100]):
    print 'True'
    imagep = pygame.image.load(filename)
    rect = imagep.get_rect()
    rect.bottomright = imagelocation
    screen.blit(imagep,rect)

bg_location = ([100,64],[210,64],[300,500],[410,500])
bg_Group = pygame.sprite.Group()
bg_Group.add(background('help.png',bg_location[0]))
bg_Group.add(background('know.png',bg_location[1]))
bg_Group.add(background('newgame.png',bg_location[2]))
bg_Group.add(background('exit.png',bg_location[3]))


screenCaption = pygame.display.set_caption('Fuhsi')
screen = pygame.display.set_mode([600,500])
screen.fill([255,255,255])
#pygame.draw.circle(screen,THECOLORS['blue'],[100,100],30,2)
background = pygame.Surface([600,500])
background.fill([0,0,255])
screen.blit(background,(0,0))

for bg in bg_Group.sprites():
    screen.blit(bg.image,bg.rect)
'''my_font = pygame.font.SysFont(None, 22)
text = 'helloworld'#u'伏羲'
text_suf = my_font.render(text,True,(0,0,255))
screen.blit(text_suf,(200,200))'''

pygame.display.flip()
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type==pygame.MOUSEBUTTONDOWN:
            print event.pos
            clickxy = event.pos
        elif event.type==pygame.MOUSEBUTTONUP:
            if clickxy[0]<100 and clickxy[1]<100 and clickxy[0]>0 and clickxy[1]>0:
                slide = slide_g(BOARDHEIGHT=2,BOARDWIDTH=2)
                slide.main()
                show_help()
'''if __name__ == "__main__":
    game1 = match_Game()
    game1.run()
    game2 = link_Game()
    game2.run()'''



