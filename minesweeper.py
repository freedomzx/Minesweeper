from environmentGenerator import *
from basicagent import *
from advancedagent import *

board = generate(3, 2)
print(board)
basicagent(board, 2)
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