from environmentGenerator import *
from basicagent import *
from advancedagent import *

board = generate(8, 16)
#printMatrix(board)
#basicagent(board, 40)
#advancedagent(board, 16)

# basicTotal = 0
# for i in range(150):
#     board = generate(30, 200)
#     basicTotal += basicagent(board, 200)

# advancedTotal = 0
# for i in range(150):
#     board = generate(30, 200)
#     advancedTotal += advancedagent(board, 200)

# print(basicTotal / 150.0)
# print(advancedTotal / 150.0)

density = 15
while density < 300:
    basicTotal = 0
    for i in range(200):
        board = generate(30, density)
        basicTotal += basicagent(board, density)

    advancedTotal = 0
    for i in range(200):
        board = generate(30, density)
        advancedTotal += advancedagent(board, density)

    print("Density of {}: basic score: {} - advanced score: {}".format(density, str(float(basicTotal / 200.0)), str(float(advancedTotal / 200.0))))
    density += 15