class Maze:
    def __init__(dimension):
        self.size = dimension
        self.grid = []
        for i in range(dimension):
            self.grid.append[[Cell([]) * dimension]]
    def generate(seed):
        startCellIndex = seed % self.size

    def generateDFS()


class Cell:
    def __init__(connections):
        self.connections = connections
