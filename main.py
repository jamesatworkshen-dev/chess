# Move generation functions for chess
def findPossibleMoves(boardDict):
    #    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    """
    Finds all possible moves for the current position.
    
    Args:
        boardDict (dict): Board state dictionary from turnIntoDict().
    
    Returns:
        list: List of possible moves in algebraic notation.
    """
    moves = []
    illegalMoves = []
    letters = ['a','b','c','d','e','f','g','h']
    numbers = ['8','7','6','5','4','3','2','1']

    ######## 'square' REFERS TO THE STARTING SQUARE OF A PIECE BEFORE THE MOVE
    
    # Determine which side to move
    isWhite = boardDict['turn'] == 'w'
    
    # Iterate through all squares
    for number in numbers:
        for letter in letters:
            square = letter + number
            piece = boardDict[square]
            
            # Skip empty squares and opponent pieces
            if piece == '.' or (isWhite and piece.islower()) or (not isWhite and piece.isupper()):
                continue
            
            # Generate moves based on piece type
            pieceType = piece.lower()
            if pieceType == 'p':
                moves.extend(getPawnMoves(boardDict, square, isWhite, letters, numbers))
            elif pieceType == 'n':
                moves.extend(getKnightMoves(boardDict, square, isWhite, letters, numbers))
            elif pieceType == 'b':
                moves.extend(getBishopMoves(boardDict, square, isWhite, letters, numbers))
            elif pieceType == 'r':
                moves.extend(getRookMoves(boardDict, square, isWhite, letters, numbers))
            elif pieceType == 'q':
                moves.extend(getQueenMoves(boardDict, square, isWhite, letters, numbers))
            elif pieceType == 'k':
                moves.extend(getKingMoves(boardDict, square, isWhite, letters, numbers))


    for index, move in enumerate(moves):
        if isLegalMove(move, boardDict, isWhite, letters, numbers):
            continue
        # remove move from moves and add to illegal moves
        illegalMoves.extend(moves.pop(index))

            

    return moves


def changeToACN(from_square, to_square, is_capture=False, is_check=False):
    """Convert move components into ACN: a8-b8x+ format."""
    notation = f"{from_square}-{to_square}"
    if is_capture:
        notation += "x"
    if is_check:
        notation += "+"
    return notation


def getPawnMoves(boardDict, square, isWhite, letters, numbers):
    moves = []
    col = letters.index(square[0])
    row = numbers.index(square[1])
    direction = -1 if isWhite else 1

    # Forward move
    new_row = row + direction
    if 0 <= new_row < 8:
        new_square = square[0] + numbers[new_row]
        is_check = isCheck(boardDict, new_square, isWhite, 'p', letters, numbers)
        notation = f"{square}-{new_square}"
        if is_check:
            notation += "+"
        moves.append(notation)

    # Diagonal captures
    for col_offset in [-1, 1]:
        new_col = col + col_offset
        new_row = row + direction
        if 0 <= new_col < 8 and 0 <= new_row < 8:
            new_square = letters[new_col] + numbers[new_row]
            target = boardDict[new_square]
            is_check = isCheck(boardDict, new_square, isWhite, 'p', letters, numbers)
            if target != '.' and isCapture(target, isWhite):
                notation = f"{square}-{new_square}x"
                if is_check:
                    notation += "+"
                moves.append(notation)
            elif new_square == boardDict['enpassant']:
                notation = f"{square}-{new_square}x"
                if is_check:
                    notation += "+"
                moves.append(notation)

    return moves


def getKnightMoves(boardDict, square, isWhite, letters, numbers):
    moves = []
    col = letters.index(square[0])
    row = numbers.index(square[1])
    knight_moves = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]

    for dc, dr in knight_moves:
        new_col = col + dc
        new_row = row + dr
        if 0 <= new_col < 8 and 0 <= new_row < 8:
            new_square = letters[new_col] + numbers[new_row]
            target = boardDict[new_square]
            is_check = isCheck(boardDict, new_square, isWhite, 'n', letters, numbers)
            if target == '.':
                notation = f"{square}-{new_square}"
                if is_check:
                    notation += "+"
                moves.append(notation)
            elif isCapture(target, isWhite):
                notation = f"{square}-{new_square}x"
                if is_check:
                    notation += "+"
                moves.append(notation)

    return moves


def getBishopMoves(boardDict, square, isWhite, letters, numbers):
    return get_diagonal_moves(boardDict, square, isWhite, letters, numbers, 'b')


def getRookMoves(boardDict, square, isWhite, letters, numbers):
    return get_straight_moves(boardDict, square, isWhite, letters, numbers, 'r')


def getQueenMoves(boardDict, square, isWhite, letters, numbers):
    return get_diagonal_moves(boardDict, square, isWhite, letters, numbers, 'q') + get_straight_moves(boardDict, square, isWhite, letters, numbers, 'q')


def getKingMoves(boardDict, square, isWhite, letters, numbers):
    moves = []
    col = letters.index(square[0])
    row = numbers.index(square[1])
    king_moves = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    for dc, dr in king_moves:
        new_col = col + dc
        new_row = row + dr
        if 0 <= new_col < 8 and 0 <= new_row < 8:
            new_square = letters[new_col] + numbers[new_row]
            target = boardDict[new_square]
            is_check = isCheck(boardDict, new_square, isWhite, 'k', letters, numbers)
            if target == '.':
                notation = f"{square}-{new_square}"
                if is_check:
                    notation += "+"
                moves.append(notation)
            elif isCapture(target, isWhite):
                notation = f"{square}-{new_square}x"
                if is_check:
                    notation += "+"
                moves.append(notation)

    return moves


def get_diagonal_moves(boardDict, square, isWhite, letters, numbers, piece):
    moves = []
    col = letters.index(square[0])
    row = numbers.index(square[1])
    directions = [(-1,-1), (-1,1), (1,-1), (1,1)]

    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        while 0 <= new_col < 8 and 0 <= new_row < 8:
            new_square = letters[new_col] + numbers[new_row]
            target = boardDict[new_square]
            is_check = isCheck(boardDict, new_square, isWhite, piece, letters, numbers)
            if target == '.':
                notation = f"{square}-{new_square}"
                if is_check:
                    notation += "+"
                moves.append(notation)
            elif isCapture(target, isWhite):
                notation = f"{square}-{new_square}x"
                if is_check:
                    notation += "+"
                moves.append(notation)
                break
            new_col += dc
            new_row += dr

    return moves


def get_straight_moves(boardDict, square, isWhite, letters, numbers, piece):
    moves = []
    col = letters.index(square[0])
    row = numbers.index(square[1])
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        while 0 <= new_col < 8 and 0 <= new_row < 8:
            new_square = letters[new_col] + numbers[new_row]
            target = boardDict[new_square]
            is_check = isCheck(boardDict, new_square, isWhite, piece, letters, numbers)
            if target == '.':
                notation = f"{square}-{new_square}"
                if is_check:
                    notation += "+"
                moves.append(notation)
            elif isCapture(target, isWhite):
                notation = f"{square}-{new_square}x"
                if is_check:
                    notation += "+"
                moves.append(notation)
                break
            new_col += dc
            new_row += dr

    return moves

def isLegalMove(move, oldBoardDictBeforeTheMove, isWhite, letters, numbers):
    from_square = move.split('-')[0]
    newBoardDictAfterTheMove = makeMove(move, oldBoardDictBeforeTheMove, isWhite, letters, numbers)
    return isLegalBoard(newBoardDictAfterTheMove, move, isWhite, from_square, letters, numbers)


def makeMove(move, board, isWhite, letters, numbers):
    # parse ACN move: e2-e4, e2-d3x, a7-a8+
    is_capture = 'x' in move
    is_check = move.endswith('+')

    if is_check:
        move = move[:-1]

    from_square, rest = move.split('-', 1)
    to_square = rest

    if is_capture and to_square.endswith('x'):
        to_square = to_square[:-1]

    piece = board[from_square]
    board[from_square] = '.'
    board[to_square] = piece

    return board
    
def isLegalBoard(newBoardDictAfterTheMove, move, isWhite, square, letters, numbers):
    # After the move, the turn belongs to the opposite side.
    next_turn = 'b' if isWhite else 'w'

    # If the side to move is in check, board state is illegal (check must be addressed).
    if isKingInCheck(newBoardDictAfterTheMove, next_turn, letters, numbers):
        return False

    return True

def isSquareAttacked(boardDict, square, byWhite, letters, numbers):
    # Tests whether square is attacked by any piece of attacker color.
    for number in numbers:
        for letter in letters:
            from_square = letter + number
            piece = boardDict[from_square]
            if piece == '.':
                continue

            if byWhite and not piece.isupper():
                continue
            if not byWhite and not piece.islower():
                continue

            piece_type = piece.lower()
            if piece_type == 'p':
                moves = getPawnMoves(boardDict, from_square, byWhite, letters, numbers)
            elif piece_type == 'n':
                moves = getKnightMoves(boardDict, from_square, byWhite, letters, numbers)
            elif piece_type == 'b':
                moves = getBishopMoves(boardDict, from_square, byWhite, letters, numbers)
            elif piece_type == 'r':
                moves = getRookMoves(boardDict, from_square, byWhite, letters, numbers)
            elif piece_type == 'q':
                moves = getQueenMoves(boardDict, from_square, byWhite, letters, numbers)
            elif piece_type == 'k':
                moves = getKingMoves(boardDict, from_square, byWhite, letters, numbers)
            else:
                continue

            for m in moves:
                dest = m.split('-', 1)[1]
                dest = dest.rstrip('+')
                if dest.endswith('x'):
                    dest = dest[:-1]
                if dest == square:
                    return True

    return False

def isKingInCheck(boardDict, colorToMove, letters, numbers):
    king_piece = 'K' if colorToMove == 'w' else 'k'
    king_square = None
    for square, piece in boardDict.items():
        if square in ['turn', 'castling', 'enpassant', 'halfmoves', 'fullmoves']:
            continue
        if piece == king_piece:
            king_square = square
            break

    if king_square is None:
        # No king found for color - illegal board
        return True

    attackerIsWhite = (colorToMove == 'b')
    return isSquareAttacked(boardDict, king_square, attackerIsWhite, letters, numbers)

def isCapture(target, isWhite):
    return (isWhite and target.islower()) or (not isWhite and target.isupper())

def isCheck(boardDict, target, isWhite, piece, letters, numbers):
    # NOTE: check detection currently simplified to avoid recursive logic;
    # returns False until a full legal check algorithm is implemented.
    return False
            
def isDiscoveredCheck(target, isWhite, piece, letters, numbers):
    pass

            
def isDoubleCheck(target, isWhite, piece, letters, numbers):
    # if isDicoveredCheck and isCheck:
    #    return True
    # return False
    pass

def isMate(move):
    pass

def findBestMove(possibleGoodMoves):
    pass

def findPossibleGoodMoves(possibleMoves):
    list = [] #[[move, type], [move, type], [move, type], [move, type], [move, type], [move, type]]
    for move in possibleMoves:
        if move not in list:
            if isTake(move):
                list.append(move, 'take')
            if isAttack(move):
                list.append(move, 'attackPiece')
            if isDefend(move):
                list.append(move, 'defendPiece')
            if isCastle(move):
                list.append(move, 'castle')
            if isDevelop(move):
                list.append(move, 'develop')
            if attackKing(move):
                list.append(move, 'attackKing')
            if isMoveStrongPieceTowardKing(move):
                list.append(move, 'prepareAttackKing')
            if isMovePawnIntoCentre(move):
                list.append(move, 'controlCentre')
            if isEvade(move):
                list.append(move, 'evadeAttack')
    return list

def isTake(move):
    pass

def isAttack(move):
    pass

def isDefend(move):
    pass

def isCastle(move):
    pass

def isDevelop(move):
    pass

def attackKing(move):
    pass

def isMoveStrongPieceTowardKing(move):
    pass

def isMovePawnIntoCentre(move):
    pass

def isEvade(move):
    pass

def turnIntoDict(fen):
    parts = fen.split(' ')
    rows = parts[0].split('/')
    
    data = rows + parts[1:]

    letters = ['a','b','c','d','e','f','g','h']
    numbers = ['8','7','6','5','4','3','2','1']

    justRows = data[:8]
    newDict = {}

    for row, number in enumerate(numbers):
        index = 0
        numberCounter = 0

        for letter in letters:
            if numberCounter > 0:
                newDict[(letter + number)] = '.'
                numberCounter -= 1
            else:
                if justRows[row][index] in numbers:
                    newDict[(letter + number)] = '.'
                    numberCounter = int(justRows[row][index]) - 1
                else:
                    newDict[(letter + number)] = justRows[row][index]

                index += 1
    
    newDict['turn'] = data[8]
    newDict['castling'] = data[9]
    newDict['enpassant'] = data[10]
    newDict['halfmoves'] = data[11]
    newDict['fullmoves'] = data[12]
    
    return newDict

boardInput = input('Custom position?\n\'N\' for no, {FEN} for yes. ')
wordsMeaningNo = ['N', 'NO']

if boardInput.upper() in wordsMeaningNo:
    boardInput = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

boardDict = turnIntoDict(boardInput)
possibleMoves = findPossibleMoves(boardDict)

print(possibleMoves)

'''
possibleGoodMoves = findPossibleGoodMoves(possibleMoves)
bestMove = findBestMove(possibleGoodMoves)

print(bestMove)
'''

