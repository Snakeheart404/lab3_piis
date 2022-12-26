import chess

class ChessHelper:
    @staticmethod
    def evaluate(gameState: chess.Board):
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
    def __init__(self, depth=2):
        self.depth = int(depth)

class NegaMax(ChessHelper):
    def getAction(self, gameState: chess.Board):
        def negamax(state: chess.Board, color, depth=self.depth):
            if depth == 0 or state.outcome() is not None:
                return None

            legalActions = state.legal_moves
            bestScore = float('-inf')
            bestAction = None

            for action in legalActions:
                state.push(action)
                score = -recursiveNegamax(state, -color, depth - 1)
                if score > bestScore:
                    bestScore = score
                    bestAction = action
                state.pop()
            return bestAction

        def recursiveNegamax(state: chess.Board, color, depth):
            if depth == 0 or state.outcome() is not None:
                return color * self.evaluate(state)

            legalActions = state.legal_moves
            bestScore = float('-inf')

            for action in legalActions:
                state.push(action)
                score = -recursiveNegamax(state, -color, depth - 1)
                bestScore = max(bestScore, score)
                state.pop()

            return bestScore

        color = 1 if gameState.turn else -1
        return negamax(gameState, color=color)


class NegaScout(ChessHelper):
    def getAction(self, gameState: chess.Board):
        def negascout(state: chess.Board, color, depth=self.depth, alpha=float('-inf'), beta=float('inf')):
            if depth == 0 or state.outcome() is not None:
                return None

            legalActions = state.legal_moves
            a = alpha
            b = beta
            isFirstMove = True
            bestAction = None

            for action in legalActions:
                state.push(action)
                score = negascoutRecursion(state, -color, depth - 1, -b, -alpha)
                if a < score < b and depth <= 2 and not isFirstMove:
                    a = -negascoutRecursion(state, -color, depth - 1, -beta, -score)
                state.pop()
                if score > a:
                    a = score
                    bestAction = action

                if a >= beta:
                    return action
                b = a + 1
                isFirstMove = False

            return bestAction

        def negascoutRecursion(state: chess.Board, color, depth, alpha, beta):
            if depth == 0 or state.outcome() is not None:
                return color * self.evaluate(state)

            legalActions = state.legal_moves
            a = alpha
            b = beta
            isFirstMove = True

            for action in legalActions:
                state.push(action)
                score = negascoutRecursion(state, -color, depth - 1, -b, -alpha)
                if a < score < b and depth <= 2 and not isFirstMove:
                    a = -negascoutRecursion(state, -color, depth - 1, -beta, -score)
                state.pop()
                a = max(a, score)
                if a >= beta:
                    return a
                b = a + 1
                isFirstMove = False

            return a

        color = 1 if gameState.turn else -1
        return negascout(gameState, color=color)


class PVS(ChessHelper):

    def getAction(self, gameState: chess.Board):
        def pvs(state: chess.Board, color, depth=self.depth, alpha=float('-inf'), beta=float('inf')):
            if depth == 0 or state.outcome() is not None:
                return None

            legalActions = state.legal_moves
            bestAction = None

            bSearchPv = True
            for action in legalActions:
                state.push(action)
                if bSearchPv:
                    score = -pvsRecursion(state, -color, depth - 1, -beta, -alpha)
                else:
                    score = -pvsRecursion(state, -color, depth - 1, -alpha - 1, -alpha)
                    if score > alpha:
                        score = -pvsRecursion(state, -color, depth - 1, -beta, -alpha)
                state.pop()
                if score >= beta:
                    return action
                if score > alpha:
                    alpha = score
                    bSearchPv = False
                    bestAction = action

            return bestAction

        def pvsRecursion(state: chess.Board, color, depth, alpha, beta):
            if depth == 0 or state.outcome() is not None:
                return color * self.evaluate(state)

            legalActions = state.legal_moves
            bSearchPv = True

            for action in legalActions:
                state.push(action)
                if bSearchPv:
                    score = -pvsRecursion(state, -color, depth - 1, -beta, -alpha)
                else:
                    score = -pvsRecursion(state, -color, depth - 1, -alpha - 1, -alpha)
                    if score > alpha:
                        score = -pvsRecursion(state, -color, depth - 1, -beta, -alpha)
                state.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
                    bSearchPv = False

            return alpha

        color = 1 if gameState.turn else -1
        return pvs(gameState, color=color)

class Game:
    def __init__(self, player, ai, p_color):
        self.gameState = chess.Board()

        if player == 1:
            self.player = NegaMax
        elif player == 2:
            self.player = NegaScout
        elif player == 3:
            self.player = PVS

        if ai == 1:
            self.ai = NegaMax
        elif ai == 2:
            self.ai = NegaScout
        elif ai == 3:
            self.ai = PVS

        self.p_color = p_color

    def nextMove(self):
        turn = self.gameState.turn
        if turn == self.p_color:
            self.makePlayerMove()
        else:
            self.makeAiMove()

    def makeAiMove(self):
        agent = self.ai(2)
        action = agent.getAction(self.gameState.copy())
        self.gameState.push(action)

    def makePlayerMove(self):
        agent = self.player(1)
        action = agent.getAction(self.gameState.copy())
        self.gameState.push(action)

    def isFinished(self):
        return self.gameState.outcome() is not None

# 1 - negamax, 2 - negascout, 3 - pvs

game = Game(2, 1, 1)
i = 1
while not game.isFinished():
    print('========' + str(i) + '========')
    print(game.gameState)
    game.nextMove()
    i += 1
print(game.gameState.outcome())
    
