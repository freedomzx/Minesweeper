from environmentGenerator import *
from minesweeper import *
import random

def basicagent(matrix, n):
    #keep track of numbers
    queriedCells = 0
    explosions = 0
    goodQueries = 0

    #matrix of dictionaries contraining info for each cell
    info = fillInInfo(matrix, len(matrix))

    finished = False
    while not finished:
        
        break #TODO this part


#find next cell to query (not hidden and safe), if cant find any choose random unqueried cell
def findNextCell(info):
    returnOnFailure = []
    for i in range(len(info)):
        for j in range(len(info)):
            if not info[i][j]["hidden"] and info[i][j]["safe"]:
                return (i, j, "safe")
            elif info[i][j]["hidden"]:
                returnOnFailure.append((i ,j))

    #if this is returned, its a list of all the hidden cells that you could query, just choose a random one here and return
    num = random.randint(0, len(returnOnFailure)-1)

    return (returnOnFailure[num][0], returnOnFailure[num][1], "randomHidden")
    



