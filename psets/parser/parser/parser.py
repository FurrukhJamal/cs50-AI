import nltk
import sys
# VP -> V | V NP | V NP PP | V NP PP Adj | V Adv Conj VP | V Adv PP Conj NP | V PP Conj NP | V Adv Conj NP
# We arrived the day before Thursday.
# N V Det N P N
# NP VP NP P NP 
# Holmes sat in the red armchair and he chuckled.
# N V P Det Adj N Conj N V
# N    V     P   Det Adj N     Conj N V
# NP    VP       NP           Conj NP VP  

# She never said  a   word until we     were at the door here.
#  N   Adv   V   Det   N    Conj  N     V   P   Det N   Adv
# NP     VP         NP            NP          VP  

# Holmes sat down  and  lit  his  pipe.
#  N      V   Adv  Conj  V   Det   N
# NP        VP     Conj  VP     NP 


# I had  a  country walk     on Thursday  and  came home  in   a  dreadful mess.
# N  V   Det  Adj     N       P    N       Conj  V    N   P      Det   Adj     N
# NP VP       NP                  NP             VP   NP              NP

# I had  a  little moist red paint in the  palm of  my  hand.
# N  V  Det  Adj    Adj  Adj  N    P   Det  N   P   Det  N

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S NP Conj S | VP NP | NP P NP | S P NP
NP -> N | Det N | Det AA N | Det N Adv
VP -> V | V NP | V NP P NP | V P NP | Adv V | V Adv 
AA -> Adj | Adj AA 


"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    result = []
    for word in nltk.word_tokenize(sentence):
        for char in word:
            if char.isalpha():
                result.append(word.lower())
                break
            
             
    # print(f"result : {result}")
    return result

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    data = []
    # for subtree in tree.subtrees(lambda t : t.label() == "NP"):
    #     # print(f"subtree : {subtree.label()}")
    #     subtree.pretty_print()
    #     print(subtree.flatten())
    #     data.extend(subtree)
    
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            # subtree.pretty_print()
            data.append(subtree)
    return data


if __name__ == "__main__":
    main()
