import random
import pygame

#check if an index is within the matrix
def checkValidIndex(d, row, col):
    return (row >= 0 and row < d) and (col >= 0 and col < d)
    
#check if an index is a mine
def checkMine(d, row, col, matrix):
    return checkValidIndex(d, row, col) and matrix[row][col] == "mine"

def fillInNumbers(d, row, col, matrix):
    matrix = [][] * d
    for i in range(len(matrix)):
        for j in range(len(matrix):
            dic = {}
            dic["safe"] = (matrix[i][j] != "mine") #whether or not if the cell is a mine or a safe
            dic["num_Mines"] = 0 #number of mines determined by clues
            if matrix[i][j] != "mine" 
            dic["safe_Squares"] = 0
            if matrix[i][j] != "mine"
            dic["safe_Squares"] += 1
            dic["discovered_mines"] = 0
            dic["hidden_squares"] = 0
    
    return matrix

#generate a d x d environment with n mines in it
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
                if toReturn[i][j] != "mine" and random.randint(1, 100) <= 5:
                    #fill in mines by chance, update numbers of indices surrounding the mine
                    toReturn[i][j] = "mine"
                    #northwest
                    if checkValidIndex(d, i-1, j-1) and toReturn[i-1][j-1] != "mine":
                        toReturn[i-1][j-1]+=1
                    #west
                    if checkValidIndex(d, i, j-1) and toReturn[i][j-1] != "mine":
                        toReturn[i][j-1]+=1
                    #southwest
                    if checkValidIndex(d, i+1, j-1) and toReturn[i+1][j-1] != "mine":
                        toReturn[i+1][j-1]+=1
                    #north
                    if checkValidIndex(d, i-1, j) and toReturn[i-1][j] != "mine":
                        toReturn[i-1][j]+=1
                    #south
                    if checkValidIndex(d, i+1, j) and toReturn[i+1][j] != "mine":
                        toReturn[i+1][j]+=1
                    #northesat
                    if checkValidIndex(d, i-1, j+1) and toReturn[i-1][j+1] != "mine":
                        toReturn[i-1][j+1]+=1
                    #east
                    if checkValidIndex(d, i, j+1) and toReturn[i][j+1] != "mine":
                        toReturn[i][j+1]+=1
                    #southeast
                    if checkValidIndex(d, i+1, j+1) and toReturn[i+1][j+1] != "mine":
                        toReturn[i+1][j+1]+=1
                    minesRemaining -= 1
                    if minesRemaining == 0:
                        cease = True
                    if cease:
                        break

    return toReturn

#fill the matrix indices with how many mines are around that index, return a list of information for each index
def setMineNumbers(matrix):
    pass

def printMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print(str(matrix[i][j]) + " ", end='')
        print("\n")

printMatrix(generate(5, 5))
