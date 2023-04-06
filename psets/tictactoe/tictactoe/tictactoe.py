"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counterE = 0
    counterX = 0
    counterO = 0

    for row in board:
        for cell in row:
            if cell == EMPTY:
                counterE += 1
            if cell == X:
                counterX += 1
            if cell == O:
                counterO += 1
    
    if counterE == 9:
        return X 
    elif counterX > counterO :
        return O 
    else : 
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                result.add((i, j))
    
    return result
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # print(f"original board at start of result: {board}")
    # print(f"action[0] : {action[0]}")
    if action[0] > 2 or action[0] < 0 or action[1] > 2 or action[1] < 0:
        # print("hitting")
        raise Exception("invalid move")

    copyBoard = copy.deepcopy(board)
    move = player(copyBoard)
    # print(f"value at given location in board: {copyBoard[action[0]][action[1]]}")
    copyBoard[action[0]][action[1]] = move 
    # print(f"original board at end of result: {board}")
    return copyBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # checks for X
    if checkHorizontalWinner(board, X):
        return X
    elif checkVerticleWinner(board, X):
        return X
    elif checkdiagnolWinner(board, X):
        return X
    # checks for Y
    elif checkHorizontalWinner(board, O):
        return O 
    elif checkVerticleWinner(board, O):
        return O
    elif checkdiagnolWinner(board, O):
        return O
    elif isBoardFull(board):
        return None
      


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    else:
        counterEmpty = 0
        for row in board:
            for cell in row:
                if cell == EMPTY:
                    counterEmpty += 1
        if counterEmpty == 0:
            return True

    return False 

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    Cboard = copy.deepcopy(board)
    # print(f"Cboard at start of minmax. {Cboard}")
    if terminal(Cboard):
        # print("board hitting terminal condition")
        return utility(board)
    else:
        moves = actions(Cboard)
        playerTurn = player(Cboard)
        
        if playerTurn == X:
            results = []
            for move in moves:
                # print(f"BOARD AT START OF X iteration: {Cboard}")
                # print(f"move in X : {move}")
                # copyBoard = copy.deepcopy(board)
                score = minValue(result(Cboard, move))
                results.append((score, move))
                Cboard = copy.deepcopy(board)
                # print(f"SCORE in X: {score}")
                # print(f"Original Board at the end of X iteration : {board}")
                # print(f"CBoard at the end of first X iteration : {Cboard}")
                if score == 1:
                    break 
                
            # print(f"results in player X condition : {results}")
            maxVal = -10000
            optimalMove = None
            for data in results:
                # print(f"data[0] type: {type(data[0])}")
                if data[0] > maxVal:
                    maxVal = data[0]
                    optimalMove = data[1]
            
            return optimalMove

        if playerTurn == O:
            results = []
            for move in moves:
                # print(f"move in O : {move}")
                # copyBoard = copy.deepcopy(board)
                # print(f"CBoard at the start of O iteration : {Cboard}")
                score = maxValue(result(Cboard, move))
                # print(f"SCORE in Y: {score}")
                results.append((score, move))
                Cboard = copy.deepcopy(board)
                # print(f"Original Board at the end of O iteration : {board}")
                # print(f"Cboard at the end of first O iteration : {Cboard}")
                if score == -1:
                    break
            # print(f"results in player O condition : {results}")
            minVal = 10000
            optimalMove = None
            for data in results:
                # print(f"data : {data}")
                # print(f"data[0] : {data[0]}")
                if data[0] < minVal:
                    minVal = data[0]
                    optimalMove = data[1]
                    
            
            return optimalMove

def minValue(board):
    cBoard = copy.deepcopy(board)
    if terminal(cBoard):
        return utility(cBoard)
    v = 1000
    for move in actions(cBoard):
        v = min(v, maxValue(result(cBoard, move)))
        CBoard = copy.deepcopy(board)
        if v == -1:
            break
    return v

def maxValue(board):
    cBoard = copy.deepcopy(board)
    if terminal(cBoard):
        return utility(cBoard)
    v = -1000
    for move in actions(cBoard):
        v = max(v, minValue(result(cBoard, move)))
        CBoard = copy.deepcopy(board)
        if v == 1:
            break
    return v


def isBoardFull(board):
    counterEmpty = 0
    for row in board:
        for cell in row:
            if cell == EMPTY:
                counterEmpty += 1
    if counterEmpty == 0:
        return True
    return False



    

def checkHorizontalWinner(board, move):
    for row in board:
        counter = 0
        for cell in row:
            if cell == move:
                counter += 1
        
        if counter == 3:
            return True
    return False 

def checkVerticleWinner(board, move):
    for col in range(3):
        counter = 0
        for y in range(3):
            if board[y][col] == move:
                counter += 1
        if counter == 3:
            return True

    return False  
                
def checkdiagnolWinner(board, move):
    if (board[0][0] == move and board[1][1] == move and board[2][2] == move):
        return True
    elif (board[0][2] == move and board[1][1] == move and board[2][0] == move):
        return True
    else:
        False

      