from space import Piece

EMPTY = 0
FIRE = 1
GRASS = 2
WATER = 3
HEART = 4
ELECTRIC = 5
POKEBALL = 6
CLEAR = 7
DEAD = 8

HEIGHT = 12
WIDTH = 6

class Board:
    # If no special inputs specified, constructs an empty board
    # Sets cursor to the defualt position which is in the middle of the board
    # If input rows is specified then creates a board with the supplied pieces
    # If input board is specified then creates a copy of the board
    def __init__(self, inputRows=None, inputDeadBlocks=None, inputBoard=None):
        self.rows = []
        self.deadBlocks = []
        if inputBoard != None:
            for r in xrange(HEIGHT):
                row = list(inputBoard.rows[r])
                self.rows.append(row)
            self.cursor = inputBoard.cursor
            self.deadBlocks = list(inputBoard.deadBlocks)
        elif inputRows != None:
            for r in xrange(HEIGHT):
                row = list(inputRows[r])
                self.rows.append(row)
            self.cursor = (5,2)
            if inputDeadBlocks != None:
                self.deadBlocks = list(inputDeadBlocks)
        else:
            for r in xrange(HEIGHT):
                row = []
                for c in xrange(WIDTH):
                    row.append(Piece(EMPTY))
                self.rows.append(row)
            self.cursor = (5, 2)

    # Apply gravity to the pieces in the board.
    # Drops any suspended pieces down
    def applyGravity(self):
        fallHeight = []
        for c in xrange(WIDTH):
            fallHeight.append(0)
        for r in xrange(HEIGHT):
            deadChunks = set()
            for c in xrange(WIDTH):
                if FIRE <= self.rows[r][c].getValue():
                    if fallHeight[c] < r and self.rows[r][c].getValue() <= POKEBALL:
                        self.rows[fallHeight[c]][c].setValue(self.rows[r][c].getValue())
                        self.rows[r][c].setValue(EMPTY)
                    if self.rows[r][c].getValue() == DEAD:
                        deadBlock = self.findDeadBlock((r,c))
                        deadChunks.add(deadBlock)
                    else:
                        fallHeight[c] += 1
            for chunk in deadChunks:
                if chunk[0][0] != 0:
                    peak = 0
                    for c in xrange(chunk[0][1], chunk[1][1]):
                        peak = max(peak, fallHeight[c])
                    if peak < chunk[0][0]:
                        for c in xrange(chunk[0][1], chunk[1][1]+1):
                            fallHeight[c] = peak+1
                            for r in xrange(chunk[0][0], chunk[1][0]+1):
                                self.rows[peak+(r-chunk[0][0])][c].setValue(DEAD)
                                self.rows[r][c].setValue(EMPTY)

    def findDeadBlock(self, deadPiece):
        for block in self.deadBlocks:
            if block[0][0] <= deadPiece[0] and block[0][1] <= deadPiece[1] \
               and block[1][0] >= deadPiece[0] and block[1][1] >= deadPiece[1]:
                return block
        return None

    # Sets a board's pieces to match those specified by inputRows
    def setFromRows(self, inputRows, inputDeadBlocks=[]):
        for r in xrange(HEIGHT):
            for c in xrange(WIDTH):
                self.rows[r][c] = inputRows[r][c]
        self.deadBlocks = list(inputDeadBlocks)

    # Sets a board's pieces to match a board described by an input file
    def loadFromFile(self, inputFile):
        with open(inputFile) as f:
            inputBoard = f.readlines()
        for l in xrange(HEIGHT):
            values = inputBoard[l].split()
            for v in xrange(len(values)):
                self.rows[HEIGHT-(l+1)][v].setValue(int(values[v]))
        self.deadBlocks = []
        for l in xrange(HEIGHT,len(inputBoard)):
            deadBlock = inputBoard[l].split("|")
            firstCorner = deadBlock[0].split(",")
            secondCorner = deadBlock[1].split(",")
            self.deadBlocks.append(((int(firstCorner[0]), int(firstCorner[1])),\
                                    (int(secondCorner[0]),int(secondCorner[1]))))

    # Prints out a board
    def printBoard(self):
        for row in reversed(self.rows):
            rowString = ""
            for piece in row:
                rowString += str(piece.getValue()) + " "
            print rowString
        print "cursor: " + str(self.cursor)

"""
board = Board()
board.loadFromFile('TestBoards/board3.txt')
board.printBoard()
board.applyGravity()
board.printBoard()
"""
