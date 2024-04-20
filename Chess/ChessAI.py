import random


pieceScore = {"K": 1, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1} #A dictionary that assigns points to each piece
CHECKMATE = 1000 #Points assigned to checkmate
STALEMATE = 0 #Points assigned to stalemate

'''
Picks and returns a random move
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

'''
Find the best move based on material alone
'''
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1 #Whether the AI plays white or black
    maxScore = -CHECKMATE
    bestMove = None
    equalMoves = [] #Moves of equivalent score impact
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = turnMultiplier*scoreMaterial(gs.board) #Aiming for either 1000 or -1000 based on who the AI is

        if score > maxScore:
            maxScore = score
            bestMove = playerMove
            equalMoves.clear()
            equalMoves.append(playerMove)
        elif score is maxScore:
            equalMoves.append(playerMove)
        gs.undoMove()

    if len(equalMoves) > 1: #If there are more than 1 equivalent moves, randomly pick one
        bestMove = findRandomMove(equalMoves)
        equalMoves.clear()

    return bestMove

'''
Score the board based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score

