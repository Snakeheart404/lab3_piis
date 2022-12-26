import chess

class ChessHelper:
    @staticmethod
    def evaluate(gameState):
        pawn = 100
        knight = 300
        bishop = 300
        rook = 500
        queen = 900
        king = 2500
        mobilityWeight = 10
        
        whitepawns = len(gameState.pieces(1,1))
        whiteknights = len(gameState.pieces(2,1))
        whitebishops = len(gameState.pieces(3,1))
        whiterooks = len(gameState.pieces(4,1))
        whitequeens = len(gameState.pieces(5,1))
        whiteking = len(gameState.pieces(6,1))
        
        blackpawns = len(gameState.pieces(1,0))
        blackknights = len(gameState.pieces(2,0))
        blackbishops = len(gameState.pieces(3,0))
        blackrooks = len(gameState.pieces(4,0))
        blackqueens = len(gameState.pieces(5,0))
        blackking = len(gameState.pieces(6,0))
        
        whitematerial = pawn*whitepawns + knight*whiteknights + bishop*whitebishops + \
                        rook*whiterooks + queen*whitequeens +king*whiteking
        blackmaterial = pawn*blackpawns + knight*blackknights + bishop*blackbishops + \
                        rook*blackrooks + queen*blackqueens +king*blackking
        material = whitematerial - blackmaterial
        
        mobility1 = gameState.legal_moves.count()
        gameState.push(chess.Move.null())
        mobility2 = gameState.legal_moves.count()
        gameState.pop()
        if (gameState.turn == chess.WHITE):
            mobility = mobility1 - mobility2
        else:
            mobility = mobility2 - mobility1

        mobility = mobilityWeight * mobility
        return material + mobility

    @staticmethod
    def isDraw(gameState):
            return gameState.is_stalemate() or gameState.is_insufficient_material() or \
                   gameState.is_fivefold_repetition() or gameState.is_seventyfive_moves()

    def __init__(self, index=0, depth=2):
        self.index = int(index)
        self.depth = int(depth)

class NegaMax(ChessHelper):
    def getAction(self):
        def negamax(gameState, depth=self.depth, color=-1):
            if gameState.is_checkmate():
                return None
 
            if depth == 0 or self.isDraw(gameState):
                return None

            legalActions = gameState.legal_moves
            bestScore = float('-inf')
            bestAction = None

            for action in legalActions:
                gameState.push(action)
                score = -negamaxRecursion(gameState, depth - 1, -color)
                if score > bestScore:
                    bestScore = score
                    bestAction = action
                gameState.pop(action)
            return bestAction

        def negamaxRecursion(gameState, depth, color):
            if gameState.is_checkmate():
                return color * float('inf')

            if depth == 0 or self.isDraw(gameState):
                return color * self.evaluate(gameState)

            legalActions = gameState.legal_moves
            bestScore = float('-inf')

            for action in legalActions:
                gameState.push(action)
                score = -negamaxRecursion(gameState, depth - 1, -color)
                bestScore = max(bestScore, score)
                gameState.pop(action)

            return bestScore
