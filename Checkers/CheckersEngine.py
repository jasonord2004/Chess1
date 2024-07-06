"""
This class is responsible for storing all the information about the current state of a checkers game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""


class GameState():
    def __init__(self):  # This initializes itself
        # The Board is a 8x8 two-dimensional list, each element of the list has 2 characters.
        # The first character represents the color of piece, 'b' or 'r'
        # The second character represents the type of the piece 'c' for checker, etc.
        # "--" represents an empty space with no piece.
        self.board = [
            ["--", "bc", "--", "bc", "--", "bc", "--", "bc"],
            ["bc", "--", "bc", "--", "bc", "--", "bc", "--"],
            ["--", "bc", "--", "bc", "--", "bc", "--", "bc"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["rc", "--", "rc", "--", "rc", "--", "rc", "--"],
            ["--", "rc", "--", "rc", "--", "rc", "--", "rc"],
            ["rc", "--", "rc", "--", "rc", "--", "rc", "--"],
        ]
        self.moveFunctions = {'c': self.getCheckerMoves}

        self.redToMove = True
        self.moveLog = []
        #self.checkmate = False
        #self.stalemate = False
        #self.inCheck = False
        #self.pins = []
        #self.checks = []


    '''
    Takes a move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant
    '''

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != '--':
            self.board[move.startRow][move.startCol] = '--'
            if move.pieceCaptured != "": #FIX
                self.board[move.capturedRow][move.capturedCol] = "--"
                print("CAPTURED: ", move.capturedRow, move.capturedCol, move.pieceCaptured)

            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)  # log the move so we can undo it later
            self.redToMove = not self.redToMove  # switch turns

        #piece promotion FIX
        #if move.isPawnPromotion:
            #promotedPiece = input("Promote to Q, R, B, or N:")
            #self.board[move.endRow][move.endCol] =  move.pieceMoved[0] + promotedPiece.upper()


    '''
    Undo the last move made  FIX
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undo
            move = self.moveLog.pop()
            #print("UNDO: ", move.pieceMoved, move.moveID, move.endRow, move.endCol)
            self.board[move.startRow][move.startCol] = move.pieceMoved
            #print(move.pieceMoved)
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            #print("UNDO CAPTURE: ", move.pieceCaptured, move.endRow, move.endCol)
            self.redToMove = not self.redToMove  # switch turns back



    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        #generate all possible moves
        moves = []

        moves = self.getAllPossibleMoves()

        # prints list of valid moves
        for i in range(len(moves)):
            print("VALID: ", moves[i].startRow, moves[i].startCol, moves[i].endRow, moves[i].endCol, "DONE")
        #if moves == []:
            #if self.inCheck:
                #self.checkmate = True
                #print("CHECK")
            #else:
                #self.stalemate = True
                #print("STALE")
        return moves

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []  #List of all possible moves
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in given row
                turn = self.board[r][c][0]  # returns the first letter of what is in the current square
                if (turn == 'r' and self.redToMove) or (turn == 'b' and not self.redToMove):
                    piece = self.board[r][c][1]
                    multiple = 0 #how many times a piece can capture
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
                    self.moveFunctions[piece](r, c, moves, multiple) #calls the appropriate move function based on piece types
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col, and add these moves to the list
    '''

    def getCheckerMoves(self, r, c, moves, multiple): # FIX METHOD

        if self.redToMove: #red checker moves
            if c-1 >= 0:
                if self.board[r-1][c-1] == "--": #red piece can advance left
                    if r - 1 == 0:
                        piecePromotion = True
                        moves.append(Move((r, c), (r-1, c-1), self.board, piecePromotion))
                    else:
                        moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1] == "--": #red piece can advance right
                    if r - 1 == 0:
                        piecePromotion = True
                        moves.append(Move((r, c), (r-1, c+1), self.board, piecePromotion))
                    else:
                        moves.append(Move((r, c), (r-1, c+1), self.board))

            #capturing ONLY 1 jump for now
            if c-multiple-2 >= 0: #captures to the left
                if self.board[r-multiple-1][c-multiple-1][0] == "b":
                    if r-multiple-2 >= 0 and self.board[r-multiple-2][c-multiple-2] == "--":
                        if r - multiple - 2 == 0:
                            piecePromotion = True
                            moves.append(Move((r, c), (r-multiple-2, c-multiple-2), self.board, piecePromotion=True))
                        else: #FIX CAPTURING MULTIPLE PIECES
                            moves.append(Move((r, c), (r - multiple - 2, c - multiple - 2), self.board))
                            multiple = multiple+2
                            self.getCheckerMoves(r, c, moves, multiple)
                            for i in range(len(moves)):
                                print("VALID: ", moves[i].startRow, moves[i].startCol, moves[i].endRow, moves[i].endCol)
            if c+2 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == "b":
                    if r-2 >= 0 and self.board[r-2][c+2] == "--":
                        if r - 2 == 0:
                            piecePromotion = True
                            moves.append(Move((r, c), (r-2, c+2), self.board, piecePromotion=True))
                        else:
                            moves.append(Move((r, c), (r-2, c+2), self.board))

        else:  # black checker moves
            if c - 1 >= 0:
                if self.board[r + 1][c - 1] == "--":  # black piece can advance left
                    if r + 1 == 7:
                        piecePromotion = True
                        moves.append(Move((r, c), (r + 1, c - 1), self.board, piecePromotion))
                    else:
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1] == "--":  # black piece can advance right
                    if r + 1 == 7:
                        piecePromotion = True
                        moves.append(Move((r, c), (r + 1, c + 1), self.board, piecePromotion))
                    else:
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

            # capturing ONLY 1 jump for now
            if c - 2 >= 0:  # captures to the left
                if self.board[r + 1][c - 1][0] == "r":
                    if r+2 >= 0 and self.board[r + 2][c - 2] == "--":
                        if r + 2 == 7:
                            piecePromotion = True
                            moves.append(Move((r, c), (r + 2, c - 2), self.board, piecePromotion=True))
                        else:
                            moves.append(Move((r, c), (r + 2, c - 2), self.board))
            if c + 2 <= 7:  # captures to the right
                if self.board[r + 1][c + 1][0] == "r":
                    if r+2 >= 0 and self.board[r + 2][c + 2] == "--":
                        if r + 2 == 7:
                            piecePromotion = True
                            moves.append(Move((r, c), (r + 2, c + 2), self.board, piecePromotion=True))
                        else:
                            moves.append(Move((r, c), (r + 2, c + 2), self.board))

class Move():
    # these dictionaries maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, piecePromotion = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        #only 1 capture
        if self.pieceMoved == 'rc':
            #print("CAPTURE: ")
            if self.startCol-2 == self.endCol: #if captured to the left
                self.capturedRow = self.startRow - 1
                self.capturedCol = self.startCol - 1
                self.pieceCaptured = board[self.capturedRow][self.capturedCol]
                #print("CAPTURE: ", self.pieceCaptured)
            elif self.startCol+2 == self.endCol: #if captured to the right
                self.capturedRow = self.startRow - 1
                self.capturedCol = self.startCol + 1
                self.pieceCaptured = board[self.capturedRow][self.capturedCol]
                #print("CAPTURE: ", self.pieceCaptured)
            else:
                self.pieceCaptured = ""
        if self.pieceMoved == 'bc':
            if self.startCol-2 == self.endCol: #if captured to the left
                self.capturedRow = self.startRow + 1
                self.capturedCol = self.startCol - 1
                self.pieceCaptured = board[self.capturedRow][self.capturedCol]
            elif self.startCol+2 == self.endCol: #if captured to the right
                self.capturedRow = self.startRow + 1
                self.capturedCol = self.startCol + 1
                self.pieceCaptured = board[self.capturedRow][self.capturedCol]

            else:
                self.pieceCaptured = ""
        #pawn promotion
        self.isPiecePromotion = ((self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)) #will determine pawn promotion
        #en passant
        self.isEnpassantMove = isEnpassantMove
        self.piecePromotion = piecePromotion
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
