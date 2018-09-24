import os
import sys
import json
from collections import defaultdict

spamDocCount  = 0
hamDocCount = 0
hamWords = 0
spamWords = 0
distinctWords = 0
hamDictionary = defaultdict(int)
spamDictionary = defaultdict(int)
jsonObject = {}


if len(sys.argv) != 2:
    print("Error: Please pass the Directory path as an arg")
    exit(1)

if not sys.argv[1]:
    print("Error: Null argument passed \n")
    exit(1)


def traverseFiles(rootDirectory):
    global spamDocCount, hamDocCount
    for root, subdirectory, files in os.walk(rootDirectory):
        if os.path.basename(root) == "ham":
            for f in files:
                if f.endswith(".txt"):
                    hamDocCount += 1
                    filename = os.path.join(root, f)
                    tokenCounts(filename)


        if os.path.basename(root) == "spam":
            for f in files:
                if f.endswith(".txt"):
                    spamDocCount += 1
                    filename = os.path.join(root, f)
                    tokenCounts(filename, ham=False)


def tokenCounts(filename, ham = True):
    """
    Count the total number of tokens present in the given spam/ham document

    :param filename: path to the spam/ham document
    :param ham: bool indicating whether the file is ham or spam
    :return: None
    """
    global hamDictionary, hamWords, spamDictionary, spamWords
    with open(filename, "r", encoding = "latin1") as f:

        if ham:
            for line in f:
                for word in line.split(" "):
                    word = word.rstrip('\n').rstrip('\r')
                    hamWords = hamWords + 1
                    hamDictionary[word]  += 1
        else:
            for line in f:
                for word in line.split(" "):
                    word = word.rstrip('\n').rstrip('\r')
                    spamWords = spamWords + 1
                    spamDictionary[word] += 1


def countDistinctWords():
    """

    :return: all the unique words found among spam and ham documents
    """
    global distinctWords
    ham = hamDictionary.keys()
    spam = spamDictionary.keys()
    vocab = set(ham + spam)
    distinctWords = len(vocab)


def createJasonObject():
    global jsonObject
    jsonObject["spamFileCount"] = spamDocCount
    jsonObject["hamFileCount"] = hamDocCount
    jsonObject["uniqueWords"] = distinctWords
    jsonObject["spamWordsCount"] = spamWords
    jsonObject["hamWordsCount"] = hamWords
    jsonObject["spamDictionary"] = spamDictionary
    jsonObject["hamDictionary"] = hamDictionary

if __name__ == "__main__":
    traverseFiles(sys.argv[1])
    countDistinctWords()
    createJasonObject()

    str1 =  json.dumps(jsonObject, indent = 4, sort_keys = True, ensure_ascii = False)
    with open ("nbmodel.txt", "w") as output:
        output.write(str1)
