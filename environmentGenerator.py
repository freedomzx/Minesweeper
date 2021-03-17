import random
import pygame

#check if an index is within the matrix
def checkValidIndex(d, row, col):
    return (row >= 0 and row < d) and (col >= 0 and col < d)
    
#check if an index is a mine
def checkMine(d, row, col, matrix):
    return checkValidIndex(d, row, col) and matrix[row][col] == "mine"

#make a matrix of information for each index
def fillInInfo(matrix, d):
    matrix = []
    for i in range(len(matrix)):
        toAdd = []
        for j in range(len(matrix)):
            dic = {}

            #keep track of whether or not the square has been directly searched yet
            dic["hidden"] = True

            #–whether or not it is a mine or safe (or currently covered)
            dic["safe"] = (matrix[i][j] != "mine") 

            #if safe, the number of mines surrounding it indicated by the clue
            dic["surrounding_clued_mines"] = ""
            if not dic["safe"]:
                dic["surrounding_clued_mines"] = "square_not_safe"
            else:
                dic["surrounding_clued_mines"] = 0
                #TODO find out what the clue means and increment this as appropriate

            #the number of safe squares identified around it, and number of mines around. also fill in hidden squares by counting valid squares around index
            dic["surrounding_safe_squares"] = 0
            dic["surrounding_mines"] = 0
            dic["surrounding_hidden_squares"] = 0

            #northwest
            if checkValidIndex(d, i-1, j-1):
                dic["surrounding_hidden_squares"]+=1
                if matrix[i-1][j-1] == "mine":
                    dic["surrounding_mines"]+=1
                else:
                    dic["surrounding_safe_squares"]+=1
            #west
            if checkValidIndex(d, i, j-1):
                dic["surrounding_hidden_squares"]+=1
                if matrix[i][j-1] == "mine":
                    dic["surrounding_mines"]+=1
                else:
                    dic["surrounding_safe_squares"]+=1
            #southwest
            if checkValidIndex(d, i+1, j-1):
                dic["surrounding_hidden_squares"]+=1
                if matrix[i+1][j-1] == "mine":
                    dic["surrounding_mines"]+=1
                else:
                    dic["surrounding_safe_squares"]+=1
            #north
            if checkValidIndex(d, i-1, j):
                dic["surrounding_hidden_squares"]+=1
                if matrix[i-1][j] == "mine":
                    dic["surrounding_mines"]+=1
                else:
                    dic["surrounding_safe_squares"]+=1
            #south
            if checkValidIndex(d, i+1, j):
                dic["surrounding_hidden_squares"]+=1
                if matrix[i+1][j] == "mine":
                    dic["surrounding_mines"]+=1
                else:
                    dic["surrounding_safe_squares"]+=1
            #northesat
            if checkValidIndex(d, i-1, j+1):
                dic["surrounding_hidden_squares"]+=1
                if matrix[i-1][j+1] == "mine":
                    dic["surrounding_mines"]+=1
                else:
                    dic["surrounding_safe_squares"]+=1
            #east
            if checkValidIndex(d, i, j+1):
                dic["surrounding_hidden_squares"]+=1
                if matrix[i][j+1] == "mine":
                    dic["surrounding_mines"]+=1
                else:
                    dic["surrounding_safe_squares"]+=1
            #southeast
            if checkValidIndex(d, i+1, j+1):
                dic["surrounding_hidden_squares"]+=1
                if matrix[i+1][j+1] == "mine":
                    dic["surrounding_mines"]+=1
                else:
                    dic["surrounding_safe_squares"]+=1

            toAdd.append(dic)
    
    return matrix

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

def checkNeighbor(row, col, matrix):
    if matrix[row][col]["surrounding_clued_mines"] - matrix[row][col]["square_not_safe"] == matrix[row][col]["surrounding_hidden_squares"]
        #northwest
        if checkValidIndex(matrix, row-1, col-1) and matrix[row-1][col-1]["hidden"] :
            matrix[row-1][col-1]["safe"] = False
        #west
        if checkValidIndex(matrix, row, col-1) and matrix[row][col-1]["hidden"] :
            matrix[row][col-1]["safe"] = False
        #southwest
        if checkValidIndex(matrix, row+1, col-1) and matrix[row+1][col-1]["hidden"] :
            matrix[row+1][col-1]["safe"] = False
        #north
        if checkValidIndex(matrix, row-1, col) and matrix[row-1][col]["hidden"] :
            matrix[row-1][col]["safe"] = False
        #south
        if checkValidIndex(matrix, row+1, col) and matrix[row+1][col]["hidden"] :
            matrix[row+1][col]["safe"] = False
        #northesat
        if checkValidIndex(matrix, row-1, col+1) and matrix[row-1][col+1]["hidden"] :
            matrix[row-1][col+1]["safe"] = False
        #east
        if checkValidIndex(matrix, row, col+1) and matrix[row][col+1]["hidden"] :
            matrix[row][col+1]["safe"] = False
        #southeast
        if checkValidIndex(matrix, row+1, col+1) and matrix[row+1][col+1]["hidden"] :
            matrix[row+1][col+1]["safe"] = False

    if matrix[row][col]["surrounding_safe_squares"] - matrix[row][col]["surrounding_safe_squares"] == matrix[row][col]["surrounding_hidden_squares"]
         #northwest
        if checkValidIndex(matrix, row-1, col-1) and matrix[row-1][col-1]["hidden"] :
            matrix[row-1][col-1]["safe"] = True
        #west
        if checkValidIndex(matrix, row, col-1) and matrix[row][col-1]["hidden"] :
            matrix[row][col-1]["safe"] = True
        #southwest
        if checkValidIndex(matrix, row+1, col-1) and matrix[row+1][col-1]["hidden"] :
            matrix[row+1][col-1]["safe"] = True
        #north
        if checkValidIndex(matrix, row-1, col) and matrix[row-1][col]["hidden"] :
            matrix[row-1][col]["safe"] = True
        #south
        if checkValidIndex(matrix, row+1, col) and matrix[row+1][col]["hidden"] :
            matrix[row+1][col]["safe"] = True
        #northesat
        if checkValidIndex(matrix, row-1, col+1) and matrix[row-1][col+1]["hidden"] :
            matrix[row-1][col+1]["safe"] = True
        #east
        if checkValidIndex(matrix, row, col+1) and matrix[row][col+1]["hidden"] :
            matrix[row][col+1]["safe"] = True
        #southeast
        if checkValidIndex(matrix, row+1, col+1) and matrix[row+1][col+1]["hidden"] :
            matrix[row+1][col+1]["safe"] = True

printMatrix(generate(5, 5))
