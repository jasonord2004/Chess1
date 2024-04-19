"""
This class is responsible for storing all the information about hte current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""


class GameState():
    def __init__(self):  # This initializes itself
        # The Board is a 8x8 two-dimensional list, each element of the list has 2 characters.
        # The first character represents the color of piece, 'b' or 'w'
        # The second character represents the type of the piece 'K' for king, etc.
        # "--" represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () #coordinates for the square where en passant capture is possible
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]


    '''
    Takes a move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant
    '''

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != '--':
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)  # log the move so we can undo it later
            self.whiteToMove = not self.whiteToMove  # switch turns
            #update king's location
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            promotedPiece = input("Promote to Q, R, B, or N:")
            self.board[move.endRow][move.endCol] =  move.pieceMoved[0] + promotedPiece.upper()

        #update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.enpassantPossible = ()

        # enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"  # capturing the pawn

        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle move
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves the rook
                self.board[move.endRow][move.endCol+1] = '--'
            else: #queenside castle move
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #moves the rook
                self.board[move.endRow][move.endCol-2] = '--'

        #update the castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back
            # update king's location
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--" #leave landing square blank
                self.board[move.startRow][move.startCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            #undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
            #undo castling rights
            self.castleRightsLog.pop() #get rid of the new castle rights from the move we are undoing
            self.currentCastlingRights = self.castleRightsLog[-1] #set the current castle rights to the last one in the list
            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else: #queenside
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'

    '''
    Update the castle rights given the move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRights.bks = False
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        #generate all possible moves
        moves = []

        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            # if there is only 1 piece causing check, then you can either move the king or block check
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                #to block a check, an ally piece must be move into a square between the enemy piece and the king
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #the location of the enemy piece causing check
                validSquares = [] #squares that pieces can move to
                #since the knight can jump over pieces, if the knight is checking, you must move or capture the knight
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) #check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #once you get to the piece, end checks
                            break
                #get rid of any moves that don't block the check or move the king
                for i in range(len(moves) - 1, -1, -1): #go through the loop backwards when removing item from a list
                    if moves[i].pieceMoved[1] != 'K': #move doesn't move the king, so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: #move doesn't block check or capture piece
                            moves.remove(moves[i])

            else: #doubleCheck, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: #not in check, so all the moves are fine to do
            moves = self.getAllPossibleMoves()

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            if len(moves) != 0 and moves[len(moves)-1].isCastleMove:
                print("CASTLE??: ", moves[len(moves)-1].moveID)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        #prints list of valid moves
        # for i in range(len(moves)):
        #     print("VALID: ", moves[i].moveID)
        if moves == []:
            if self.inCheck:
                self.checkmate = True
                print("CHECKM")
            else:
                self.stalemate = True
                print("STALE")
        return moves  # for now, not worrying about checks

    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                return True
        return False

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []  #List of all possible moves
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in given row
                turn = self.board[r][c][0]  # returns the first letter of what is in the current square
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    #instead of doing a lot of if statements, you can make a dictionary
                    # if piece == 'p':
                    #     self.getPawnMoves(r, c, moves)
                    # elif piece == 'R':
                    #     self.getRookMoves(r, c, moves)
                    # elif piece == 'N':
                    #     self.getKnightMoves(r, c, moves)
                    # elif piece == 'B':
                    #     self.getBishopMoves(r, c, moves)
                    # elif piece == 'Q':
                    #     self.getQueenMoves(r, c, moves)
                    # elif piece == 'K':
                    #     self.getKingMoves(r, c, moves)
                    self.moveFunctions[piece](r, c, moves) #calls the appropriate move function based on piece types
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col, and add these moves to the list
    '''

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 square white pawn advance
                if not piecePinned or pinDirection == (-1, 0):
                    if r - 1 == 0:
                        pawnPromotion = True
                        moves.append(Move((r, c), (r-1, c), self.board, pawnPromotion))
                    else:
                        moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                        moves.append(Move((r, c), (r-2, c), self.board))

            #captures
            if c-1 >= 0: #captures to the left
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    if not piecePinned or pinDirection == (-1, -1):
                        if r - 1 == 0:
                            pawnPromotion = True
                            moves.append(Move((r, c), (r-1, c-1), self.board, pawnPromotion=True))
                        else:
                            moves.append(Move((r, c), (r - 1, c - 1), self.board))
                if(r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture
                    if not piecePinned or pinDirection == (-1, 1):
                        if r - 1 == 0:
                            pawnPromotion = True
                            moves.append(Move((r, c), (r-1, c+1), self.board, pawnPromotion=True))
                        else:
                            moves.append(Move((r, c), (r - 1, c + 1), self.board))
                if (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))

        else: #black pawn moves
            if self.board[r+1][c] == "--": #1 square black pawn advance
                if not piecePinned or pinDirection == (1, 0):
                    if r + 1 == 0:
                        pawnPromotion = True
                        moves.append(Move((r, c), (r+1, c), self.board, pawnPromotion=True))
                    else:
                        moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":  # 2 square pawn advance
                        moves.append(Move((r, c), (r+2, c), self.board))
            #captures
            if c-1 >= 0:  # captures to the left
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture
                    if not piecePinned or pinDirection == (1, -1):
                        if r + 1 == 0:
                            pawnPromotion = True
                            moves.append(Move((r, c), (r+1, c-1), self.board, pawnPromotion=True))
                        else:
                            moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c+1 <= 7:  # captures to the right
                if self.board[r+1][c + 1][0] == 'w':  # enemy piece to capture
                    if not piecePinned or pinDirection == (1, 1):
                        if r + 1 == 0:
                            pawnPromotion = True
                            moves.append(Move((r, c), (r+1, c+1), self.board, pawnPromotion=True))
                        else:
                            moves.append(Move((r, c), (r + 1, c + 1), self.board))
                if (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))

        #add pawn promotions later

    '''
    Get all the rook moves for the pawn located at row, col, and add these moves to the list
    '''

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': #can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        if self.whiteToMove: #white's turn
            for U in range(1, r+1): #up moves
                if not piecePinned or pinDirection == (-1, 0) or pinDirection == (1, 0):
                    if self.board[r-U][c] == "--":
                        moves.append(Move((r, c), (r-U, c), self.board))
                    elif self.board[r-U][c][0] == "b":
                        moves.append(Move((r, c), (r-U, c), self.board))
                        break
                    else:
                        break
            for D in range(1, len(self.board[r])-r): #down moves
                if not piecePinned or pinDirection == (1, 0) or pinDirection == (-1, 0):
                    if self.board[r+D][c] == "--":
                        moves.append(Move((r, c), (r+D, c), self.board))
                    elif self.board[r+D][c][0] == "b":
                        moves.append(Move((r, c), (r+D, c), self.board))
                        break
                    else:
                        break
            for L in range(1, c+1): #left moves
                if not piecePinned or pinDirection == (0, -1) or pinDirection == (0, 1):
                    if self.board[r][c-L] == "--":
                        moves.append(Move((r, c), (r, c-L), self.board))
                    elif self.board[r][c - L][0] == "b":
                        moves.append(Move((r, c), (r, c-L), self.board))
                        break
                    else:
                        break
            for R in range(1, len(self.board[r])-c): #right moves
                if not piecePinned or pinDirection == (0, 1) or pinDirection == (0, -1):
                    if self.board[r][c+R] == "--":
                        moves.append(Move((r, c), (r, c+R), self.board))
                    elif self.board[r][c+R][0] == "b":
                        moves.append(Move((r, c), (r, c+R), self.board))
                        break
                    else:
                        break
        else: #black's turn
            for U in range(1, r+1): #up moves
                if not piecePinned or pinDirection == (-1, 0) or pinDirection == (1, 0):
                    if self.board[r-U][c] == "--":
                        moves.append(Move((r, c), (r-U, c), self.board))
                    elif self.board[r-U][c][0] == "w":
                        moves.append(Move((r, c), (r-U, c), self.board))
                        break
                    else:
                        break
            for D in range(1, len(self.board[r])-r): #down moves
                if not piecePinned or pinDirection == (1, 0) or pinDirection == (-1, 0):
                    if self.board[r+D][c] == "--":
                        moves.append(Move((r, c), (r+D, c), self.board))
                    elif self.board[r+D][c][0] == "w":
                        moves.append(Move((r, c), (r+D, c), self.board))
                        break
                    else:
                        break
            for L in range(1, c+1): #left moves
                if not piecePinned or pinDirection == (0, -1) or pinDirection == (0, 1):
                    if self.board[r][c-L] == "--":
                        moves.append(Move((r, c), (r, c-L), self.board))
                    elif self.board[r][c - L][0] == "w":
                        moves.append(Move((r, c), (r, c-L), self.board))
                        break
                    else:
                        break
            for R in range(1, len(self.board[r])-c): #right moves
                if not piecePinned or pinDirection == (0, 1) or pinDirection == (0, -1):
                    if self.board[r][c+R] == "--":
                        moves.append(Move((r, c), (r, c+R), self.board))
                    elif self.board[r][c+R][0] == "w":
                        moves.append(Move((r, c), (r, c+R), self.board))
                        break
                    else:
                        break

    '''
    Get all the knight moves for the pawn located at row, col, and add these moves to the list
    '''

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            if r-2 >= 0: #if can move upwards
                if c+1 < len(self.board[r]): #up and right
                    if not piecePinned and self.board[r-2][c+1] == "--" or self.board[r-2][c+1][0] == "b":
                        moves.append(Move((r, c), ((r-2), (c+1)), self.board))
                if c-1 >= 0: #up and left
                    if not piecePinned and self.board[r-2][c-1] == "--" or self.board[r-2][c-1][0] == "b":
                        moves.append(Move((r, c), ((r-2), (c-1)), self.board))

            if r+2 < len(self.board[r]): #if can move downwards
                if c + 1 < len(self.board[r]): #down and right
                    if not piecePinned and self.board[r+2][c+1] == "--" or self.board[r+2][c+1][0] == "b":
                        moves.append(Move((r, c), ((r+2), (c+1)), self.board))
                if c - 1 >= 0: #down and left
                    if not piecePinned and self.board[r+2][c-1] == "--" or self.board[r+2][c-1][0] == "b":
                        moves.append(Move((r, c), ((r+2), (c-1)), self.board))

            if r-1 >= 0: #if can move upwards
                if c+2 < len(self.board[r]): #up and right
                    if not piecePinned and self.board[r-1][c+2] == "--" or self.board[r-1][c+2][0] == "b":
                        moves.append(Move((r, c), ((r-1), (c+2)), self.board))
                if c-2 >= 0: #up and left
                    if not piecePinned and self.board[r-1][c-2] == "--" or self.board[r-1][c-2][0] == "b":
                        moves.append(Move((r, c), ((r-1), (c-2)), self.board))
            if r+1 < len(self.board[r]): #if can move downwards
                if c+2 < len(self.board[r]): #down and right
                    if not piecePinned and self.board[r+1][c+2] == "--" or self.board[r+1][c+2][0] == "b":
                        moves.append(Move((r, c), ((r+1), (c+2)), self.board))
                if c-2 >= 0: #down and left
                    if not piecePinned and self.board[r+1][c-2] == "--" or self.board[r+1][c-2][0] == "b":
                        moves.append(Move((r, c), ((r+1), (c-2)), self.board))

        else: #black's turn
            if r-2 >= 0: #if can move upwards
                if c+1 < len(self.board[r]):  #up and right
                    if not piecePinned and self.board[r-2][c+1] == "--" or self.board[r-2][c+1][0] == "w":
                        moves.append(Move((r, c), ((r-2), (c+1)), self.board))
                if c-1 >= 0: #up and left
                    if not piecePinned and self.board[r-2][c-1] == "--" or self.board[r-2][c-1][0] == "w":
                        moves.append(Move((r, c), ((r-2), (c-1)), self.board))
            if r+2 < len(self.board[r]): #if can move downwards
                if c + 1 < len(self.board[r]):  #down and right
                    if not piecePinned and self.board[r+2][c+1] == "--" or self.board[r+2][c+1][0] == "w":
                        moves.append(Move((r, c), ((r+2), (c+1)), self.board))
                if c - 1 >= 0: #down and left
                    if not piecePinned and self.board[r+2][c-1] == "--" or self.board[r+2][c-1][0] == "w":
                        moves.append(Move((r, c), ((r+2), (c-1)), self.board))

            if r-1 >= 0: #if can move upwards
                if c+2 < len(self.board[r]): #up and right
                    if not piecePinned and self.board[r-1][c+2] == "--" or self.board[r-1][c+2][0] == "w":
                        moves.append(Move((r, c), ((r-1), (c+2)), self.board))
                if c-2 >= 0: #up and left
                    if not piecePinned and self.board[r-1][c-2] == "--" or self.board[r-1][c-2][0] == "w":
                        moves.append(Move((r, c), ((r-1), (c-2)), self.board))
            if r+1 < len(self.board[r]): #if can move downwards
                if c+2 < len(self.board[r]): #down and right
                    if not piecePinned and self.board[r+1][c+2] == "--" or self.board[r+1][c+2][0] == "w":
                        moves.append(Move((r, c), ((r+1), (c+2)), self.board))
                if c-2 >= 0: #down and left
                    if not piecePinned and self.board[r+1][c-2] == "--" or self.board[r+1][c-2][0] == "w":
                        moves.append(Move((r, c), ((r+1), (c-2)), self.board))

    '''
    Get all the bishop moves for the pawn located at row, col, and add these moves to the list
    '''

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:  # white's turn
            for uR in range(1, len(self.board[r])):  # up-right moves
                if not piecePinned or pinDirection == (-1, 1) or pinDirection == (1, -1):
                    if r-uR < 0 or c+uR > len(self.board[r])-1 or self.board[r-uR][c+uR][0] == "w":
                        break
                    elif self.board[r-uR][c+uR] == "--":
                        moves.append(Move((r, c), (r-uR, c+uR), self.board))
                    elif self.board[r-uR][c+uR][0] == "b":
                        moves.append(Move((r, c), (r-uR, c+uR), self.board))
                        break
            for uL in range(1, len(self.board[r])):  # up-left moves
                if not piecePinned or pinDirection == (-1, -1) or pinDirection == (1, 1):
                    if r-uL < 0 or c-uL < 0 or self.board[r-uL][c-uL][0] == "w":
                        break
                    elif self.board[r-uL][c-uL] == "--":
                        moves.append(Move((r, c), (r-uL, c-uL), self.board))
                    elif self.board[r-uL][c-uL][0] == "b":
                        moves.append(Move((r, c), (r-uL, c-uL), self.board))
                        break
            for dR in range(1, len(self.board[r])):  # down-right moves
                if not piecePinned or pinDirection == (1, 1) or pinDirection == (-1, -1):
                    if r+dR > len(self.board[r])-1 or c+dR > len(self.board[r])-1 or self.board[r+dR][c+dR][0] == "w":
                        break
                    if self.board[r+dR][c+dR] == "--":
                        moves.append(Move((r, c), (r+dR, c+dR), self.board))
                    elif self.board[r+dR][c+dR][0] == "b":
                        moves.append(Move((r, c), (r+dR, c+dR), self.board))
                        break
            for dL in range(1, len(self.board[r])):  # down-left moves
                if not piecePinned or pinDirection == (1, -1) or pinDirection == (-1, 1):
                    if r+dL > len(self.board[r])-1 or c-dL < 0 or self.board[r+dL][c-dL][0] == "w":
                        break
                    elif self.board[r+dL][c-dL] == "--":
                        moves.append(Move((r, c), (r+dL, c-dL), self.board))
                    elif self.board[r+dL][c-dL][0] == "b":
                        moves.append(Move((r, c), (r+dL, c-dL), self.board))
                        break

        else:  # black's turn
            for uR in range(1, len(self.board[r])):  # up-right moves
                if not piecePinned or pinDirection == (-1, 1) or pinDirection == (1, -1):
                    if r-uR < 0 or c+uR > len(self.board[r])-1 or self.board[r-uR][c+uR][0] == "b":
                        break
                    elif self.board[r-uR][c+uR] == "--":
                        moves.append(Move((r, c), (r-uR, c+uR), self.board))
                    elif self.board[r-uR][c+uR][0] == "w":
                        moves.append(Move((r, c), (r-uR, c+uR), self.board))
                        break
            for uL in range(1, len(self.board[r])):  # up-left moves
                if not piecePinned or pinDirection == (-1, -1) or pinDirection == (1, 1):
                    if r-uL < 0 or c-uL < 0 or self.board[r-uL][c-uL][0] == "b":
                        break
                    elif self.board[r-uL][c-uL] == "--":
                        moves.append(Move((r, c), (r-uL, c-uL), self.board))
                    elif self.board[r-uL][c-uL][0] == "w":
                        moves.append(Move((r, c), (r-uL, c-uL), self.board))
                        break
            for dR in range(1, len(self.board[r])):  # down-right moves
                if not piecePinned or pinDirection == (1, 1) or pinDirection == (-1, -1):
                    if r+dR > len(self.board[r])-1 or c+dR > len(self.board[r])-1 or self.board[r+dR][c+dR][0] == "b":
                        break
                    if self.board[r+dR][c+dR] == "--":
                        moves.append(Move((r, c), (r+dR, c+dR), self.board))
                    elif self.board[r+dR][c+dR][0] == "w":
                        moves.append(Move((r, c), (r+dR, c+dR), self.board))
                        break
            for dL in range(1, len(self.board[r])):  # down-left moves
                if not piecePinned or pinDirection == (1, -1) or pinDirection == (-1, 1):
                    if r+dL > len(self.board[r])-1 or c-dL < 0 or self.board[r+dL][c-dL][0] == "b":
                        break
                    elif self.board[r+dL][c-dL] == "--":
                        moves.append(Move((r, c), (r+dL, c-dL), self.board))
                    elif self.board[r+dL][c-dL][0] == "w":
                        moves.append(Move((r, c), (r+dL, c-dL), self.board))
                        break

    '''
    Get all the Queen moves for the pawn located at row, col, and add these moves to the list
    '''

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
    Get all the King moves for the pawn located at row, col, and add these moves to the list
    '''

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece (empty or enemy)
                    #place king on end square and check for checks
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    #place king back on original location
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

    '''
    Generate all valid castle moves for the king at (r, c) and add them to the list of moves
    '''

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return #can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))
                print("CASTLE: ", moves[len(moves)-1].moveID)

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))


    '''
    Returns if the player is in check, a list of pins, and a list of checks
    '''
    def checkForPinsAndChecks(self):
        pins = [] #squares where the allied pinned piece is and the direction it is pinned from
        checks = [] #squares where enemy is applying a check from
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        #check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        #the first 4 directions in this dictionary are the orthogonal directions
        #the last 4 directions in this dictionary are the diagonal directions
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () #reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8  and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == (): #1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: #2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1] #the type of piece checking
                        #5 possibilities that are causing checks (knight done separately)
                        #1) Orthogonally away from the king and the piece is a rook
                        #2) Diagonally away from the king and the piece is a bishop
                        #3) 1 square away from the king and the piece is a pawn (can only attack in one direction)
                        #4) Any direction (Orthogonally and Diagonally) away from the king and the piece is a queen
                        #5) Any direction 1 square away form the king and the piece is a king
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or \
                                (i == 1 and type == 'K'):
                            if possiblePin == (): #there is no piece blocking, so the king is in check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #there is a piece blocking, so a piece is pinned
                                pins.append(possiblePin)
                                break
                        else: #enemy piece not applying check
                            break
                else: #out of the board area
                    break
                #check for knight checks
                knightMoves = {(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)}
                for m in knightMoves:
                    endRow = startRow + m[0]
                    endCol = startCol + m[1]
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece[0] == enemyColor and endPiece[1] == 'N': #there is an enemy knight attacking the king
                            inCheck = True
                            checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
class Move():
    # these dictionaries maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, pawnPromotion = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #pawn promotion
        self.isPawnPromotion = ((self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)) #will determine pawn promotion
        #en passant
        self.isEnpassantMove = isEnpassantMove
        self.pawnPromotion = pawnPromotion
        if self.isEnpassantMove:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'
        #castle move
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
