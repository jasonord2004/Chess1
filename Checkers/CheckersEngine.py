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
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)  # log the move so we can undo it later
            self.redToMove = not self.redToMove  # switch turns

        #pawn promotion
        #if move.isPawnPromotion:
            #promotedPiece = input("Promote to Q, R, B, or N:")
            #self.board[move.endRow][move.endCol] =  move.pieceMoved[0] + promotedPiece.upper()


    '''
    Undo the last move made
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
        # for i in range(len(moves)):
        #     print("VALID: ", moves[i].moveID)
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

    def getCheckerMoves(self, r, c, moves): # FIX METHOD

        if self.redToMove: #red checker moves
            if self.board[r-1][c] == "--": #1 square white pawn advance  FIX
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
