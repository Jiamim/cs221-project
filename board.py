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
    def __init__(self, inputRows=None, inputBoard=None):
        self.rows = []
        if inputBoard != None:
            for r in xrange(HEIGHT):
                row = list(inputBoard.rows[r])
                self.rows.append(row)
            self.cursor = inputBoard.cursor
        elif inputRows != None:
            for r in xrange(HEIGHT):
                row = list(inputRows[r])
                self.rows.append(row)
            self.cursor = (5,2)
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
            for c in xrange(WIDTH):
                if FIRE <= self.rows[r][c].getValue():
                    if fallHeight[c] < r:
                        self.rows[fallHeight[c]][c].setValue(self.rows[r][c].getValue())
                        self.rows[r][c].setValue(EMPTY)
                    fallHeight[c] += 1

    # Sets a board's pieces to match those specified by inputRows
    def setFromRows(self, inputRows):
        for r in xrange(HEIGHT):
            for c in xrange(WIDTH):
                self.rows[r][c] = inputRows[r][c]        

    # Sets a board's pieces to match a board described by an input file
    def loadFromFile(self, inputFile):
        with open(inputFile) as f:
            inputBoard = f.readlines()
        for line in enumerate(inputBoard):
            values = line[1].split()
            for v in xrange(len(values)):
                self.rows[HEIGHT-(line[0]+1)][v].setValue(int(values[v]))

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
board.loadFromFile('TestBoards/board2.txt')
board.printBoard()
board.applyGravity()
board.printBoard()
"""  
