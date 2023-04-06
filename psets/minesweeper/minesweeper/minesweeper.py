import itertools
import random
from copy import *



class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

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

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

        self.mines = set()
        self.safes = set()

    def getCells(self):
        return self.cells

    def getCount(self):
        return self.count
    
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def __sub__ (self, other):
        return Sentence(self.getCells() - other.getCells(), self.getCount() - other.getCount())

    # Test
    def __hash__(self):
        return hash(tuple(self.cells)) + hash(self.count)

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else : 
            return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.mines.add(cell)
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.safes.add(cell)
            self.cells.remove(cell)
    
    def markAllMines(self):
        for cell in deepcopy(self.cells):
            self.mark_mine(cell)

    def markAllSafe(self):
        for cell in deepcopy(self.cells):
            self.mark_safe(cell)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        #test
        self.unknownCells = set()

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        
        # calculate the neighbors of the cell
        neighbors = set()
        for col in range(cell[1] - 1 , cell[1] + 2):    
            for row in range(cell[0] - 1 , cell[0] + 2):
                if (row, col) not in self.moves_made and col >= 0 and row >= 0 and col < self.width and row < self.height and (row, col) != cell:
                    neighbors.add((row, col))

        # print(f"CELL : {cell}")
        # print(f"neighors : {neighbors}")

        self.knowledge.append(Sentence(neighbors, count))
        totalInferences = 0
        inferenceCounter = 0
        atStart = 0
        while True:
            atStart = totalInferences
            for i in range(len(self.knowledge)):
                sentence = self.knowledge[i]
                for j in range(len(self.knowledge)):
                    nextSentence = self.knowledge[j]

                    if sentence.getCells() and sentence.getCells().issubset(nextSentence.getCells()):
                        newCells = nextSentence.getCells() - sentence.getCells()
                        newCount = nextSentence.getCount() - sentence.getCount()
                        s= Sentence(newCells , newCount)
                        if s not in self.knowledge:
                            self.knowledge.append(s)
                            inferenceCounter += 1

            #check
            for sentence in deepcopy(self.knowledge):
                if sentence.getCells() and len(sentence.getCells()) == sentence.getCount():
                    # print("Case all Mines")
                    inferenceCounter += 1
                    for Cell in deepcopy(sentence.getCells()):
                        self.mark_mine(Cell)
                elif sentence.getCells() and sentence.getCount() == 0:
                    # print("Case all safes")
                    inferenceCounter += 1
                    for Cell in deepcopy(sentence.getCells()):
                        self.mark_safe(Cell)
            
            totalInferences = inferenceCounter
            if atStart == totalInferences:
                break                 
                 

        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        mines = deepcopy(self.mines)
        safes = deepcopy(self.safes)
        
        while True:
            try:
                move = safes.pop()
                if move not in self.moves_made:
                    return move        
            except KeyError:
                return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # for row in range(self.height):
        #     for col in range(self.width):
        #         if (row, col) not in self.moves_made and (row, col) not in self.mines:
        #             return (row, col)

        count = 0
        while True:
            move = (random.randrange(self.height), random.randrange(self.width))
            if move not in self.moves_made and move not in self.mines:
                return move
            count += 1
            if count >= self.height * self.width:
                break
        return None   

# def main():
#     # ai = MinesweeperAI()
#     # print(ai.add_knowledge((7, 7), 2))
#     s1 = Sentence(set(((0,0) , (0, 1), (0,2))), 2 )
#     cell = set()
#     s2 = Sentence(set([(0,2)]), 0 )
#     print(f"s2.getCells(): {s2.getCells()}")
#     print(s1.getCells().issubset(s2.getCells()))
#     s3 = s1.getCells() - s2.getCells()
#     print(f"s3 : {s3}")

#     print(f"s1 cells: {s1.getCells()}")

#     s4 = s1 - Sentence(set(((0, 0 ), (0,2))), 1)
#     print(f"Subtracted sentence is {s4}")

#     s5 = Sentence(set(((0, 0 ), (0,2))), 1) - s1

#     print(f"reversed subtracted sentence : {s5}") 

#     print(f"union of s1 and s2 {s2.getCells().intersection(s1.getCells())}")

#     tuplesSet = set()
#     tuplesSet.add((s1, s2))
#     print(f"is (s1, s2) in set : {(s1, s2) in tuplesSet}")
#     print(f"is (s2, s1) in set : {(s2, s1) in tuplesSet}")

#     print(f"Test empty cell sentence")

#     emptySentence = Sentence(set() , 1)
#     print(f"{emptySentence}")
#     print(f"if sentence.getcells():")
#     if emptySentence.getCells():
#         print("True")
#     else:
#         print("False")


# if __name__ == "__main__":
#     main()         
