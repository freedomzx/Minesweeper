from environmentGenerator import *
from basicagent import *
from advancedagent import *

board = generate(16, 40)
printMatrix(board)
basicagent(board, 40)
#advancedagent(board)

# basicTotal = 0
# for i in range(100):
#     board = generate(10, 20)
#     basicTotal += basicagent(board)

# print(basicTotal / 100.0)

# advancedTotal = 0
# for i in range(100):
#     board = generate(10, 20)
#     advancedTotal += advancedagent(board)

# print(advancedTotal / 100.0)