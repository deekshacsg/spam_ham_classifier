def getMetrics(fname):

    compareLabels = []

    with open(fname) as f:
        for line in f:

            spaceIndex = line.find(" ")
            predictedLabel = line[0:spaceIndex]
            filePath = line[spaceIndex + 1:]
            fileName = filePath[filePath.rfind("/") + 1:]

            if "spam" in fileName:
                trueLabel = "spam"
            else:
                trueLabel = "ham"
            compareLabels.append((predictedLabel, trueLabel))

            # confusion matrix

    performanceMatrix = [[0.0, 0.0], [0.0, 0.0]]
    for line in compareLabels:
        if (line[0] == line[1] == "ham"):
            performanceMatrix[0][0] += 1
        elif (line[0] == line[1] == "spam"):
            performanceMatrix[1][1] += 1
        elif (line[0] == "spam" and line[1] == "ham"):
            performanceMatrix[0][1] += 1
        else:
            performanceMatrix[1][0] += 1

    spamPrecision = performanceMatrix[1][1] / (performanceMatrix[1][1] + performanceMatrix[0][1])
    spamRecall = performanceMatrix[1][1] / (performanceMatrix[1][1] + performanceMatrix[1][0])
    spamFScore = 2 * spamPrecision * spamRecall / (spamPrecision + spamRecall)
    print('Performance for SPAM')
    print('Precision' + " " + str(spamPrecision))
    print('Recall   ' + " " + str(spamRecall))
    print('F Score  ' + " " + str(spamFScore) + '\n')

    hamPrecision = performanceMatrix[0][0] / (performanceMatrix[0][0] + performanceMatrix[1][0])
    hamRecall = performanceMatrix[0][0] / (performanceMatrix[0][0] + performanceMatrix[0][1])
    hamFScore = 2 * hamPrecision * hamRecall / (hamPrecision + hamRecall)
    print('Performance for HAM')
    print('Precision' + " " + str(hamPrecision))
    print('Recall   ' + " " + str(hamRecall))
    print('F Score  ' + " " + str(hamFScore))


if __name__ == "__main__":
    getMetrics("nboutput.txt")