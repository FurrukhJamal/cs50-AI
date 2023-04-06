import tictactoe

def testPlayer(board):
    
    player = tictactoe.player(board)
    print(player)

def testActions(board):
    result = tictactoe.actions(board)
    print(result)

def testResult(board):
    result = tictactoe.result(board, (1,1))
    print(result)

def testWinner():
    board = [[None, "O" , "O"], [None, "O" , None], ["O", None , "X"]]
    result = tictactoe.winner(board)
    print(f"winner is {result}")

    board = [[None, None , None], [None, None , None], [None, None , "X"]]
    result = tictactoe.winner(board)
    print(f"winner returning on board with one move {result}")

def testTerminal():
    board = [["X", "O" , "X"], ["O", "X" , "O"], ["O", "X" , "O"]]
    result = tictactoe.terminal(board)
    print(f"terminal board result : {result}")

def testUtility():
    board = [[None, "O" , "O"], [None, "O" , None], ["O", None , "X"]]
    result = tictactoe.utility(board)
    print(f"winner utility is {result} ")

    board = [["X", "O" , "X"], ["O", "X" , "O"], ["O", "X" , "O"]]
    result = tictactoe.utility(board)
    print(f"winner utility is {result} ")

if __name__ == "__main__":
    board = [[None, "O" , "X"], [None, None , "X"], ["O", "O" , "X"]]
    testPlayer(board)
    testActions(board)
    testResult(board)
    testWinner()
    testTerminal()
    testUtility()
