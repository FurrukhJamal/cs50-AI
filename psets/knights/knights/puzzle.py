from logic import *
# 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   github token
# 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

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And( 
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnave, CKnight),
    
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight)),

    Biconditional(AKnave, Not(And(AKnave, AKnight)))
    
    


    # TODO
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnave, CKnight),
    
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight)),

    Biconditional(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnave, CKnight),
    
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight)),

    Biconditional(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    # Or(Biconditional(BKnight, (And(AKnave, BKnight))), Biconditional(BKnave, And(AKnave, BKnave)))
    Biconditional(BKnight, And(AKnave, BKnight)) 
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnave, CKnight),
    
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight)),

    
    # Or(Implication(AKnight, BKnave) , Implication(AKnave , Not(BKnave))),
    # Or(Implication(BKnight, CKnave) , Implication(BKnave , Not(CKnave))),
    # Or(Implication(CKnight, AKnight) , Implication(CKnave , Not(AKnight))),

    # Or(And(AKnight, BKnave), And(AKnave, Not(BKnave))),
    # Or(Implication(AKnight, BKnave), Implication(AKnave, Not(BKnave))),
    # Or(And(BKnave, Not(CKnave), And(BKnight, CKnave))),
    # Implication(CKnight, AKnight)
    
    Biconditional(AKnight, Biconditional(AKnight, Not(AKnave))),
    Biconditional(BKnight, And(Biconditional(AKnight, BKnave), CKnave)),
    Biconditional(CKnight, AKnight)

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
