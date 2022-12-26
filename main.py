import chess

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

