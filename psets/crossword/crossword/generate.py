import sys


from crossword import *
from copy import *
from collections import deque 
from math import *

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        # print(f"number of variables: {len(self.crossword.variables)}")
        # print(f"Overlaps : {self.crossword.overlaps}")
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # print(f"self.domains : {self.domains}")
        for variable in self.domains:
            for word in deepcopy(self.domains[variable]):
                if len(word) != variable.length:
                    self.domains[variable].remove(word)
        # print(f"updated self-domains: {self.domains}")

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        (overlappingIndexX, overlappingIndexY) = self.crossword.overlaps[x, y]
        # print(f"Variables are : {x} and {y}")
        # print(f"word in x domains : {self.domains[x]}")
        # print(f"word in y's domain : {self.domains[y]}")
        flagForRivision = False
        for word in deepcopy(self.domains[x]):
            counter = 0
            for wordY in self.domains[y]:
                
                if word[overlappingIndexX] != wordY[overlappingIndexY]:
                    counter += 1
                    # print(f"counter : {counter}")
            if counter == len(self.domains[y]):
                self.domains[x].remove(word)
                flagForRivision = True

        # print(f"domain of x after updating: {self.domains[x]}")
        if flagForRivision:
            return True
        return False            
                     
        # if flagForRivision : 
        #     return True
                
        


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # print(f"arc at start : {arcs}")
        if arcs == None:
            arcs = deepcopy(self.crossword.overlaps)
        
        q = deque()
        for arc in arcs:
            if arcs[arc] != None:
                # print(f"type: {type(arc)}")
                q.append(arc)
                # print(f"arc[0] : {arc[0]} arc[1] : {arc[1]}")
                # print(type(arc))
        # print(f"QUEUE: {q}")
        
        while q:
            if isinstance(q[-1], tuple) and len(q[-1]) == 2:
                x , y = q.pop()
            # print(f"x in ac3 loop : {x}")
            # print(f"y in ac3 loop: {y}")
            # print(f"self.revise(x, y) : {self.revise(x, y)}")

            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False 
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        q.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        counter = 0
        for variable in assignment:
            if type(assignment[variable]) == "str":
                counter += 1
        if counter == len(assignment):
            return True
        return False 

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # print(f"assignment in consistent function: {assignment}")
        if len(assignment) == 1:
            return True 
        
        for variable in assignment:
            for nextVariable in assignment:
                if variable == nextVariable:
                    continue
                elif assignment[variable] == assignment[nextVariable]:
                    return False  

            if len(assignment[variable]) != variable.length:
                return False
            for neighbor in self.crossword.neighbors(variable):
                # print(f"neighbors for selected variable: {variable} in consisten function : {self.crossword.neighbors(variable)}")
                # print(f"neighbor is : {neighbor}")
                (indexVariable, indexNeighbor) = self.crossword.overlaps[variable, neighbor]
                # print(f"overlapping index : ({indexVariable}, {indexNeighbor})")
                if neighbor in assignment and variable in assignment:
                    # print(f"assignment[variable][indexVariable] : {assignment[variable][indexVariable]} assignment[neighbor][indexNeighbor] : {assignment[neighbor][indexNeighbor]}")
                    if assignment[variable][indexVariable] != assignment[neighbor][indexNeighbor]:
                        return False

        return True 

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # print(f"assigmnet in order_domain_values : {assignment}")
        for neighbor in self.crossword.neighbors(var):
            
            data = {}
            for word in self.domains[var]:
                counter = 0
                for neighborsWord in self.domains[neighbor]:
                    if word == neighborsWord:
                        counter += 1
                    indexVar, indexNeighbor = self.crossword.overlaps[var, neighbor]
                    if word[indexVar] != neighborsWord[indexNeighbor]:
                        counter +=1
                data[word] = counter
        words = sorted(data.items(), key = lambda item : item[1])
        # print(f"The list of words are : {words}")
        wordsWithoutCount = []
        for tup in words:
            wordsWithoutCount.append(tup[0]) 
        # print(f"The same list without the counter : {wordsWithoutCount}")
        return wordsWithoutCount

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # print("Hitting select_unassigned_variable")
        # for variable in self.crossword.variables:
        #     if variable not in assignment:
        #         # print(f"Selected Variable: {variable}")
        #         return variable
        minNumberDomains = inf
        result = []
        for variable in self.crossword.variables:
            if variable not in assignment:
                if len(self.domains[variable]) < minNumberDomains:
                    minNumberDomains = len(self.domains[variable])

        for variable in self.crossword.variables:
            # print(f"variable in loop: {variable}")
            # print(f"len(self.domains[variable]) : {len(self.domains[variable])}")
            if variable not in assignment:
                if len(self.domains[variable]) == minNumberDomains:
                    result.append(variable)   
        # print(f"result : {result}")
        # return result[0]
        

        # if there was one variable and not a tie 
        if len(result) == 1:
            # print(f"i should not see this shit")
            return result[0]
        else:
            # decide on number of degrees 
            # print(f"selected with max degree")
            data = {}
            # for variable in result:
            #     counter = 0
            #     for tup in self.crossword.overlaps.keys():
            #         if variable in tup:
            #             counter += 1
                
            #     data[variable] = counter
            for variable in result:
                data[variable] = len(self.crossword.neighbors(variable))
            # print(f"data : {data}")
            # sorting the variables based on the highest degree 
            variableDegrees = sorted(data.items() , key = lambda item : item[1] , reverse = True)
            result = []
            for val in variableDegrees:
                result.append(val[0])
            return result[0] 

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # print(f"assigment : {assignment}")
        if len(assignment) == len(self.crossword.variables):
            return assignment
        
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            # print(f"value : {value}")
            newAssignment = deepcopy(assignment)
            newAssignment[var] = value
            if self.consistent(newAssignment):
                result = self.backtrack(newAssignment)
                # print(f"result from recursive call : {result} \n\n")
                if result is not None:
                    return result
            # print(f"REMOVING TRIED VALUE")
            # print(f"assigment before removing : {assignment}")
            del newAssignment[var]
            # print(f"assigment after removing : {assignment}")
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


def test():
    x = Variable(2, 4 , Variable.DOWN, 4)
    print(f"{x}")
    y = Variable(4, 4 , Variable.ACROSS, 4)





if __name__ == "__main__":
    main()
    # test()
