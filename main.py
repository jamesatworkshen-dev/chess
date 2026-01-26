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
    letters = ['a','b','c','d','e','f','g','h']
    numbers = ['8','7','6','5','4','3','2','1']
    
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

    return moves


def getPawnMoves(boardDict, square, isWhite, letters, numbers):
    moves = []
    col = letters.index(square[0])
    row = numbers.index(square[1])
    direction = -1 if isWhite else 1
    
    # Forward move
    new_row = row + direction
    if 0 <= new_row < 8:
        new_square = square[0] + numbers[new_row]
        if boardDict[new_square] == '.':
            moves.append(f"{square}-{new_square}")
    
    # Diagonal captures
    for col_offset in [-1, 1]:
        new_col = col + col_offset
        new_row = row + direction
        if 0 <= new_col < 8 and 0 <= new_row < 8:
            new_square = letters[new_col] + numbers[new_row]
            target = boardDict[new_square]
            if target != '.' and ((isWhite and target.islower()) or (not isWhite and target.isupper())):
                moves.append(f"{square}-{new_square}")
    
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
            if target == '.' or ((isWhite and target.islower()) or (not isWhite and target.isupper())):
                moves.append(f"{square}-{new_square}")
    
    return moves


def getBishopMoves(boardDict, square, isWhite, letters, numbers):
    return get_diagonal_moves(boardDict, square, isWhite, letters, numbers)


def getRookMoves(boardDict, square, isWhite, letters, numbers):
    return get_straight_moves(boardDict, square, isWhite, letters, numbers)


def getQueenMoves(boardDict, square, isWhite, letters, numbers):
    return get_diagonal_moves(boardDict, square, isWhite, letters, numbers) + get_straight_moves(boardDict, square, isWhite, letters, numbers)


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
            if target == '.' or ((isWhite and target.islower()) or (not isWhite and target.isupper())):
                moves.append(f"{square}-{new_square}")
    
    return moves


def get_diagonal_moves(boardDict, square, isWhite, letters, numbers):
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
                moves.append(f"{square}-{new_square}")
            elif (isWhite and target.islower()) or (not isWhite and target.isupper()):
                moves.append(f"{square}-{new_square}")
                break
            else:
                break
            new_col += dc
            new_row += dr
    
    return moves


def get_straight_moves(boardDict, square, isWhite, letters, numbers):
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
                moves.append(f"{square}-{new_square}")
            elif (isWhite and target.islower()) or (not isWhite and target.isupper()):
                moves.append(f"{square}-{new_square}")
                break
            else:
                break
            new_col += dc
            new_row += dr
    
    return moves


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

    for letter in letters:
        for number in numbers:
            if (letter + '-file') in newDict:
                newDict[(letter + '-file')] += newDict[(letter + number)]
            else:
                newDict[(letter + '-file')] = newDict[(letter + number)]
    
    for number in numbers:
        for letter in letters:
            if ('rank-' + number) in newDict:
                newDict[('rank-' + number)] += newDict[(letter + number)]
            else:
                newDict[('rank-' + number)] = newDict[(letter + number)]
    
    return newDict

boardInput = input('Custom position?\n\'N\' for no, {FEN} for yes. ')
wordsMeaningNo = ['N', 'NO']

if boardInput.upper() in wordsMeaningNo:
    boardInput = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

boardDict = turnIntoDict(boardInput)
possibleMoves = findPossibleMoves(boardDict)

print(possibleMoves)

