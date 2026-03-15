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

    legal_moves = []
    for move in moves:
        if isLegalMove(move, boardDict, isWhite, letters, numbers):
            legal_moves.append(move)

    return legal_moves


def changeToACN(from_square, to_square, is_capture=False, is_check=False):
    """Convert move components into ACN: from a7-b8x+ format to axb8+"""
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

    def push(move):
        notation = move
        if isCheck(move, boardDict, isWhite, letters, numbers):
            notation += '+'
        moves.append(notation)

    # Forward move
    new_row = row + direction
    if 0 <= new_row < 8:
        new_square = square[0] + numbers[new_row]
        if boardDict[new_square] == '.':
            if (isWhite and new_row == 0) or (not isWhite and new_row == 7):
                for promo in ['q', 'r', 'b', 'n']:
                    push(f"{square}-{new_square}={promo}")
            else:
                push(f"{square}-{new_square}")

            # initial double push
            start_row = 6 if isWhite else 1
            if row == start_row:
                jump_row = row + 2 * direction
                jump_square = square[0] + numbers[jump_row]
                if boardDict[jump_square] == '.':
                    push(f"{square}-{jump_square}")

    # Diagonal captures
    for col_offset in (-1, 1):
        new_col = col + col_offset
        new_row = row + direction
        if 0 <= new_col < 8 and 0 <= new_row < 8:
            new_square = letters[new_col] + numbers[new_row]
            target = boardDict[new_square]
            if target != '.' and isCapture(target, isWhite):
                if (isWhite and new_row == 0) or (not isWhite and new_row == 7):
                    for promo in ['q', 'r', 'b', 'n']:
                        push(f"{square}-{new_square}x={promo}")
                else:
                    push(f"{square}-{new_square}x")
            elif new_square == boardDict.get('enpassant', ''):
                push(f"{square}-{new_square}x")

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
            if target == '.':
                notation = f"{square}-{new_square}"
                if isCheck(notation, boardDict, isWhite, letters, numbers):
                    notation += '+'
                moves.append(notation)
            elif isCapture(target, isWhite):
                notation = f"{square}-{new_square}x"
                if isCheck(notation, boardDict, isWhite, letters, numbers):
                    notation += '+'
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
            if target == '.':
                notation = f"{square}-{new_square}"
                if isCheck(notation, boardDict, isWhite, letters, numbers):
                    notation += '+'
                moves.append(notation)
            elif isCapture(target, isWhite):
                notation = f"{square}-{new_square}x"
                if isCheck(notation, boardDict, isWhite, letters, numbers):
                    notation += '+'
                moves.append(notation)

    # Castling (naive rule set, assumes no interference in path and rights recorded in boardDict['castling'])
    rights = boardDict.get('castling', '')
    if isWhite and square == 'e1':
        if 'K' in rights and boardDict.get('f1', '.') == '.' and boardDict.get('g1', '.') == '.':
            if not isKingInCheck(boardDict, 'w', letters, numbers) and not isSquareAttacked(boardDict, 'f1', False, letters, numbers) and not isSquareAttacked(boardDict, 'g1', False, letters, numbers):
                moves.append('e1-g1')
        if 'Q' in rights and boardDict.get('d1', '.') == '.' and boardDict.get('c1', '.') == '.' and boardDict.get('b1', '.') == '.':
            if not isKingInCheck(boardDict, 'w', letters, numbers) and not isSquareAttacked(boardDict, 'd1', False, letters, numbers) and not isSquareAttacked(boardDict, 'c1', False, letters, numbers):
                moves.append('e1-c1')
    if not isWhite and square == 'e8':
        if 'k' in rights and boardDict.get('f8', '.') == '.' and boardDict.get('g8', '.') == '.':
            if not isKingInCheck(boardDict, 'b', letters, numbers) and not isSquareAttacked(boardDict, 'f8', True, letters, numbers) and not isSquareAttacked(boardDict, 'g8', True, letters, numbers):
                moves.append('e8-g8')
        if 'q' in rights and boardDict.get('d8', '.') == '.' and boardDict.get('c8', '.') == '.' and boardDict.get('b8', '.') == '.':
            if not isKingInCheck(boardDict, 'b', letters, numbers) and not isSquareAttacked(boardDict, 'd8', True, letters, numbers) and not isSquareAttacked(boardDict, 'c8', True, letters, numbers):
                moves.append('e8-c8')

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
            if target == '.':
                notation = f"{square}-{new_square}"
                if isCheck(notation, boardDict, isWhite, letters, numbers):
                    notation += '+'
                moves.append(notation)
            elif isCapture(target, isWhite):
                notation = f"{square}-{new_square}x"
                if isCheck(notation, boardDict, isWhite, letters, numbers):
                    notation += '+'
                moves.append(notation)
                break
            else:
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
            if target == '.':
                notation = f"{square}-{new_square}"
                if isCheck(notation, boardDict, isWhite, letters, numbers):
                    notation += '+'
                moves.append(notation)
            elif isCapture(target, isWhite):
                notation = f"{square}-{new_square}x"
                if isCheck(notation, boardDict, isWhite, letters, numbers):
                    notation += '+'
                moves.append(notation)
                break
            else:
                break
            new_col += dc
            new_row += dr

    return moves

