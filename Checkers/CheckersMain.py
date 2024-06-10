"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from Checkers.Checkers import CheckersEngine

WIDTH = HEIGHT = 512# 400 is also good
DIMENSION = 8  # Chessboard dimensions are 8x8
SQ_SIZE = HEIGHT // DIMENSION  # Since 512 is divisible by 8, each square will be uniformly sized
MAX_FPS = 15  # For animations later on
IMAGES = {}  # Dictionary of images

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''


def loadImages():
    pieces = ['rc', 'bc']
    for piece in pieces:  # Will set piece equal to the first element in pieces and iterate until completion or error
        IMAGES[piece] = p.transform.scale(p.image.load("Checkers images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: We can access an image by saying 'IMAGES['wc']'
    # p.transform.scale will make sure each image is uniformly scaled to the entire size of the chessboard square


'''
The main driver for our code. This will handle user input and updating the graphics
'''

def main():
    p.init()  # Initializes pygame
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = CheckersEngine.GameState()  # Calls the constructor CheckersEngine
    #validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    animate = False #flag variable for when we should animate a move
    loadImages()  # only do this once, before the while loop
    running = True
    sqSelected = () #no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] #keep track of player clicks (two tuples: [(6, 4), (4, 4])
    gameOver = False
    playerOne = True #If a human is playing white, then this will be True. If an AI is playing, then False
    playerTwo = False #Same but for black pieces
    while running:
        '''
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                #print("PLAYER MOVE:")
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()  # (x, y) location of mouse
                    col = location[0]//SQ_SIZE  # Uses double divides // to make sure it is rounded
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col): #the user clicked the same square twice
                        sqSelected = () #deselect
                        playerClicks = []# clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: #after 2nd click
                        move = CheckersEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)): #iterates through all the validMoves
                            if move == validMoves[i]: #if our current move is equal to the current valid move
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                #print("Piece: ", validMoves[i].pieceMoved, validMoves[i].moveID)
                                sqSelected = () #reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #resets the board when 'r' is pressed
                    gs = CheckersEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        #AI move finder
        if not gameOver and not humanTurn:
            # #AIMove = CheckersAI.findRandomMove(validMoves)  #The AI will make random moves
            # AIMove = CheckersAI.greedyAlgo(gs, validMoves)  #The AI will make the best moves based only on material
            AIMove = CheckersAI.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = CheckersAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        '''
        drawGameState(screen, gs)  # draws the screen
        '''
        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')
        '''
        clock.tick(MAX_FPS)
        #p.display.flip()

'''
Highlight square selected and moves for piece selected
'''
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != (): #square is not empty
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #makes sure the square selected is a piece that can be moved
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value --> 0 transparent; 255 solid
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
'''

'''
Responsible for all the graphics within a current game state
'''
#def drawGameState(screen, gs, validMoves, sqSelected):
def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on the board
    #highlightSquares(screen, gs, validMoves, sqSelected)
    #drawPieces(screen, gs.board)  # draw pieces on top of those squares


'''
Draw the squares on the board. Must call this function before the pieces.
'''

def drawBoard(screen):
    global colors
    colors = [p.Color(238, 238, 210), p.Color(118, 150, 86)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''

def drawPieces(screen, board): #Separated the two functions to highlight pieces
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = ((abs(dR) + abs(dC)) * framesPerSquare)
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*(frame/frameCount), move.startCol + dC*(frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(200)

def drawText(screen, text):
    font = p.font.SysFont("Times New Roman", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()
