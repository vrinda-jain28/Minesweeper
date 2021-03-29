import numpy as np
import random


class Environment():
    """
    Minesweeper game representation
    """

    def __init__(self, height=50, width=50, mines=100):
        """"
        Take in desired dimensions and a given number of mines to generate a board with randomly placed mines
        """
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly to the board
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # Maintain a set of mines that is found by the player
        self.mines_found = set()  # initially this set is empty

    def is_mine(self, cell):
        i, j = cell # a board cell contains a row and column, where i is row and j is column
        return self.board[i][j]

    def mineNeighbor(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        counter = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        counter += 1

        return counter

    def mineList(self):
        return self.mines
