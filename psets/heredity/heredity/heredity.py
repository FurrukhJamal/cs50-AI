import csv
import itertools
import sys
from copy import *

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    # print(f"prob : {probabilities}")
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # jointProb = []
    # probablity = 0
    # for person in people:
    #     # print(f"person : {person}")
    #     if person not in one_gene and person not in two_genes:
    #         # print(f"{person} have no gene")
    #         if person in have_trait : 
    #             probablity = PROBS["gene"][0] * PROBS["trait"][0][True]
    #         if person not in have_trait:
    #             probablity = PROBS["gene"][0] * PROBS["trait"][0][False]
    #         # print(f"probability for {person} in no gene condition : {probablity}")
    #     elif person in two_genes:
    #         # print(f"{person} have two gene")
    #         PR2Gene = 0
    #         # case person has no mother and father
    #         if people[person]["mother"] == None and people[person]["father"] == None:
    #             PR2Gene = PROBS["gene"][2]

    #         # case mother yes father None
    #         elif people[person]["mother"] != None and people[person]["father"] == None:
    #             PRmother = 0.99 * PROBS["gene"][1]
    #             PR2Gene = PRmother

    #         # mother None father present
    #         elif people[person]["mother"] == None and people[person]["father"] != None:
    #             PRfather = 0.99 * PROBS["gene"][1]
    #             PR2Gene = PRfather

    #         # case both father and mother there
    #         elif people[person]["mother"] !=None and people[person]["mother"] != None:
    #             prMotherFather = 0
    #             prMotherNotFather = 0
    #             prFatherNotMother = 0
    #             prNotMotherNotFather = 0
    #             if (people[person]["mother"] in one_gene or people[person]["mother"] in two_genes) and (people[person]["father"] in one_gene or people[person]["father"] in two_genes):
    #                 prMotherFather = 0.99 * 0.99
    #             if (people[person]["mother"] in one_gene or people[person]["mother"] in two_genes) and (people[person]["father"] not in one_gene and people[person]["father"] not in two_genes):
    #                 # case mother has a gene father doesnt
    #                 prMotherNotFather = 0.99 * 0.01
                    
    #             if (people[person]["father"] in one_gene or people[person]["father"] in two_genes) and people[person]["mother"] not in one_gene and people[person]["mother"] not in two_genes:
    #                 prFatherNotMother = 0.99 * 0.01
                    
    #             if people[person]["mother"] not in one_gene and people[person]["mother"] not in two_genes and people[person]["father"] not in one_gene and people[person]["father"] not in two_genes:
    #                 prNotMotherNotFather = 0.01 * 0.01
    #         # print(f"probability for {person} in two gene condition : {probablity}")
    #             PR2Gene = prMotherFather + prMotherNotFather + prFatherNotMother + prNotMotherNotFather

    #             if person in have_trait:
    #                 probablity = PR2Gene * PROBS["trait"][2][True]
                
    #             if person not in have_trait:
    #                 probablity = PR2Gene * PROBS["trait"][2][False]
    #     elif person in one_gene:
    #         # print(f"{person} have one gene")
    #         PR1Gene = 0
    #         # if both mother father have atleast one gene
    #         if (people[person]["mother"] in one_gene or people[person]["mother"] in two_genes) and (people[person]["father"] in one_gene or people[person]["father"] in two_genes):
    #             # case gets gene from mother
    #             PRMother = 0.99 * 0.01
    #             # case gets gene from father
    #             PRFather = 0.99 * 0.01
    #             PR1Gene = PRMother + PRFather
    #         # case mother have the gene only
    #         elif (people[person]["mother"] in one_gene or people[person]["mother"] in two_genes) and (people[person]["father"] not in one_gene or people[person]["father"] not in two_genes):
    #             PRMother = 0.99 * PROBS["gene"][0]
    #             PRFather = 0.01 * 0.01
    #             PR1Gene = PRMother + PRFather
    #         # case father have the gene only
    #         elif (people[person]["father"] in one_gene or people[person]["father"] in two_genes) and (people[person]["mother"] not in one_gene or people[person]["mother"] not in two_genes):
    #             # print(f"father with gene condition hitting")
    #             PRMother = 0.01 * 0.01
    #             PRFather = 0.99 * 0.99
    #             PR1Gene = PRMother + PRFather
    #             # print(f"probabliy of having one gene : {PR1Gene}")
    #         # both dont have the gene
    #         elif people[person]["father"] not in one_gene and people[person]["father"] not in two_genes and people[person]["mother"] not in one_gene and people[person]["mother"] not in two_genes:
    #             PRMother = 0.01 * PROBS["mutation"]
    #             PRFather = PROBS["mutation"] * PROBS["mutation"]
    #             PR1Gene = PRMother + PRFather
            
    #         if person in have_trait:
    #             probablity = PR1Gene * PROBS["trait"][1][True]
            
    #         if person not in have_trait:
    #             probablity = PR1Gene * PROBS["trait"][1][False]
            
    #         # print(f"probablity for {person} in one gene condition : {probablity}")
    #     jointProb.append(probablity)

    # # calculating the joint probability
    # # print(f"jointprobablity array:{jointProb} ")
    # product = 1
    # for val in jointProb:
    #     product *= val

    # # print(f"joint_probability: {product}")
    # return product

    geneProb = 0
    traitProb = 0
    combinedProb = 1
    # print(f"people : {people}")
    for person in people:
        mother = people[person]["mother"]
        father = people[person]["father"]

        parentProb = {mother : 0, father : 0}
        # print(f"parentProb : {parentProb}")
        # print(f"mother : {mother}")

        if mother == None and father == None:
            if person not in one_gene and person not in two_genes:
                numgene = 0
                prob =  PROBS["gene"][numgene]
            elif person in one_gene:
                numgene = 1
                prob = PROBS["gene"][numgene]
            elif person in two_genes:
                numgene = 2
                prob = PROBS["gene"][numgene]
            
            geneProb = prob 
        else:
            for parent in parentProb:
                if parent not in one_gene and parent not in two_genes:
                    parentProb[parent] = PROBS["mutation"]
                elif parent in one_gene:
                    parentProb[parent] = (1 - PROBS["mutation"]) * 0.5
                elif parent in two_genes:
                    parentProb[parent] = 1 - PROBS["mutation"]
            # print(f"parentProb after setting it up: {parentProb}")
            if person not in one_gene and person not in two_genes:
                numgene = 0
                geneProb = (1 - parentProb[mother]) * (1 - parentProb[father])
            elif person in one_gene:
                numgene = 1
                prob1 = parentProb[mother] * (1 - parentProb[father])
                prob2 = parentProb[father] * (1 - parentProb[mother])
                geneProb = prob1 + prob2
            elif person in two_genes:
                numgene = 2
                geneProb = parentProb[mother] * parentProb[father]
        
        
        if person in have_trait:
            traitProb = PROBS["trait"][numgene][True]
        else:
            traitProb = PROBS["trait"][numgene][False]
        
        combinedProb *= geneProb * traitProb

    return combinedProb



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else :
            probabilities[person]["gene"][0] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # print(f"person : {person}")
        # for key , val in probabilities[person].items():
        #     print(f"key: {key}")
        #     print(f"val : {val}")
        #     # print(f"gene's prob: {probabilities[person]["gene"][gene]}")
        #     # if key == "gene":
        #     #     for gene, probability in probabilities[person][key].items():
        #     #         total = sum(probabilities[person][key].values())
        #     #         probabilities[person][key][gene] /= total    
        #     for geneOrTrait, probability in probabilities[person][key].items():
            
        #         total = sum(probabilities[person][key].values())
        #         probabilities[person][key][geneOrTrait] /= total
        total = 0
        for val in probabilities[person]["gene"]:
            total += probabilities[person]["gene"][val]
        for val in probabilities[person]["gene"]:
            probabilities[person]["gene"][val] /= total
        
        total = 0
        for geneNum in probabilities[person]["trait"]:
            total += probabilities[person]["trait"][geneNum]
        for geneNum in probabilities[person]["trait"]:
            probabilities[person]["trait"][geneNum] /= total

