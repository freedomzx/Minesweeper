from environmentGenerator import *

board = generate(3, 2)
boardInfo = fillInInfo(board, len(board))
printMatrix(board)
for i in range(len(board)):
    for j in range(len(board)):
        #print(str(i) + " " +  str(j))
        print(boardInfo[i][j], end = '                 ')
    print("\n")