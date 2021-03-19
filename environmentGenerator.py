import random
import pygame

#check if an index is within the matrix
def checkValidIndex(d, row, col):
    return (row >= 0 and row < d) and (col >= 0 and col < d)
    
#check if an index is a mine
def checkMine(d, row, col, matrix):
    return checkValidIndex(d, row, col) and matrix[row][col] == "m"

#make a matrix of information for each index
def fillInInfo(matrix, d):
    toReturn = []
    for i in range(len(matrix)):
        toAdd = []
        for j in range(len(matrix)):
            dic = {}

            #keep track of whether or not the square has been directly searched yet
            dic["safe"] = "inconclusive"
            dic["status"] = "unqueried"

            #if safe, the number of mines surrounding it indicated by the clue
            dic["surrounding_clued_mines"] = ""
            if matrix[i][j] == "m":
                dic["surrounding_clued_mines"] = "m"
            else:
                dic["surrounding_clued_mines"] = matrix[i][j]

            #the number of safe squares identified around it, and number of mines around. also fill in hidden squares by counting valid squares around index
            dic["surrounding_safe_squares"] = 0
            dic["surrounding_mines"] = 0
            dic["surrounding_hidden_squares"] = 0

            #northwest
            if checkValidIndex(d, i-1, j-1):
                dic["surrounding_hidden_squares"]+=1
            #west
            if checkValidIndex(d, i, j-1):
                dic["surrounding_hidden_squares"]+=1
            #southwest
            if checkValidIndex(d, i+1, j-1):
                dic["surrounding_hidden_squares"]+=1
            #north
            if checkValidIndex(d, i-1, j):
                dic["surrounding_hidden_squares"]+=1
            #south
            if checkValidIndex(d, i+1, j):
                dic["surrounding_hidden_squares"]+=1
            #northesat
            if checkValidIndex(d, i-1, j+1):
                dic["surrounding_hidden_squares"]+=1
            #east
            if checkValidIndex(d, i, j+1):
                dic["surrounding_hidden_squares"]+=1
            #southeast
            if checkValidIndex(d, i+1, j+1):
                dic["surrounding_hidden_squares"]+=1
            toAdd.append(dic)
        toReturn.append(toAdd)

    return toReturn

#generate a d x d environment with n mines in it.  only places mines, does not put in numbers yet.
def generate(d, n):
    minesRemaining = n
    toReturn = []
    for i in range(d):
        addLine = []
        for j in range(d):
            addLine.append(0)
        toReturn.append(addLine)

    cease = False
    while minesRemaining > 0:
        if cease:
            break
        for i in range(d):
            if cease:
                break
            for j in range(d):
                if toReturn[i][j] != "m" and random.randint(1, 100) <= 5:
                    #fill in mines by chance, update numbers of indices surrounding the mine
                    toReturn[i][j] = "m"
                    #northwest
                    if checkValidIndex(d, i-1, j-1) and toReturn[i-1][j-1] != "m":
                        toReturn[i-1][j-1]+=1
                    #west
                    if checkValidIndex(d, i, j-1) and toReturn[i][j-1] != "m":
                        toReturn[i][j-1]+=1
                    #southwest
                    if checkValidIndex(d, i+1, j-1) and toReturn[i+1][j-1] != "m":
                        toReturn[i+1][j-1]+=1
                    #north
                    if checkValidIndex(d, i-1, j) and toReturn[i-1][j] != "m":
                        toReturn[i-1][j]+=1
                    #south
                    if checkValidIndex(d, i+1, j) and toReturn[i+1][j] != "m":
                        toReturn[i+1][j]+=1
                    #northesat
                    if checkValidIndex(d, i-1, j+1) and toReturn[i-1][j+1] != "m":
                        toReturn[i-1][j+1]+=1
                    #east
                    if checkValidIndex(d, i, j+1) and toReturn[i][j+1] != "m":
                        toReturn[i][j+1]+=1
                    #southeast
                    if checkValidIndex(d, i+1, j+1) and toReturn[i+1][j+1] != "m":
                        toReturn[i+1][j+1]+=1
                    minesRemaining -= 1
                    if minesRemaining == 0:
                        cease = True
                    if cease:
                        break

    return toReturn

def printMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print(str(matrix[i][j]) + " ", end='')
        print("\n")

def checkNeighbor(row, col, matrix):
    if matrix[row][col]["surrounding_clued_mines"] - matrix[row][col]["surrounding_mines"] == matrix[row][col]["surrounding_hidden_squares"]:
        #northwest
        if checkValidIndex(len(matrix), row-1, col-1):
            matrix[row-1][col-1]["safe"] = False
        #west
        if checkValidIndex(len(matrix), row, col-1):
            matrix[row][col-1]["safe"] = False
        #southwest
        if checkValidIndex(len(matrix), row+1, col-1):
            matrix[row+1][col-1]["safe"] = False
        #north
        if checkValidIndex(len(matrix), row-1, col):
            matrix[row-1][col]["safe"] = False
        #south
        if checkValidIndex(len(matrix), row+1, col):
            matrix[row+1][col]["safe"] = False
        #northesat
        if checkValidIndex(len(matrix), row-1, col+1):
            matrix[row-1][col+1]["safe"] = False
        #east
        if checkValidIndex(len(matrix), row, col+1):
            matrix[row][col+1]["safe"] = False
        #southeast
        if checkValidIndex(len(matrix), row+1, col+1) :
            matrix[row+1][col+1]["safe"] = False

    if (8 - matrix[row][col]["surrounding_clued_mines"]) - matrix[row][col]["surrounding_safe_squares"] == matrix[row][col]["surrounding_hidden_squares"]:
         #northwest
        if checkValidIndex(len(matrix), row-1, col-1):
            matrix[row-1][col-1]["safe"] = True
        #west
        if checkValidIndex(len(matrix), row, col-1):
            matrix[row][col-1]["safe"] = True
        #southwest
        if checkValidIndex(len(matrix), row+1, col-1):
            matrix[row+1][col-1]["safe"] = True
        #north
        if checkValidIndex(len(matrix), row-1, col):
            matrix[row-1][col]["safe"] = True
        #south
        if checkValidIndex(len(matrix), row+1, col):
            matrix[row+1][col]["safe"] = True
        #northesat
        if checkValidIndex(len(matrix), row-1, col+1):
            matrix[row-1][col+1]["safe"] = True
        #east
        if checkValidIndex(len(matrix), row, col+1):
            matrix[row][col+1]["safe"] = True
        #southeast
        if checkValidIndex(len(matrix), row+1, col+1):
            matrix[row+1][col+1]["safe"] = True
