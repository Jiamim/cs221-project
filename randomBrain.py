import random
import board

NUMTRIALS = 1000

class RandomBrain:
    def findBestActions(self, inputBoard, numMoves=8):
        bestScore = 0.0
        bestMoves = []
        for i in xrange(NUMTRIALS):
            score = 0.0
            moves = []
            for j in xrange(numMoves):
                movePosition = (random.randint(0,board.HEIGHT-1),random.randint(0,board.WIDTH-2))
                inputBoard.makeMove(movePosition)
                locations = set()
                locations.add(movePosition)
                locations.add((movePosition[0], movePosition[1]+1))
                locations.update(inputBoard.applyGravity())
                score += inputBoard.focusedEvaluate(locations)
                #score += inputBoard.evaluate()
                #inputBoard.processBoard()
                moves.append(movePosition)
            if score > bestScore:
                bestScore = score
                bestMoves = moves
            inputBoard.rollback()
        return bestScore, bestMoves

if __name__ == '__main__':
    testBoard = board.Board()
    testBoard.loadFromFile('TestBoards/random_board2.txt')
    testBoard.processBoard()
    testBoard.printBoard()
    print ""
    rndBrain = RandomBrain()
    score, actions = rndBrain.findBestActions(testBoard)
    for action in actions:
        testBoard.makeMove(action)
        testBoard.printBoard()
        print ""
        testBoard.processBoard()
    testBoard.printBoard()
    print ""
    print score
    print actions

