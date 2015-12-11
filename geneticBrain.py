import random
import board
import time

NUMSEQUENCES = 400
NUMGENERATIONS = 5
NUMMOVES = 8
SCALE = 2.0

class GeneticBrain:
    def getSequenceScore(self, inputBoard, moves):
        score = 0
        for move in moves:
            inputBoard.makeMove(move)
            locations = set()
            locations.add(move)
            locations.add((move[0], move[1]+1))
            locations.update(inputBoard.applyGravity())
            tempScore, numClears = inputBoard.focusedEvaluate(locations)
            score += tempScore
            #inputBoard.processBoard()
        score -= inputBoard.getColumnHeightsScore(inputBoard.getColumnHeights())
        inputBoard.rollback()
        return score
    
    def initializeSequences(self, inputBoard):
        moveSequences = []
        for i in xrange(NUMSEQUENCES):
            moves = []
            for j in xrange(NUMMOVES):
                movePosition = (random.randint(0,board.HEIGHT-2),random.randint(0,board.WIDTH-2))
                moves.append(movePosition)
            score = self.getSequenceScore(inputBoard, moves)
            moveSequences.append((pow(score,SCALE),moves))
        return moveSequences

    def pickSequence(self, moveSequences):
        total = sum(move[0] for move in moveSequences)
        choice = random.random()*total
        index = 0
        while choice > 0:
            choice -= moveSequences[index][0]
            index += 1
        return moveSequences[index-1][1]

    def spliceSequences(self, seq1, seq2):
        swapPoint = random.randint(0,NUMMOVES-1)
        child1 = []
        child2 = []
        for i in xrange(swapPoint):
            child1.append(seq1[i])
            child2.append(seq2[i])
        for i in xrange(swapPoint,NUMMOVES):
            child1.append(seq2[i])
            child2.append(seq1[i])
        return child1, child2

    def newGeneration(self, inputBoard, moveSequences):
        newMoveSequences = []
        for i in xrange(NUMSEQUENCES/2):
            seq1 = self.pickSequence(moveSequences)
            seq2 = self.pickSequence(moveSequences)
            child1, child2 = self.spliceSequences(seq1, seq2)
            newMoveSequences.append((pow(self.getSequenceScore(inputBoard, child1),SCALE),child1))
            newMoveSequences.append((pow(self.getSequenceScore(inputBoard, child2),SCALE),child2))
        return newMoveSequences

    def findBestActions(self, inputBoard):
        moveSequences = self.initializeSequences(inputBoard)
        for i in xrange(NUMGENERATIONS):
            moveSequences = self.newGeneration(inputBoard, moveSequences)
        bestSequence = []
        #bestScore = -1*inputBoard.getColumnHeightsScore(inputBoard.getColumnHeights())
        bestScore = -100000
        for sequence in moveSequences:
            if sequence[0] > bestScore:
                bestScore = sequence[0]
                bestSequence = sequence[1]
        return self.getSequenceScore(inputBoard, bestSequence), self.getSequenceClears(inputBoard, bestSequence)

    def getSequenceClears(self, inputBoard, sequence):
        finalMoves = []
        for move in sequence:
            inputBoard.makeMove(move)
            locations = set()
            locations.add(move)
            locations.add((move[0], move[1]+1))
            locations.update(inputBoard.applyGravity())
            tempScore, numClears = inputBoard.focusedEvaluate(locations)
            finalMoves.append((move, numClears))
        inputBoard.rollback()
        return finalMoves


if __name__ == '__main__':
    testBoard = board.Board()
    testBoard.loadFromFile('TestBoards/random_board1.txt')
    testBoard.processBoard()
    testBoard.printBoard()
    print ""
    genBrain = GeneticBrain()
    start_time = time.time()
    score, actions = genBrain.findBestActions(testBoard)
    print "time: " + str(time.time() - start_time)
    for action in actions:
        testBoard.makeMove(action[0])
        testBoard.printBoard()
        print ""
        testBoard.processBoard()
    testBoard.printBoard()
    print ""
    print score
    print actions

        
