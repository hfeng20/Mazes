import random
import matplotlib.pyplot as plt
import math


class Maze:
    def __init__(self,dimension):
        self.size = dimension
        self.grid = []
        for i in range(dimension):
            temp = []
            for t in range(dimension):
                cell = Cell(i, t, self.size)
                temp.append(cell)
            self.grid.append(temp)

    def generate(self,seed,randomizeEndPoints):

        if(randomizeEndPoints):
            start = random.randint(0,self.size - 1)
            end = random.randint(0,self.size - 1)
            if(random.randint(0,1) == 0):
                startCol = 0
                startRow = start
                endCol = self.size - 1
                endRow = end
            else:
                startCol = start
                startRow = 0
                endCol = end
                endRow = self.size - 1
            startCell = self.grid[startRow][startCol]
            endCell = self.grid[endRow][endCol]
        else:
            startCell = self.grid[0][0]
            endCell = self.grid[self.size - 1][self.size - 1]

            

        startCellIndex = seed % self.size
        self.generateDFS(self.grid, self.grid[0][startCellIndex])
        lines = []
        print("start: " + (str)(startCell.row) + " " + (str)(startCell.col))
        print("end: " + (str)(endCell.row) + " " + (str)(endCell.col))
        for i in range(0, len(self.grid)):

            for t in range(0, len(self.grid)):
                startTop = False
                startLeft = False
                endBottom = False
                endRight = False
                cell = self.grid[i][t]
                if cell == startCell:
                    if cell.row == 0:
                        startTop = True
                    else:
                        startLeft = True
                elif cell == endCell:
                    if cell.row == self.size - 1:
                        endBottom = True
                    else:
                        endRight = True


                if cell.col + 1 == self.size:
                    if not endRight:
                        lines.append([cell.topRight, cell.bottomRight])
                    else:
                        coords = [cell.topRight[0] + 10, (cell.topRight[1] + cell.bottomRight[1])/2]
                        plt.plot(plt.Circle((cell.topRight[0] + 10, (cell.topRight[1] + cell.bottomRight[1])/2)))

                elif not self.grid[cell.row][cell.col + 1] in cell.connections:
                    coords = [cell.topRight, cell.bottomRight]
                    lines.append(coords)

                if cell.col == 0:
                    if not startLeft:
                        lines.append([cell.topLeft, cell.bottomLeft])

                elif not self.grid[cell.row][cell.col - 1] in cell.connections:
                    coords = [cell.topLeft, cell.bottomLeft]
                    lines.append(coords)

                if cell.row + 1 == self.size:
                    if not endBottom:
                        lines.append([cell.bottomLeft, cell.bottomRight])

                elif not self.grid[cell.row + 1][cell.col] in cell.connections:
                    coords = [cell.bottomLeft, cell.bottomRight]
                    lines.append(coords)

                if cell.row == 0:
                    if not startTop:
                        lines.append([cell.topRight, cell.topLeft])

                elif not self.grid[cell.row - 1][cell.col] in cell.connections:
                    coords = [cell.topRight, cell.topLeft]
                    lines.append(coords)
        
        for line in lines:
            xs,ys = zip(*line)
            plt.plot(xs,ys)
        plt.axis("scaled")
        plt.show()

    def generateDFS(self,grid, startCell):
        startCell.visited = True
        nextCell = self.randomUnvisitedNeighbor(startCell)
        while nextCell:
            self.connectCells(startCell, nextCell)
            self.generateDFS(grid,nextCell)
            nextCell = self.randomUnvisitedNeighbor(startCell)

    def connectCells(self, cell1, cell2):
        cell1.connections.append(cell2)
        cell2.connections.append(cell1)

    def randomUnvisitedNeighbor(self, cell):
        row = cell.row
        col = cell.col
        possibleNeighbors = []
        if row - 1 >= 0 and not self.grid[row - 1][col].visited:
            possibleNeighbors.append(self.grid[row - 1][col])
        if col - 1 >= 0 and not self.grid[row][col - 1].visited:
            possibleNeighbors.append(self.grid[row][col - 1])
        if col + 1 < self.size and not self.grid[row][col + 1].visited:
            possibleNeighbors.append(self.grid[row][col + 1])
        if row + 1 < self.size and not self.grid[row + 1][col].visited:
            possibleNeighbors.append(self.grid[row + 1][col])
        if len(possibleNeighbors) == 0:
            return None
        return possibleNeighbors[random.randint(0, len(possibleNeighbors) - 1)]        




class Cell:
    #left, down, right, up
    def __init__(self, row, col, gridSize):
        self.row = row
        self.col = col
        self.visited = False
        self.connections = []
        self.topLeft = [col * 10, (gridSize - row) * 10]
        self.topRight = [(col + 1) * 10, (gridSize - row) * 10]
        self.bottomLeft = [col * 10, (gridSize - row - 1) * 10]
        self.bottomRight = [(col + 1) * 10, (gridSize - row - 1) * 10]



print("Input \"generate\" to generate a new maze. Input \"solution\" to see the solution path. Input nothing to exit.")
action = input("-")
curMaze = None
while action != "":
    if action == "generate":
        curMaze = Maze((int)(input("Difficulty (1-40): ")))
        randomize = input("Randomize end points? If n, start will be top left and end will be bottom right. (y or n): ")
        if randomize == "y":
            randomize = True
        else:
            randomize = False
        curMaze.generate(100, randomize)
    if action == "solution":
        break
    if action == "":
        break
    action = input("-")