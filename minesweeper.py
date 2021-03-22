from environmentGenerator import *
from basicagent import *
from advancedagent import *

#board = generate(16, 40)
#printMatrix(board)
#basicagent(board, 40)
#advancedagent(board, 40)

basicTotal = 0
for i in range(150):
    board = generate(16, 40)
    basicTotal += basicagent(board, 40)

advancedTotal = 0
for i in range(150):
    board = generate(16, 40)
    advancedTotal += advancedagent(board, 40)

print(basicTotal / 150.0)
print(advancedTotal / 150.0)