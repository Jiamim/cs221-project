from space import Piece
import copy

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
        self.backupRows = []
        self.backupDeadBlocks = []
        self.backupCursor = (5,2)
        self.softRows = []
        self.createBackUps()
        if inputBoard != None:
            for r in xrange(HEIGHT):
                row = []
                for tile in inputBoard.rows[r]:
                    row.append(copy.copy(tile))
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
        self.commit()

    def createBackUps(self):
        for r in xrange(HEIGHT):
            row = []
            softRow = []
            for c in xrange(WIDTH):
                row.append(Piece(EMPTY))
                softRow.append(Piece(EMPTY))
            self.backupRows.append(row)
            self.softRows.append(softRow)

    def softCommit(self):
        for r in xrange(HEIGHT):
            for c in xrange(WIDTH):
                self.softRows[r][c].setValue(self.rows[r][c].getValue())

    def softRollback(self):
        for r in xrange(HEIGHT):
            for c in xrange(WIDTH):
                self.rows[r][c].setValue(self.softRows[r][c].getValue())

    def commit(self):
        for r in xrange(HEIGHT):
            for c in xrange(WIDTH):
                self.backupRows[r][c].setValue(self.rows[r][c].getValue())
        self.backupDeadBlocks = list(self.deadBlocks)
        self.backupCursor = self.cursor

    def rollback(self):
        for r in xrange(HEIGHT):
            for c in xrange(WIDTH):
                self.rows[r][c].setValue(self.backupRows[r][c].getValue())
        #self.deadBlocks = list(self.backupDeadBlocks)
        #self.cursor = self.backupCursor

    # Apply gravity to the pieces in the board.
    # Drops any suspended pieces down
    def applyGravity(self):
        fallenTiles = set()
        fallHeight = []
        for c in xrange(WIDTH):
            fallHeight.append(0)
        for r in xrange(HEIGHT):
            deadChunks = set()
            for c in xrange(WIDTH):
                if FIRE <= self.rows[r][c].getValue():
                    if fallHeight[c] < r and self.rows[r][c].getValue() <= POKEBALL:
                        self.rows[fallHeight[c]][c].setValue(self.rows[r][c].getValue())
                        fallenTiles.add((fallHeight[c], c))
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
        return fallenTiles

    def findMatches(self):
        matches = []
        # Check for horizontal matches
        for r in xrange(HEIGHT):
            matchStart = 0
            matchType = self.rows[r][0].getValue()
            for c in xrange(WIDTH):
                # Check if current streak is a valid match
                if FIRE <= matchType and matchType <= POKEBALL and \
                   (self.rows[r][c].getValue() != matchType or c == WIDTH - 1):
                    if c - matchStart > 2 or (self.rows[r][c].getValue() == matchType and c - matchStart > 1):
                        match = []
                        for i in xrange(matchStart, c):
                            match.append((r,i))
                        if c == WIDTH - 1 and self.rows[r][c].getValue() == matchType:
                            match.append((r,c))
                        matches.append(match)
                    matchStart = c
                    matchType = self.rows[r][c].getValue()
                if matchType == EMPTY:
                    matchStart = c
                    matchType = self.rows[r][c].getValue()
        # Check for vertical matches
        for c in xrange(WIDTH):
            matchStart = 0
            matchType = self.rows[0][c].getValue()
            for r in xrange(HEIGHT):
                # Check if current streak is a valid match
                if FIRE <= matchType and matchType <= POKEBALL and \
                   (self.rows[r][c].getValue() != matchType or r == HEIGHT - 1):
                    if r - matchStart > 2 or (self.rows[r][c].getValue() == matchType and r - matchStart > 1):
                        match = []
                        for i in xrange(matchStart, r):
                            match.append((i,c))
                        if r == HEIGHT - 1 and self.rows[r][c].getValue() == matchType:
                            match.append((r,c))
                        matches.append(match)
                    matchStart = r
                    matchType = self.rows[r][c].getValue()
                if matchType == EMPTY:
                    matchStart = r
                    matchType = self.rows[r][c].getValue()
        return matches

    # Find matches that only looks at locations where pieces were changed
    def focusedFindMatches(self, locations):
        matches = []
        horizontalViewedTiles = set()
        verticalViewedTiles = set()
        for startR, startC in locations:
            horizontalViewedTiles.add((startR, startC))
            verticalViewedTiles.add((startR, startC))
            matchType = self.rows[startR][startC].getValue()
            if matchType < FIRE or matchType > POKEBALL:
                continue
            # Check for horizontal match going through the location
            rightIndex = 0
            while startC + rightIndex+1 <= WIDTH - 1 and \
                   self.rows[startR][startC + rightIndex+1].getValue() == matchType and \
                   (startR, startC + rightIndex+1) not in horizontalViewedTiles:
                rightIndex = rightIndex + 1
            leftIndex = 0
            while startC + leftIndex-1 >= 0 and \
                  self.rows[startR][startC + leftIndex-1].getValue() == matchType and \
                  (startR, startC + leftIndex-1) not in horizontalViewedTiles:
                leftIndex = leftIndex - 1
            if rightIndex - leftIndex >= 2:
                match = []
                for i in xrange(startC+leftIndex,startC+rightIndex+1):
                    horizontalViewedTiles.add((startR, i))
                    match.append((startR, i))
                matches.append(match)
                
            # Check for vertical match going through the location
            upIndex = 0
            while startR + upIndex+1 <= HEIGHT - 1 and \
                   self.rows[startR + upIndex+1][startC].getValue() == matchType and \
                   (startR + upIndex+1, startC) not in verticalViewedTiles:
                upIndex = upIndex + 1
            downIndex = 0
            while startR + downIndex-1 >= 0 and \
                  self.rows[startR + downIndex-1][startC].getValue() == matchType and \
                  (startR + downIndex-1, startC) not in verticalViewedTiles:
                downIndex = downIndex - 1
            if upIndex - downIndex >= 2:
                match = []
                for i in xrange(startR+downIndex,startR+upIndex+1):
                    verticalViewedTiles.add((i, startC))
                    match.append((i, startC))
                matches.append(match)
        return matches
        

    # Removes any matches from the board, if clear is specified changes these pieces to cleared pieces
    def removeMatches(self, matches, clear=False):
        for match in matches:
            for r,c in match:
                if clear:
                    self.rows[r][c].setValue(CLEAR)
                else:
                    self.rows[r][c].setValue(EMPTY)

    # Takes the board into its next stable state via applying gravity and removing matches
    def processBoard(self):
        self.applyGravity()
        matches = self.findMatches()
        while (len(matches) > 0):
            #print matches
            self.removeMatches(matches)
            self.applyGravity()
            #self.printBoard()
            matches = self.findMatches()
            #print matches

    def findDeadBlock(self, deadPiece):
        for block in self.deadBlocks:
            if block[0][0] <= deadPiece[0] and block[0][1] <= deadPiece[1] \
               and block[1][0] >= deadPiece[0] and block[1][1] >= deadPiece[1]:
                return block
        return None

    # Swaps the piece at the specified position and the piece to its immediate right
    # If move is invalid does nothing
    def makeMove(self, position):
        if position[0] >= HEIGHT or position[0] < 0 \
           or position[1] >= WIDTH-1 or position[1] < 0:
            print "Invalid Move , " + str((position[0], position[1]))
        else:
            temp = self.rows[position[0]][position[1]].getValue()
            self.rows[position[0]][position[1]].setValue(self.rows[position[0]][position[1]+1].getValue())
            self.rows[position[0]][position[1]+1].setValue(temp)


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
        self.commit()

    # Evaluate function that returns the score for a board
    def evaluate(self):
        #self.softCommit()
        score = 0.0
        chainLevel = 1
        matches = self.findMatches()
        while len(matches) > 0:
            matchedTiles = set()
            for match in matches:
                for tile in match:
                    matchedTiles.add(tile)
            score += chainLevel * len(matchedTiles)
            self.applyGravity()
            self.removeMatches(matches)
            self.applyGravity()
            matches = self.findMatches()
            chainLevel += 1
        #self.softRollback()
        return score

    # Evaluate function that runs faster by only looking at changed locations
    def focusedEvaluate(self, locations):
        #self.softCommit()
        score = 0.0
        chainLevel = 1
        matches = self.focusedFindMatches(locations)
        while len(matches) > 0:
            matchedTiles = self.getMatchedTiles(matches)
            score += chainLevel * len(matchedTiles)
            matchedTiles.update(self.applyGravity())
            self.removeMatches(matches)
            matchedTiles.update(self.applyGravity())
            matches = self.focusedFindMatches(matchedTiles)
            chainLevel += 1
        #self.softRollback()
        return score

    def getMatchedTiles(self, matches):
        matchedTiles = set()
        for match in matches:
            matchedTiles.update(set(match))
        return matchedTiles

    # Prints out a board
    def printBoard(self):
        for row in reversed(self.rows):
            rowString = ""
            for piece in row:
                rowString += str(piece.getValue()) + " "
            print rowString
        print "cursor: " + str(self.cursor)


