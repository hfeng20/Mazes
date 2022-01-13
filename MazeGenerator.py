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
            start = random.randint(0,self.size * 4 - 1)
            end = random.randint(0,self.size * 4 - 1)
            while(start == end):
                end = random.randint(0,self.size * 4 - 1)

        startCellIndex = seed % self.size
        self.generateDFS(self.grid, self.grid[0][startCellIndex])
        lines = []

        for i in range(0, len(self.grid)):

            for t in range(0, len(self.grid)):

                cell = self.grid[i][t]

                if cell.col + 1 == self.size:
                    if not cell.row + 1 == self.size:
                        lines.append([cell.topRight, cell.bottomRight])

                elif not self.grid[cell.row][cell.col + 1] in cell.connections:
                    coords = [cell.topRight, cell.bottomRight]
                    lines.append(coords)

                if cell.col == 0:
                    lines.append([cell.topLeft, cell.bottomLeft])

                elif not self.grid[cell.row][cell.col - 1] in cell.connections:
                    coords = [cell.topLeft, cell.bottomLeft]
                    lines.append(coords)

                if cell.row + 1 == self.size:
                    lines.append([cell.bottomLeft, cell.bottomRight])

                elif not self.grid[cell.row + 1][cell.col] in cell.connections:
                    coords = [cell.bottomLeft, cell.bottomRight]
                    lines.append(coords)

                if cell.row == 0:
                    if not cell.col == 0:
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

maze = Maze(40)
maze.generate(3, True)