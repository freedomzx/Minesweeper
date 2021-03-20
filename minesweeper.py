from environmentGenerator import *
from basicagent import *

board = generate(10, 20)
basicagent(board)
# board = generate(2, 1)
# info = fillInInfo(board, 2)

# for i in range(len(info)):
#     for j in range(len(info)):
#         print(info[i][j], end = '  ')
#     print("\n")