if __name__ == "__main__":
    main()
    # people = {
    #     'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
    #     'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
    #     'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
    # }

    # joint_probability(people, {"Harry"}, {"James"}, {"James"})

    # normalization test 
    # test = {
    #     "trait" : {
    #         True : 0.1,
    #         False : 0.3
    #     }
    # }

    # if test["trait"][True] + test["trait"][False] != 1:
    #     factor = 1
    #     if test["trait"][True] > test["trait"][False]:
    #         factor = test["trait"][True]/test["trait"][False]
    #         x = test["trait"][True]
    #         y = test["trait"][False]
    #     elif test["trait"][True] < test["trait"][False]:
    #         factor = test["trait"][False]/test["trait"][True]
    #         x = test["trait"][False]
    #         y = test["trait"][True]

    #     changeFactor = 0.01
    #     while x + y != 1.00:
            
    #         x = round(x + changeFactor, 4)
    #         y = round(x * factor, 4)
    #         print(f"x : {x} y : {y}")
    #         if x > 1.00:
    #             changeFactor = -changeFactor



    #     print(f"x : {x} y : {y}")  

    # Test for normalizing
    # probabilites = {
    #     "Harry" : {
    #         "gene" : {
    #             0 : 0.10,
    #             1: 0.3,
    #             2 : 0.5

    #         }
    #     }
    # }

    # normalize(probabilites)



