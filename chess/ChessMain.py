# this is the main driver file for the game #
# will be responsible for handling user inputs and displaying the current GameState object #


import pygame as p
from chess import ChessEngine

WIDTH = HEIGHT = 512  # or change to 400 if it looks too pixelated #
DIMENSION = 8  # dimentions of a chess board are 8x8 #
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations later on #
IMAGES = {}

'initialize a global dictionary of images. This will be called exactly once in the main' \


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

    # note: we can access an image by saying 'IMAGES['wp']' #


'the main driver for our code. This will handle user input and updating the graphics' \

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    loadImages()  # only do this once, before the while log #
    running = True
    sqSelected = ()  # there is no square selected initially, keeps track of users last click (tuple: (row,col))
    playerClicks = []  # keeps track of the player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # finds location of mouse#
                col = location [0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):  # user clicked the same square twice. #
                    sqSelected = () # deselects
                    playerClicks = [] # clears player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for bot 1st and 2nd clicks
                if len(playerClicks) == 2: # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () #reset user clicks
                    playerClicks = []



        clock.tick(MAX_FPS)
        p.display.flip()
        drawGameState(screen, gs)

'responsible for all the grapghics withhin the current game state'


def drawGameState(screen,gs):
    drawBoard(screen) # draws the squares on the baord #
    # add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) # draw pieces on top of the squares #


' draws the squares onto the board. the top left square is always white'
def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range (DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



' draws the pieces onto the board using the current GameState. board'
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--': #not an empty square (a piece is occupying it) #
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




if __name__ == '__main__':
    main()





