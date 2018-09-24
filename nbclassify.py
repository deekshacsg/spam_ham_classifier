import os
import sys
import json
import math

hamDocCount = 0
spamDocCount = 0
hamWords = 0
spamWords = 0
distinctWords = 0
nbValues = {}
spamDict = {}
hamDict = {}
spamProbability = 0
hamProbability = 0


def loadValues():
    global nbValues, hamDocCount, spamDocCount, distinctWords, hamWords, spamWords
    global spamDict, hamDict, spamProbability, hamProbability
    with open("nbmodel.txt", "r") as inputFile:
        nbValues = json.load(inputFile)
        hamDocCount = nbValues["hamFileCount"]
        spamDocCount = nbValues["spamFileCount"]
        distinctWords = nbValues["uniqueWords"]
        hamWords = nbValues["hamWordsCount"]
        spamWords = nbValues["spamWordsCount"]
        spamDict = nbValues["spamDictionary"]
        hamDict = nbValues["hamDictionary"]
        spamProbability = math.log(spamDocCount / (spamDocCount + hamDocCount))
        hamProbability = math.log(hamDocCount / (spamDocCount + hamDocCount))


def calculateProbability(filename, classA, classB, numberOfWords, uniqueWords, classProbability):
    """
    Calculate the probability of a doc belonging to a given class ( ham/spam)
    :param filename:
    :param classA: ham dictionary
    :param classB: spam dictionary
    :param numberOfWords: total number of words found in all documents belonging to a given class
    :param uniqueWords: unique words found among spam and ham documents
    :param classProbability: Spam/Ham class prior
    :return: score between [0.0, 1.0] indicating the probability of the document belonging to a class
    """
    probability = 0.0
    with open(filename, "r", encoding="latin1") as f:
        for line in f:
            for word in line.split(" "):
                word = word.rstrip('\n').rstrip('\r')
                if word in classA:
                    word_count = classA[word]
                elif word in classB:
                    word_count = 0
                else:
                    word_count = -1

                if word_count != -1:
                    probability = probability + math.log((word_count + 1) / (numberOfWords + distinctWords))
        return (probability + classProbability)


def nbClassifier(rootDirectory):
    """
    For each file under the root directory, calculate it's spam and ham probability.
    Mark the doc as SPAM if P(SPAM) > P(HAM), else mark it as HAM
    :param rootDirectory:
    :return:
    """
    outputFile = open("nboutput.txt", "w", encoding="latin1")
    for root, subdirectory, files in os.walk(rootDirectory):
        for f in files:
            if f.endswith(".txt"):
                filename = os.path.join(root, f)
                classIsHam = calculateProbability(filename, hamDict, spamDict, hamWords, distinctWords, hamProbability)
                classIsSpam =calculateProbability(filename, spamDict, hamDict, spamWords, distinctWords,spamProbability)
                if (classIsHam > classIsSpam):
                    outputFile.write("ham" + " " + filename + "\n")
                else:
                    outputFile.write("spam" + " " + filename + "\n")

    outputFile.close()


if __name__ == "__main__":
    loadValues()
    nbClassifier(sys.argv[1])