if __name__ == '__main__':
    board = Board()
    board.loadFromFile('TestBoards/test_board1.txt')
    board.printBoard()
    #board.applyGravity()
    #board.printBoard()
    #board.processBoard()
    #board.printBoard()
    matches = board.findMatches()
    board.removeMatches(matches)
    board.printBoard()
    board.applyGravity()
    board.printBoard()
    """
    changedLocations = set()
    changedLocations.add((8,4))
    changedLocations.add((8,5))
    print board.focusedEvaluate(changedLocations)
    matches = board.focusedFindMatches(changedLocations)
    #matches = board.findMatches()
    board.removeMatches(matches)
    changedLocations = board.getMatchedTiles(matches)
    board.printBoard()
    changedLocations.update(board.applyGravity())
    board.printBoard()
    print changedLocations
    matches = board.focusedFindMatches(changedLocations)
    #matches = board.findMatches()
    board.removeMatches(matches)
    changedLocations = board.getMatchedTiles(matches)
    board.printBoard()
    changedLocations.update(board.applyGravity())
    board.printBoard()
    print changedLocations
    matches = board.focusedFindMatches(changedLocations)
    #matches = board.findMatches()
    board.removeMatches(matches)
    changedLocations = board.getMatchedTiles(matches)
    board.printBoard()
    changedLocations.update(board.applyGravity())
    board.printBoard()
    print changedLocations
    matches = board.focusedFindMatches(changedLocations)
    #matches = board.findMatches()
    board.removeMatches(matches)
    board.printBoard()
    board.applyGravity()
    board.printBoard()
    """
