from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from collections import *
import operator


class OrderedCounter(Counter, OrderedDict):
    pass


def createExamples():
    numberArrayExample = open('numArEx.txt', 'a')
    numbersWeHave = range(0,10)
    versionsWeHave = range(1,10)

    for eachNum in numbersWeHave:
        for eachVer in versionsWeHave:
            imgFilePath = 'numbers/' + str(eachNum) + '.' + str(eachVer) + '.png'
            exampleImage = Image.open(imgFilePath)
            exampleImageArray = np.array(exampleImage)
            exampleImageArrayList = str(exampleImageArray.tolist())

            lineToWrite = str(eachNum) + '::' + exampleImageArrayList + '\n'
            numberArrayExample.write(lineToWrite)


def threshold(imageArray):
    balanceArray = []
    newArray = imageArray

    for eachRow in imageArray:
        for eachPixel in eachRow:
            avgNum = reduce(lambda x, y: x + y, eachPixel[:3])/len(eachPixel[:3])
            balanceArray.append(avgNum)

    balance = reduce(lambda x, y: x + y, balanceArray)/len(balanceArray)

    for eachRow in newArray:
        for eachPixel in eachRow:
            if reduce(lambda x, y: x + y, eachPixel[:3])/len(eachPixel[:3]) > balance:
                eachPixel[0] = 255
                eachPixel[1] = 255
                eachPixel[2] = 255
                eachPixel[3] = 255

            else:
                eachPixel[0] = 0
                eachPixel[1] = 0
                eachPixel[2] = 0
                eachPixel[3] = 255

    return newArray


def whatNumIsThis(filePath):
    matchedArray = []
    loadExamples = open('numArEx.txt', 'r').read()
    loadExamples = loadExamples.split('\n')

    image = Image.open(filePath)
    imageArray = threshold(np.array(image))
    imageArrayList = imageArray.tolist()

    inQuestion = str(imageArrayList)

    for eachExample in loadExamples:
        if len(eachExample) > 3:
            splitExample = eachExample.split('::')
            currentNumber = splitExample[0]
            currentArray = splitExample[1]

            eachPixelInExample = currentArray.split('],')

            eachPixelInQuestion = inQuestion.split('],')

            x = 0

            while x < len(eachPixelInExample):
                if eachPixelInExample[x] == eachPixelInQuestion[x]:
                    matchedArray.append(int(currentNumber))

                x += 1

    x = Counter(matchedArray)
    print max(x.iteritems(), key=operator.itemgetter(1))[0]

    graphX = []
    graphY = []

    for eachThing in x:
        graphX.append(eachThing)
        graphY.append(x[eachThing])

    fig = plt.figure()
    ax1 = plt.subplot2grid((4,4), (0,0), rowspan=1, colspan=4)
    ax2 = plt.subplot2grid((4,4), (1,0), rowspan=3, colspan=4)

    ax1.imshow(imageArray)
    ax2.bar(graphX, graphY, align='center')
    plt.ylim(350)

    xloc = plt.MaxNLocator(12)

    ax2.xaxis.set_major_locator(xloc)

    plt.show()


whatNumIsThis('test.png')
