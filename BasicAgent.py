import Environment
import numpy as np
import random
import Clue


# newEnvironment = minesweeperVScode.Environment # Load original environment -> used to compare with moves and update


class BasicAgent():
    """
    Represents Basic Agent
    Tasks: For each cell, keep track of:
            – if safe, the number of mines surrounding it indicated by the clue
            – the number of safe squares identified around it
            – the number of mines identified around it.
            – the number of hidden squares around it.

    2)  • If, for a given cell, the total number of mines (the clue) minus the number of revealed mines is the number of
            hidden neighbors, every hidden neighbor is a mine.

    3)  • If, for a given cell, the total number of safe neighbors (8 - clue) minus the number of revealed safe neighbors is
            the number of hidden neighbors, every hidden neighbor is safe.

    4)  • If a cell is identified as safe, reveal it and update your information.

    5)  • If a cell is identified as a mine, mark it and update your information.

    6)  • The above steps can be repeated until no more hidden cells can be conclusively identified.

    7)  • If no hidden cell can be conclusively identified as a mine or safe, pick a cell to reveal uniformly at random from
            the remaining cells.
    """

    def __init__(self, height=50, width=50):

        # Initialize the dimensions of the board,set the height and width
        self.height = height
        self.width = width

        self.track_moves = set()  # Keep a track of the moves which have been made
        self.total_cells = set()  # as well as a set of all board cells -> total cells

        for x in range(height):
            for y in range(width):
                self.total_cells.add((x, y))  # adds all locations (x,y) into all cells

        self.mineSet = set()  # keep a track of the board cells known to be mines
        self.safeSet = set()  # keep a track of the board cells known to be safes

        # List of clues (set of cells and count of how many are mines)
        self.knowledgeBase = []
        # Example knowledge base: [((set of cells) = count), ((set2 of cells) = count), ((set3 of cells) = count)]

    def MarkMine(self, cell):
        """
        Add the cell to the set of board cells known to be mines.
        For each clue in the knowledge base, mark the cell as a mine as well.
        This updates the cell as a mine in the total knowledge base.
        """
        self.mineSet.add(cell)
        for clue in self.knowledgeBase:
            clue.MarkMine(cell)

    def MarkSafe(self, cell):
        """
        Add the cell to the set of board cells known to be safes.
        For each clue in the knowledge base, mark the cell as a safe as well.
        This updates the cell as a safe in the total knowledge base.
        """
        for clue in self.knowledgeBase:
            clue.MarkSafe(cell)

    def add_knowledge(self, cell, count):
        """
        The knowledge base is updated based on how many mines surround a safe cell (the clue)
        This function adds a cell to the set of moves that have been made, mark the current cell as safe,
        adds a new clue to the knowledge base using the cell and count given within function parameters,
        mark any other cell as safe or mine that can be inferred using basic inference techniques, and finally update
        the knowledge base with any new clues that can be inferred.
        """

        # add cell to list of moves that have been made
        self.track_moves.add(cell)

        # add cell to list of safe cells
        self.MarkSafe(cell)

        updatedKnowledgeBase = []
        # parse through the neighbors/surrounding cells of the current cell
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # If the cell is within board dimensions, and is identified to be a mine, add it as a new knowledge
                if 0 <= i < self.height and 0 <= j < self.width:  # in bounds
                    if (i, j) not in self.track_moves and (i, j) not in self.safeSet:
                        updatedKnowledgeBase.append((i, j))
                        # for a given move, check if cell location is in set of moves_made or in set of safes

        # add the new Knowledge to the knowledge base, calling the Clue class
        if len(updatedKnowledgeBase) != 0:
            self.knowledgeBase.append(Clue.Clue(updatedKnowledgeBase, count))

        while self.SimplifyKnowledgeBase() != self.knowledgeBase:
            pass

        """
        Print a text based representation of the sets for easy user viewing within the terminal
        USE FOR TESTING OUTPUTS!!
        """
        print("\n\n\n\n")
        print("------------------------------------------------------------------")
        print("\nCurrent move made: ", cell)
        print("Current Knowledge Base: ")
        for clue in self.knowledgeBase:
            print(clue)
        print("\nConfirmed Safe Cells: ")
        print(self.safeSet)

        print("\nConfirmed Mine Cells: ")
        print(self.mineSet)
        print("------------------------------------------------------------------")

    def move_safely(self):
        """
        Picks a safe move from the set of safe moves (safeSet) available to make. If there is not a safe move to be made
        the function does not return anything
        """
        if len(self.safeSet) > 0:
            return self.safeSet.pop()
        else:
            print("No safe moves to be made :(")
            return None

    def move_randomly(self):
        """
        Picks a random move from the set of moves that are available to make (total board cells - moves that have
        already been made - moves that have been identified as mines). If there is not a random move, available moves ≤ 0
        to be made the function does not return anything
        """
        availableMoves = self.total_cells - self.track_moves - self.mineSet  # makes a move that has not already been made and is known to not be a mine
        if len(availableMoves) > 0:
            return random.choice(tuple(availableMoves))
        else:
            return None

    def SimplifyKnowledgeBase(self):
        """
        Make a copy of the current knowledge base and iterate through each clue. For each clue, retrieve the known safes
        & known mines. Iterate through each set, and update it with the union of both and remove it from the knowledge
        base.
        """

        # make a copy of the current knowledge base
        GoThroughClues = self.knowledgeBase.copy()

        for clue in GoThroughClues:  # Queries all the clues in the knowledge base
            # call known_safes function from the Clue class, returns set of safe cells and stores in known_safes
            SafesQueried = clue.SafesKnown()
            # call known_mines function from the Clue class, returns set of mine cells and stores in known_mines
            MinesQueried = clue.MinesKnown()

            if SafesQueried:
                self.safeSet.update(SafesQueried)  # Add to safeSet
                self.knowledgeBase.remove(clue)  # remove clue from the knowledge base

            if MinesQueried:
                self.knowledgeBase.remove(clue)  # remove clue from knowledge base
                for mine in MinesQueried.union(self.mineSet):
                    # if there is an overlap between known_mines and self.mines, mark the mine
                    self.MarkMine(mine)

        return self.knowledgeBase

    def FlagCells(self):
        """
        Return the set of all mines (mineSet) that have been identified up to current point
        """
        return self.mineSet
