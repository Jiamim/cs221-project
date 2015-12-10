import random
import board

NUMMOVES = 2

class ExhaustiveBrain:
    def getSequenceScore(self, inputBoard, moves):
        score = 0
        for move in moves:
            inputBoard.makeMove(move)
            locations = set()
            locations.add(move)
            locations.add((move[0], move[1]+1))
            locations.update(inputBoard.applyGravity())
            score += inputBoard.focusedEvaluate(locations)
            #inputBoard.processBoard()
        inputBoard.rollback()
        return score

    def getAllMoves(self, inputBoard):
        moveSequences = []
        for r in xrange(board.HEIGHT):
            for c in xrange(board.WIDTH-1):
                moveSequences.append((r, c))
        return moveSequences

    def findBestActions(self, inputBoard):
        allMoves = self.getAllMoves(inputBoard)
        moveSequences = []
        moveSequences.append([])
        for i in xrange(NUMMOVES):
            newMoveSequences = []
            for sequence in moveSequences:
                for move in allMoves:
                    newSequence = list(sequence)
                    newSequence.append(move)
                    newMoveSequences.append(newSequence)

            moveSequences = newMoveSequences
        bestScore = 0
        bestSequence = []
        for sequence in moveSequences:
            score = self.getSequenceScore(inputBoard, sequence)
            if score > bestScore:
                bestScore = score
                bestSequence = sequence
        return bestScore, bestSequence

testBoard = board.Board()
testBoard.loadFromFile('TestBoards/random_board2.txt')
testBoard.processBoard()
testBoard.printBoard()
print ""
exBrain = ExhaustiveBrain()
score, actions = exBrain.findBestActions(testBoard)
for action in actions:
    testBoard.makeMove(action)
    testBoard.printBoard()
    print ""
    testBoard.processBoard()
testBoard.printBoard()
print ""
print score
print actions        
