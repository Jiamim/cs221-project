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
    def __init__(self):
        self.rows = []
        for r in xrange(HEIGHT):
            row = []
            for c in xrange(WIDTH):
                row.append(Piece(EMPTY))
            self.rows.append(row)
        self.cursor = (5, 2)

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

    def loadFromFile(self, inputFile):
        with open(inputFile) as f:
            inputBoard = f.readlines()
        for line in enumerate(inputBoard):
            values = line[1].split()
            for v in xrange(len(values)):
                self.rows[HEIGHT-(line[0]+1)][v].setValue(int(values[v]))

    def printBoard(self):
        for row in reversed(self.rows):
            rowString = ""
            for piece in row:
                rowString += str(piece.getValue()) + " "
            print rowString
        print "cursor: " + str(self.cursor)

board = Board()
board.loadFromFile('TestBoards/board2.txt')
board.printBoard()
board.applyGravity()
board.printBoard()
    
