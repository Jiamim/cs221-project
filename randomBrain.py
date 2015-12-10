import random
import board

NUMTRIALS = 400

class RandomBrain:
    def findBestActions(self, inputBoard, numMoves=8):
        bestScore = -100000
        bestMoves = []
        for i in xrange(NUMTRIALS):
            score = 0.0
            moves = []
            for j in xrange(numMoves):
                movePosition = (random.randint(0,board.HEIGHT-2),random.randint(0,board.WIDTH-2))
                inputBoard.makeMove(movePosition)
                locations = set()
                locations.add(movePosition)
                locations.add((movePosition[0], movePosition[1]+1))
                locations.update(inputBoard.applyGravity())
                tempScore, numClears = inputBoard.focusedEvaluate(locations)
                score += tempScore
                #score += inputBoard.evaluate()
                #inputBoard.processBoard()
                moves.append((movePosition, numClears))
            score -= inputBoard.getColumnHeightsScore(inputBoard.getColumnHeights())
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
    print actions
    for action in actions:
        testBoard.makeMove(action[0])
        testBoard.printBoard()
        print ""
        testBoard.processBoard()
    testBoard.printBoard()
    print ""
    print score
    print actions