def isLegalMove(move, oldBoardDictBeforeTheMove, isWhite, letters, numbers):
    from_square = move.split('-')[0]
    newBoardDictAfterTheMove = makeMove(move, oldBoardDictBeforeTheMove, isWhite, letters, numbers)
    return isLegalBoard(newBoardDictAfterTheMove, move, isWhite, from_square, letters, numbers)


def makeMove(move, board, isWhite, letters, numbers):
    # parse move: e2-e4, e2-d3x, a7-a8+
    is_capture = 'x' in move
    is_check = move.endswith('+')

    if is_check:
        move = move[:-1]

    from_square, rest = move.split('-', 1)
    to_square = rest

    if is_capture and to_square.endswith('x'):
        to_square = to_square[:-1]

    new_board = board.copy()
    piece = new_board[from_square]

    # en passant cleanup by default unless set below
    new_board['enpassant'] = '-'

    # handle en passant capture
    if piece.lower() == 'p':
        if board.get('enpassant') == to_square and board.get(to_square, '.') == '.':
            # remove the pawn behind the target square
            direction = 1 if isWhite else -1
            captured_square = to_square[0] + numbers[numbers.index(to_square[1]) + direction]
            new_board[captured_square] = '.'

    new_board[from_square] = '.'
    new_board[to_square] = piece

    # handle pawn two-square advance en passant target
    if piece.lower() == 'p':
        from_row = numbers.index(from_square[1])
        to_row = numbers.index(to_square[1])
        if abs(from_row - to_row) == 2:
            mid_row = (from_row + to_row) // 2
            new_board['enpassant'] = to_square[0] + numbers[mid_row]

    # handle castling rook move
    if piece.lower() == 'k':
        if from_square == 'e1' and to_square == 'g1':
            new_board['h1'] = '.'
            new_board['f1'] = 'R'
        elif from_square == 'e1' and to_square == 'c1':
            new_board['a1'] = '.'
            new_board['d1'] = 'R'
        elif from_square == 'e8' and to_square == 'g8':
            new_board['h8'] = '.'
            new_board['f8'] = 'r'
        elif from_square == 'e8' and to_square == 'c8':
            new_board['a8'] = '.'
            new_board['d8'] = 'r'

    return new_board
    
def isLegalBoard(newBoardDictAfterTheMove, move, isWhite, square, letters, numbers):
    # After the move, the turn belongs to the opposite side. To be legal, the side that just moved must not be in check.
    side_just_moved = 'w' if isWhite else 'b'

    if isKingInCheck(newBoardDictAfterTheMove, side_just_moved, letters, numbers):
        return False

    return True

