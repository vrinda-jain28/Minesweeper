import itertools
import random
import Clue
import Environment


class ImprovedAgent():
    """
    This improved agent uses inference based prediction approach to solving the board
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

        # Keep track of cells known to be safe or mines
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
        counter = 0
        self.mineSet.add(cell)
        for clue in self.knowledgeBase:
            counter = counter + clue.MarkMine(cell)
        return counter

    def MarkSafe(self, cell):
        """
        Add the cell to the set of board cells known to be safes.
        For each clue in the knowledge base, mark the cell as a safe as well.
        This updates the cell as a safe in the total knowledge base.
        """
        counter = 0
        self.safeSet.add(cell)
        for clue in self.knowledgeBase:
            counter = counter + clue.MarkSafe(cell)
        return counter

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

        # maintain a set of neighbors for a cell
        neighboringCells = set()

        i, j = cell

        # parse through neighbors/surrounding cells of a given cell
        for row in range(max(0, i - 1), min(i + 2, self.height)):
            for col in range(max(0, j - 1), min(j + 2, self.width)):
                # ignores the cell itself, and parses through neighboring cells and adds it to set of neighbors
                if (row, col) != (i, j):
                    neighboringCells.add((row, col)) # add cell to set of neighboring cells

        # add the clue to the knowledge base, each clue is represented by a set of cells as well as a count
        self.knowledgeBase.append(Clue.Clue(neighboringCells, count))

        # call the update knowledge base function, which marks additional cells as either safe cells or mine cells
        self.updateKnowledgeBase()

        inferences = self.newInferences()

        while inferences:
            for clue in inferences:
                self.knowledgeBase.append(clue)

            # call the update knowledge base function, which marks additional cells as either safe cells or mine cells
            self.updateKnowledgeBase()

            inferences = self.newInferences()
        print("\nMove: ", cell)

        while self.SimplifyKnowledgeBase() != self.knowledgeBase:
            pass

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

    def move_safely(self):
        """
        Picks a safe move from the set of safe moves (safeSet) available to make. If there is not a safe move to be made
        the function does not return anything
        """
        for move in self.safeSet:
            if move not in self.track_moves and move not in self.mineSet:
                self.print()
                return move
            else:
                print("No safe moves available :(")
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

    def print(self):
        print("\n\n\n")
        print("------------------------------------------------------------------")
        print("KnowledgeBase: ")
        for clue in self.knowledgeBase:
            print("\t", clue.cells, " = ", clue.count)
        print("\nConfirmed Safe:")
        print(self.safeSet)

        print("\nConfirmed Mines:")
        print(self.mineSet)
        print("------------------------------------------------------------------")

    def newInferences(self):
        """
        For each clue in the knowledge base: add it to the list of removed clues if it does not contain any cells
        Choose another clue from the knowledge base, check if it is empty (add to list of removed clues if it is)
        Make sure the two clues are different from one another and if the list of cells in the clues overlap(using
        subset). If it is a subset, then inferences can be drawn. Finally, remove any clues that are empty sets
        """

        inferences = []  # maintain a list of inferences
        removeClue = []  # maintain a list of clues to remove

        for clue1 in self.knowledgeBase:
            # mark for removal if it is empty
            if clue1.cells == set():
                removeClue.append(clue1)
                continue
            for clue2 in self.knowledgeBase:
                if clue2.cells == set():
                    removeClue.append(clue2)
                    continue
                if clue1 != clue2:  # make sure the clues are different from one another
                    if clue2.cells.issubset(clue1.cells):  # if s2 is a subset of s1
                        compareCells = clue1.cells.difference(clue2.cells)
                        compareCount = clue1.count - clue2.count
                        new_inference = Clue.Clue(compareCells, compareCount)
                        if new_inference not in self.knowledgeBase:
                            inferences.append(new_inference)

        # remove sentences without any cells
        self.knowledgeBase = [clues for clues in self.knowledgeBase if clues not in removeClue]
        return inferences

    def updateKnowledgeBase(self):
        """
        This function marks additional cells as mines or safes.
        """
        count = 1
        while count:
            count = 0
            # Iterate through all the clues within the knowledge base
            for clue in self.knowledgeBase:
                # Iterate through all the cells for the safes known within a clue
                for cell in clue.SafesKnown():  # calls the SafesKnown function from the Clue class
                    # Mark the cell as safe and update the count
                    self.MarkSafe(cell)
                    count += 1
                for cell in clue.MinesKnown():  # calls the MinesKnown function from the Clue class
                    # Mark the cell as a mine and update the count
                    self.MarkMine(cell)
                    count += 1
            # Iterate through all the cells from the set of safe cells
            for cell in self.safeSet:
                count += self.MarkSafe(cell)

            # Iterate through all the cells from the set of mine cells
            for cell in self.mineSet:
                count += self.MarkMine(cell)

    def FlagCells(self):
        """
        Return the set of all mines (mineSet) that have been identified up to current point
        """
        return self.mineSet
