import os
import random
import re
import sys
from collections import deque
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages    
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prb = (1 - damping_factor)/ len(corpus.keys())
    
    if len(corpus[page]) == 0:
        
        data = {}
        for key in corpus.keys():
            # data[key] = round(prb, 4)
            data[key] = 1/len(corpus.keys())
        return data
    else:
        prbFromCurrentPage = (1 - damping_factor)/ len(corpus.keys()) + (damping_factor * (1/ len(corpus[page])))
        data = {}
        for key in corpus.keys():
            if key == page:
                # data[key] = round((1 - damping_factor)/ len(corpus.keys()), 4)
                data[key] = (1 - damping_factor)/ len(corpus.keys())
                # data[key] = prbFromCurrentPage
            elif key in corpus[page]:
                # data[key] = round(prbFromCurrentPage, 4)
                data[key] = prbFromCurrentPage
            else:
                # data[key] = round(prb, 4)
                data[key] = prb
        # for key in corpus[page]:
        #     data
        return data  


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    prbFirst = (1 - damping_factor)/len(corpus.keys())
    # insert equal probability for first page
    samePrb = {}
    for key in range(len(corpus.keys())):
        samePrb[key] = prbFirst
    data = {}
    nextPage = random.choices(list(corpus.keys()),  list(samePrb.values()), k = 1)[0]
    # print(f"first nextPage is: {nextPage}")
    # print(f"transition_model : {transition_model(corpus, nextPage, damping_factor)}")
    data[nextPage] = 1

    for i in range(n -1):
        # print(f"in loop list(corpus[nextPage]): {list(corpus[nextPage])} \n in loop list(transition_model) : {list(transition_model(corpus, nextPage, damping_factor).values())}")
        nextPage = random.choices(list(corpus.keys()), list(transition_model(corpus, nextPage, damping_factor).values()), k = 1)[0]
        # print(f"next page in loop: {nextPage}")
        try:
            data[nextPage] += 1
        except KeyError:
            data[nextPage] = 1

    #   calculating the probabilty for each page by dividing their number counts by sample size
    for page, count in data.items():
        data[page] = count/n 
    
    return data


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PR = {}
    N = len(corpus.keys())
    # initialzing the probablities
    for webPage in corpus.keys():
        #             [previous, latest]
        # PR[webPage] = [0, 1/len(corpus)]
        PR[webPage] = deque([0, 1/len(corpus)], 2)
    
    possibleVisits = PR.keys()
    # print(f"values in dict: {list(PR.values())}")
    # print(f"possibleVisits : {list(possibleVisits)}")
    
    weights = []
    for val in PR.values():
        weights.append(val[1])
    # print(f"weights : {weights}")
    counter = 0
    # minDifference = 1
    minDifference = []
    # while max(minDifference) > 0.001:
    maxDifference = 1
    while maxDifference > 0.0001: 
        Mindifference = 2
        minDifference = []
        for page in PR.keys():
            # print(f"page : {page}")
            pagesLinkedByPage = []
            for web in PR.keys():
                # print(f"corpus[{web}] : {corpus[web]}")
                if page in corpus[web] and page != web:
                    pagesLinkedByPage.append(web)
                
            # print(f"{page} linked by {pagesLinkedByPage}")
            
            sum = 0
            for link in pagesLinkedByPage:
                sum += PR[link][1]/len(corpus[link])
            
            newPR = (1 - damping_factor)/len(corpus) + (damping_factor * sum)
            # print(f"newPR: {newPR}")
            PR[page].append(newPR)
            difference = abs(PR[page][1] - PR[page][0] )
            # if abs(PR[page][1] - PR[page][0]) < difference:
            #     print(f"difference changed for page: {page}")
            # print(f"minDIfference before condition : {minDifference}")
            # if difference < minDifference and PR[page][1] != PR[page][0] :
            #     minDifference = difference
                # print(f"new difference is {difference}")
                
            minDifference.append(difference)
        
            # print(f"minDifference array : {minDifference}")
            # print(f"PR: {PR}\n")
            # print(f"difference : {difference}\n\n")

        maxDifference = max(minDifference)   

    # print(f"PR at the end:{PR}")
    data = {}
    for key , val in PR.items():
        data[key] = round(val[1],4)
        # data[key] = val[1]
    
    # print(f"returned value: {data}")
    return data


if __name__ == "__main__":
    main()
    # test = {}
    # # test["1.html"] = set(["2.html", "3.html"])
    # # test["2.html"] = set(["3.html"])
    # # test["3.html"] = set (["2.html"])

    # # print(transition_model(test, "2.html", 0.85))
    # # print(sample_pagerank(test, 0.85, 1000))
    # # iterate_pagerank(test, 0.85)