def isSquareAttacked(boardDict, square, byWhite, letters, numbers):
    # Tests whether square is attacked by any piece of attacker color without using isCheck recursion.
    target_col = letters.index(square[0])
    target_row = numbers.index(square[1])

    # Pawn attacks
    pawn_dir = -1 if byWhite else 1
    for dc in (-1, 1):
        c = target_col + dc
        r = target_row + pawn_dir
        if 0 <= c < 8 and 0 <= r < 8:
            attacker = boardDict[letters[c] + numbers[r]]
            if byWhite and attacker == 'P':
                return True
            if not byWhite and attacker == 'p':
                return True

    # Knight attacks
    knight_moves = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
    for dc, dr in knight_moves:
        c = target_col + dc
        r = target_row + dr
        if 0 <= c < 8 and 0 <= r < 8:
            attacker = boardDict[letters[c] + numbers[r]]
            if byWhite and attacker == 'N':
                return True
            if not byWhite and attacker == 'n':
                return True

    # King adjacent
    for dc in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if dc == 0 and dr == 0:
                continue
            c = target_col + dc
            r = target_row + dr
            if 0 <= c < 8 and 0 <= r < 8:
                attacker = boardDict[letters[c] + numbers[r]]
                if byWhite and attacker == 'K':
                    return True
                if not byWhite and attacker == 'k':
                    return True

    # Sliding pieces
    directions = [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)]
    for dc, dr in directions:
        c = target_col + dc
        r = target_row + dr
        while 0 <= c < 8 and 0 <= r < 8:
            attacker = boardDict[letters[c] + numbers[r]]
            if attacker != '.':
                if byWhite:
                    if attacker == 'Q':
                        return True
                    if attacker == 'B' and abs(dc) == abs(dr):
                        return True
                    if attacker == 'R' and (dc == 0 or dr == 0):
                        return True
                else:
                    if attacker == 'q':
                        return True
                    if attacker == 'b' and abs(dc) == abs(dr):
                        return True
                    if attacker == 'r' and (dc == 0 or dr == 0):
                        return True
                break
            c += dc
            r += dr

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
        return 'illegal'

    attackerIsWhite = (colorToMove == 'b')
    return isSquareAttacked(boardDict, king_square, attackerIsWhite, letters, numbers)

def isCapture(target, isWhite):
    return (isWhite and target.islower()) or (not isWhite and target.isupper())

def isCheck(move, boardDict, isWhite, letters, numbers):
    # Detect whether `move` gives check to opponent king.
    new_board = makeMove(move, boardDict, isWhite, letters, numbers)
    next_turn = 'b' if isWhite else 'w'
    return isKingInCheck(new_board, next_turn, letters, numbers)


def getAttackers(boardDict, square, byWhite, letters, numbers):
    attacker_squares = []
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
                col = letters.index(from_square[0])
                row = numbers.index(from_square[1])
                direction = -1 if byWhite else 1
                for dc in (-1, 1):
                    nc = col + dc
                    nr = row + direction
                    if 0 <= nc < 8 and 0 <= nr < 8:
                        if letters[nc] + numbers[nr] == square:
                            attacker_squares.append(from_square)
            elif piece_type == 'n':
                knight_moves = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
                col = letters.index(from_square[0]); row = numbers.index(from_square[1])
                for dc, dr in knight_moves:
                    nc = col + dc
                    nr = row + dr
                    if 0 <= nc < 8 and 0 <= nr < 8:
                        if letters[nc] + numbers[nr] == square:
                            attacker_squares.append(from_square)
            elif piece_type == 'b':
                for direction in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                    c = letters.index(from_square[0]) + direction[0]
                    r = numbers.index(from_square[1]) + direction[1]
                    while 0 <= c < 8 and 0 <= r < 8:
                        curr = letters[c] + numbers[r]
                        if curr == square:
                            attacker_squares.append(from_square)
                            break
                        if boardDict[curr] != '.':
                            break
                        c += direction[0]; r += direction[1]
            elif piece_type == 'r':
                for direction in [(-1,0), (1,0), (0,-1), (0,1)]:
                    c = letters.index(from_square[0]) + direction[0]
                    r = numbers.index(from_square[1]) + direction[1]
                    while 0 <= c < 8 and 0 <= r < 8:
                        curr = letters[c] + numbers[r]
                        if curr == square:
                            attacker_squares.append(from_square)
                            break
                        if boardDict[curr] != '.':
                            break
                        c += direction[0]; r += direction[1]
            elif piece_type == 'q':
                for direction in [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)]:
                    c = letters.index(from_square[0]) + direction[0]
                    r = numbers.index(from_square[1]) + direction[1]
                    while 0 <= c < 8 and 0 <= r < 8:
                        curr = letters[c] + numbers[r]
                        if curr == square:
                            attacker_squares.append(from_square)
                            break
                        if boardDict[curr] != '.':
                            break
                        c += direction[0]; r += direction[1]
            elif piece_type == 'k':
                for dc in (-1,0,1):
                    for dr in (-1,0,1):
                        if dc == 0 and dr == 0:
                            continue
                        c = letters.index(from_square[0]) + dc
                        r = numbers.index(from_square[1]) + dr
                        if 0 <= c < 8 and 0 <= r < 8 and letters[c] + numbers[r] == square:
                            attacker_squares.append(from_square)

    return attacker_squares


