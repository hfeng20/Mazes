import random
import matplotlib.pyplot as plt
import math


class Maze:
    def __init__(self,dimension):
        self.lines = None
        self.startCell = None
        self.endCell = None
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
            start = random.randint(1,self.size - 2)
            end = random.randint(1,self.size - 2)
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
        self.startCell = startCell
        self.endCell = endCell
            

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
        self.lines = lines


    def showMapWithSolution(self, solutionPath):
        plt.figure()

        for line in self.lines:
            xs,ys = zip(*line)
            plt.plot(xs,ys, color = "green")
        for line in solutionPath:
            xs,ys = zip(*line)
            plt.plot(xs,ys, color = "red")

        if self.startCell.row == 0:
            coords = [self.startCell.topLeft[0] + 3, self.startCell.topRight[1] + 10]
            plt.text(coords[0], coords[1], "↓", fontsize=12)
        elif self.startCell.col == 0:
            coords = [self.startCell.bottomLeft[0] - 10, self.startCell.bottomRight[1] + 3]
            plt.text(coords[0], coords[1], "→", fontsize=12)
        if self.endCell.row == self.size - 1:
            coords = [self.endCell.bottomLeft[0] + 3, self.endCell.bottomRight[1] - 10]
            plt.text(coords[0], coords[1], "↓", fontsize=12)
        elif self.endCell.col == self.size - 1:
            coords = [self.endCell.topRight[0], self.endCell.bottomRight[1]]
            plt.text(coords[0], coords[1], "→", fontsize=12)


        plt.axis("scaled")
        plt.axis("off")
        plt.ion()
        plt.show()
        plt.pause(0.01)

    def showMap(self):
        plt.figure()

        for line in self.lines:
            xs,ys = zip(*line)
            plt.plot(xs,ys, color = "green")

        if self.startCell.row == 0:
            coords = [self.startCell.topLeft[0] + 3, self.startCell.topRight[1] + 10]
            plt.text(coords[0], coords[1], "↓", fontsize=12)
        elif self.startCell.col == 0:
            coords = [self.startCell.bottomLeft[0] - 10, self.startCell.bottomRight[1] + 3]
            plt.text(coords[0], coords[1], "→", fontsize=12)
        if self.endCell.row == self.size - 1:
            coords = [self.endCell.bottomLeft[0] + 3, self.endCell.bottomRight[1] - 10]
            plt.text(coords[0], coords[1], "↓", fontsize=12)
        elif self.endCell.col == self.size - 1:
            coords = [self.endCell.topRight[0], self.endCell.bottomRight[1]]
            plt.text(coords[0], coords[1], "→", fontsize=12)


        plt.axis("scaled")
        plt.axis("off")
        plt.ion()
        plt.show()
        plt.pause(0.01)
    
    def showSolution(self):
        for row in self.grid:
            for cell in row:
                cell.visited = False

        start = self.startCell
        end = self.endCell
        path = self.solutionHelper([],start, end)

        solutionLines = []
        for index in range(len(path) - 1):
            cell = path[index]
            nextCell = path[index + 1]
            curCellCenterCoords = [cell.bottomLeft[0] + 5, cell.bottomLeft[1] + 5]
            nextCellCenterCoords = [nextCell.bottomLeft[0] + 5, nextCell.bottomLeft[1] + 5]
            solutionLines.append([curCellCenterCoords, nextCellCenterCoords])
        self.showMapWithSolution(solutionLines)

        

    def solutionHelper(self,path,start,end):
        start.visited = True
        #print((str)(start.row) + " " + (str)(start.col))
        neighbors = self.getConnectedNeighbors(start)

        if start == end or len(path) > 0:
            path.append(start)
            return path
        if len(neighbors) == 0:
            return None
        possiblePath = None
        for neighbor in neighbors:
            temp = self.solutionHelper(path, neighbor, end)
            if temp:
                temp.append(start)
                return temp

    def getConnectedNeighbors(self, cell):
        row = cell.row
        col = cell.col
        possibleNeighbors = []
        if row - 1 >= 0 and not self.grid[row - 1][col].visited and self.grid[row - 1][col] in cell.connections:
            possibleNeighbors.append(self.grid[row - 1][col])
        if col - 1 >= 0 and not self.grid[row][col - 1].visited and self.grid[row][col - 1] in cell.connections:
            possibleNeighbors.append(self.grid[row][col - 1])
        if col + 1 < self.size and not self.grid[row][col + 1].visited and self.grid[row][col + 1] in cell.connections:
            possibleNeighbors.append(self.grid[row][col + 1])
        if row + 1 < self.size and not self.grid[row + 1][col].visited and self.grid[row + 1][col] in cell.connections:
            possibleNeighbors.append(self.grid[row + 1][col])
        return possibleNeighbors

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

print("Input \"generate\" or \"g\" to generate a new maze. Input \"solution\" or \"s\"to see the solution path. Input nothing to exit.")
action = input(">")
curMaze = None
while action != "":
    if action == "generate" or action == "g":
        size = (input("Difficulty (1-40): "))
        while not size.isnumeric() or (int)(size) > 40:
            size = input("Invalid! (1-40): ")
        curMaze = Maze((int)(size))
        randomize = input("Randomize end points? If n, start will be top left and end will be bottom right. (y or n): ")
        while True:
            if randomize == "y" or randomize == "n":
                break
            randomize = input("Invalid! (y or n): ")
        if randomize == "y":
            randomize = True
        else:
            randomize = False
        curMaze.generate(100, randomize)
        curMaze.showMap()
    if action == "solution" or action == "s":
        if not curMaze:
            print("No maze generated!")
        else:
            curMaze.showSolution()
    if action == "":
        break
    action = input(">")