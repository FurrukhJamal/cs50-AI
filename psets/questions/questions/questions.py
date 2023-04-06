import nltk
import sys
import os
import math 
import string

# nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = {}
    for filename in os.listdir(directory):
        # print(filename)
        # bug NEED FO FIX IT 
        # if filename == "machine_learning.txt" or filename == "probability.txt":
        #     continue
        with open(os.path.join(directory, filename), encoding="utf8") as f:
            # print(f.read())
            data[filename] = f.read()
    return data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # print(f"string.punctuation : {string.punctuation}")
    # test  = nltk.corpus.stopwords.words("english")
    # print(f"ltk.corpus.stopwords.words(\"english\") : {test}")
    data = []
    for word in nltk.word_tokenize(document):
        word = word.lower()
        # print(f"word in tokenize function: {word}")
        if word.isalpha() and word not in nltk.corpus.stopwords.words("english"):
            data.append(word)
    return data


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set()
    for filename in documents:
        for word in documents[filename]:
            words.add(word)
    
    idfs = {}
    for word in words:
        numDocsWordIsIn = sum(word in documents[filename] for filename in documents)
        idf = math.log(len(documents)/numDocsWordIsIn)
        idfs[word] = idf 
    
    return idfs



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # print(f"query is : {query}")
    frequencies = {}
    for qWord in query:
        # print(f"qWord : {qWord}")
        for file in files:
            if file not in frequencies.keys():
                frequencies[file] = {}
            if qWord in files[file]:
                
                for word in files[file]:
                    if word == qWord:
                        if word not in frequencies[file]:
                            frequencies[file][word] = 1
                        else : 
                            frequencies[file][word] += 1
            else : 
                frequencies[file][qWord] = 0
                
    # print(f"frequencies : {frequencies}")
    tfidf = {}
    for filename in frequencies:
        tfidf[filename] = []
        for word in query:
            tfidf[filename].append((word, idfs[word] * frequencies[filename][word]))
    # print(f"TFIDFS : {tfidf}")

    tfidfSum = {}
    
    for filename in tfidf:
        total = 0
        for val in tfidf[filename]:
            total += val[1]
        tfidfSum[filename] = total
    
    # print(f"tfidfSum : {tfidfSum}")

    data = sorted(tfidfSum, key = tfidfSum.get , reverse = True)
    # print(f"top files to be returned : {data}")
    data = data[:n]
    return data 




def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # print(f"sentences : {sentences.keys()}")
    # test = idfs["how"]
    # print(f"idf[how] : {test}")
    wordMeasures = {}
    for sentence in sentences.keys():
        wordMeasures[sentence] = 0
        idfSum = 0
        for word in query:
            if word in sentences[sentence]:
                idfSum += idfs[word]
        wordMeasures[sentence] = idfSum
    # print(f"wordMeausres : {wordMeasures}")
    maxidf = max(wordMeasures.values())
    sortedSentencesWithIdf = dict(sorted(wordMeasures.items(), key = lambda item: item[1], reverse = True))
    # print(f"sortedSentencesWithIdf : {sortedSentencesWithIdf}\n")
    
    # checking to see if there are more than one sentences with equal maxidf
    sentencesWithMaxIdf = [] 
    for sentence in wordMeasures:
        if wordMeasures[sentence] == maxidf:
            sentencesWithMaxIdf.append(sentence)
    
    # print(f"sentencesWithMaxIdf : {sentencesWithMaxIdf} \n")

    queryTermSentences = {}
    sortedQueryTermSentences = []
    if len(sentencesWithMaxIdf) > 1:
        # distinguish bw the sentences on the basis of query term density
        
        for sentence in sentencesWithMaxIdf:
            numOfWordMatch = 0
            for word in sentences[sentence]:
                if word in query:
                    numOfWordMatch += 1
            qtd = numOfWordMatch/ len(sentences[sentence]) 
            # qtd = (numOfWordMatch)/ len(sentences[sentence]) * (1 / len(query))
            queryTermSentences[sentence] = qtd
        # print(f"queryTermSentences : {queryTermSentences} \n\n")
        sortedQueryTermSentences = sorted(queryTermSentences, key = queryTermSentences.get, reverse = True)
        # print(f"sortedQueryTermSentences : {sortedQueryTermSentences}")

    # returning the data list as a some of list for the list of sentences sorted based on query term
    # density if there was a tie, and the reamining list of the list sorted by idfs. If there was not a tie 
    # then automatically sortedQueryTermSentences would be empty and data would only contain sentences sorted 
    # via idfs
    data = sortedQueryTermSentences + list(sortedSentencesWithIdf.keys())[len(sortedQueryTermSentences) : n]
    return data[:n] 



if __name__ == "__main__":
    main()