def countAttackers(boardDict, square, byWhite, letters, numbers):
    return len(getAttackers(boardDict, square, byWhite, letters, numbers))


def isDiscoveredCheck(move, boardDict, isWhite, letters, numbers):
    if not isCheck(move, boardDict, isWhite, letters, numbers):
        return False

    from_square, to_square = move.rstrip('+').split('-', 1)
    piece = boardDict[from_square]

    board_after = makeMove(move, boardDict, isWhite, letters, numbers)
    next_turn = 'b' if isWhite else 'w'

    king_sq = None
    king_piece = 'K' if next_turn == 'w' else 'k'
    for sq, p in board_after.items():
        if sq in ['turn', 'castling', 'enpassant', 'halfmoves', 'fullmoves']:
            continue
        if p == king_piece:
            king_sq = sq
            break

    if king_sq is None:
        return False

    attackers = getAttackers(board_after, king_sq, isWhite, letters, numbers)
    if not attackers:
        return False

    # If the moved piece is one of the attackers, direct check; otherwise discovered.
    if to_square in attackers:
        return len(attackers) > 1
    return True


def isDoubleCheck(move, boardDict, isWhite, letters, numbers):
    if not isCheck(move, boardDict, isWhite, letters, numbers):
        return False

    board_after = makeMove(move, boardDict, isWhite, letters, numbers)
    next_turn = 'b' if isWhite else 'w'

    king_sq = None
    king_piece = 'K' if next_turn == 'w' else 'k'
    for sq, p in board_after.items():
        if sq in ['turn', 'castling', 'enpassant', 'halfmoves', 'fullmoves']:
            continue
        if p == king_piece:
            king_sq = sq
            break

    if king_sq is None:
        return False

    attackers = getAttackers(board_after, king_sq, isWhite, letters, numbers)
    return len(attackers) >= 2

    board_after = makeMove(move, boardDict, isWhite, letters, numbers)
    opp_color = 'b' if isWhite else 'w'
    king_piece = 'K' if opp_color == 'w' else 'k'
    king_square = None
    for sq, p in board_after.items():
        if sq in ['turn', 'castling', 'enpassant', 'halfmoves', 'fullmoves']:
            continue
        if p == king_piece:
            king_square = sq
            break

    if king_square is None:
        return False

    attacker_color = isWhite
    return countAttackers(board_after, king_square, attacker_color, letters, numbers) >= 2


def isMate(move, boardDict, isWhite, letters, numbers):
    board_after = makeMove(move, boardDict, isWhite, letters, numbers)
    board_after['turn'] = 'b' if isWhite else 'w'

    # Must be check immediately after the move
    if not isKingInCheck(board_after, board_after['turn'], letters, numbers):
        return False

    next_moves = findPossibleMoves(board_after)
    return len(next_moves) == 0

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
    return 'x' in move


def isAttack(move):
    # attack may include capture or putting opponent in check
    return 'x' in move or '+' in move


def isDefend(move):
    # stub: no board context, approximate as not in capture and not castling
    return 'x' not in move and '-' in move and 'o-o' not in move.lower()


def isCastle(move):
    return move in ['e1-g1', 'e1-c1', 'e8-g8', 'e8-c8']


def isDevelop(move):
    return move.startswith(('b','g','n','c','d','f'))


def attackKing(move):
    return '+' in move


def isMoveStrongPieceTowardKing(move):
    # basic heuristic: queen/rook/bishop in move text
    return any(p in move for p in ['q', 'r', 'b', 'Q', 'R', 'B'])


def isMovePawnIntoCentre(move):
    if len(move) < 5:
        return False
    to_sq = move.split('-')[1].rstrip('+').rstrip('x')
    return to_sq in ['d4', 'd5', 'e4', 'e5']


def isEvade(move):
    # move out of check indicated by removing '+' from one move; no context available
    return '-' in move and '+' not in move

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

if __name__ == '__main__':
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


