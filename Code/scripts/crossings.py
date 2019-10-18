#Made by Timothy Johnson
#code to find a lower bound on the number of crossings

# To estimate the total number of crossings, we focus on edges that begin in the first row.
# However, this means we need to keep track of compatible locations in the next two rows as well.

# Note that for two edges to cross, the columns they span must overlap.

from collections import defaultdict

cellMap = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7,
    'H': 12, 'I': 13, 'J': 14, 'K': 15, 'L': 16, 'M': 17,
    'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27,
    'S': 34, 'T': 35, 'U': 36, 'V': 37,
    'W': 45, 'X': 46, 'Y': 47,
    'Z': 56, '[': 57,
    '@': 67
}
movesX = [1, 2,  2,  1, -1, -2, -2, -1]
movesY = [2, 1, -1, -2, -2, -1,  1,  2]

def validMoves(row):
    moves = []
    for square in cellMap:
        prevMove = cellMap[square] // 10
        prevRow = movesY[prevMove] + row
        nextMove = cellMap[square] % 10
        nextRow = movesY[nextMove] + row
        # print(square, prevRow, nextRow)
        if prevRow >= 0 and nextRow >= 0:
            moves.append(square)
    return moves


def buildColumns():
    columns = []
    for a in validMoves(0):
        for b in validMoves(1):
            columns.append((a, b))
    return columns


def startMoves(startColumn, startRow):
    moves = []
    for square in cellMap:
        prevMove = cellMap[square] // 10
        prevRow = movesY[prevMove] + startRow
        prevColumn = movesX[prevMove] + startColumn
        nextMove = cellMap[square] % 10
        nextRow = movesY[nextMove] + startRow
        nextColumn = movesX[nextMove] + startColumn
        if prevRow >= 0 and prevColumn >= 0 and nextRow >= 0 and nextColumn >= 0:
            moves.append(square)
    return moves


def getStartColumns(startColumn):
    columns = []
    for a in startMoves(startColumn, 0):
        for b in startMoves(startColumn, 1):
            columns.append((a, b))
    return columns


# Check that the edges in squares1 match with squares2
def isCompatiblePair(squares1, squares2, columnDistance):
    assert len(squares1) == len(squares2)
    rowsChecked = len(squares1)
    edgeCounts = defaultdict(int)
    countEdges(squares1, edgeCounts, 0)
    countEdges(squares2, edgeCounts, columnDistance)
    for edge in edgeCounts:
        row1, column1, row2, column2 = edge
        if (row1 < rowsChecked and column1 == 0 and row2 < rowsChecked and column2 == columnDistance):
            if not edgeCounts[edge] == 2:
                return False
    return True


def countEdges(column, edgeCounts, columnIndex):
    for row in range(len(column)):
        index = column[row]
        prevMove = cellMap[index] // 10
        prevRow = movesY[prevMove] + row
        prevColumn = movesX[prevMove] + columnIndex
        nextMove = cellMap[index] % 10
        nextRow = movesY[nextMove] + row
        nextColumn = movesX[nextMove] + columnIndex

        if prevColumn < columnIndex:
            edgeCounts[(prevRow, prevColumn, row, columnIndex)] += 1
        else:
            edgeCounts[(row, columnIndex, prevRow, prevColumn)] += 1

        if nextColumn < columnIndex:
            edgeCounts[(nextRow, nextColumn, row, columnIndex)] += 1
        else:
            edgeCounts[(row, columnIndex, nextRow, nextColumn)] += 1


def countSelfCrossings(column):
    crossingCount = 0
    allMoves = getMoves(column, 0)
    for index1 in range(len(allMoves)):
        for index2 in range(index1):
            if hasCrossing(allMoves[index1], allMoves[index2]):
                crossingCount += 1
    return crossingCount


def countPairCrossings(column1, column2):
    crossingCount = 0
    allMoves1 = getMoves(column1, 0)
    allMoves2 = getMoves(column2, 1)
    for move1 in allMoves1:
        for move2 in allMoves2:
            if hasCrossing(move1, move2):
                crossingCount += 1.0 / numCounts(move1, move2)
    return crossingCount


def getMoves(column, startColumn):
    moves = []
    for index in range(len(column)):
        prevMove = cellMap[column[index]] // 10
        prevRow = movesY[prevMove] + index
        prevColumn = movesX[prevMove] + startColumn
        move1 = (index, startColumn, prevRow, prevColumn)
        moves.append(move1)

        nextMove = cellMap[column[index]] % 10
        nextRow = movesY[nextMove] + index
        nextColumn = movesX[nextMove] + startColumn
        move2 = (index, startColumn, nextRow, nextColumn)
        moves.append(move2)
    return moves


def hasCrossing(move1, move2):
    A = (move1[0], move1[1])
    B = (move1[2], move1[3])
    C = (move2[0], move2[1])
    D = (move2[2], move2[3])
    return intersect(A, B, C, D)

# https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
def ccw(A,B,C):
    return (C[0]-A[0]) * (B[1]-A[1]) > (B[0]-A[0]) * (C[1]-A[1])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def numCounts(move1, move2):
    times = 0
    A = (move1[0], move1[1])
    B = (move1[2], move1[3])
    C = (move2[0], move2[1])
    D = (move2[2], move2[3])
    columns = set()
    if A[0] <= 1:
        columns.add(A[1])
    if B[0] <= 1:
        columns.add(B[1])
    if C[0] <= 1:
        columns.add(C[1])
    if D[0] <= 1:
        columns.add(D[1])

    for column in columns:
        if (column + 1) in columns:
            times += 1
    return times


def getCrossingSequences(sequenceLength, numCrossings):
    for column1 in getStartColumns(0):
        for column2 in getStartColumns(1):
            crossingSequencesRec([column1, column2], sequenceLength, numCrossings)


def crossingSequencesRec(startSeq, sequenceLength, maxCrossings):
    currCrossings = countCrossings(startSeq)
    for column in columnPairEdges[(startSeq[-2], startSeq[-1])]:
        newSequence = [c for c in startSeq]
        newSequence.append(column)
        newCrossings = currCrossings + selfCrossings[column] + pairCrossings[(startSeq[-1], column)]
        if newCrossings < maxCrossings:
            if len(newSequence) == sequenceLength:
                print(newSequence, newCrossings)
            else:
                crossingSequencesRec(newSequence, sequenceLength, maxCrossings)

def countCrossings(sequence):
    crossingCount = 0
    for column in sequence:
        crossingCount += selfCrossings[column]

    for i in range(len(sequence) - 1):
        crossingCount += pairCrossings[sequence[i], sequence[i + 1]]
    return crossingCount


if __name__ == '__main__':
    columns = buildColumns()

    # Build pairs of columns that match at a distance of one or two apart
    columnPairs1 = {}
    columnPairs2 = {}
    for column1 in columns:
        columnPairs1[column1] = set()
        columnPairs2[column1] = set()
        for column2 in columns:
            if (isCompatiblePair(column1, column2, 1)):
                columnPairs1[column1].add(column2)
            if (isCompatiblePair(column1, column2, 2)):
                columnPairs2[column1].add(column2)

    columnPairEdges = {}
    for column1 in columns:
        for column2 in columnPairs1[column1]:
            columnPairEdges[(column1, column2)] = []
            for column3 in columnPairs1[column2]:
                if column3 in columnPairs2[column1]:
                    columnPairEdges[(column1, column2)].append(column3)

    selfCrossings = {}
    for column in columns:
        selfCrossings[column] = countSelfCrossings(column)

    pairCrossings = {}
    for column1 in columns:
        for column2 in columnPairs1[column1]:
            pairCrossings[(column1, column2)] = countPairCrossings(column1, column2)

    getCrossingSequences(15, 18)

"""
    # Dynamic programming
    maxWidth = 2
    bestWidth = [{} for i in range(maxWidth)]
    startColumns0 = getStartColumns(0)
    startColumns1 = getStartColumns(1)
    for column1 in startColumns0:
        for column2 in startColumns1:
            if column2 in columnPairs1[column1]:
                bestWidth[1][(column1, column2)] = selfCrossings[column1] + selfCrossings[column2] + pairCrossings[(column1, column2)]

    for i in range(2, maxWidth):
        for oldPair in bestWidth[i - 1]:
            column1, column2 = oldPair
            for column3 in columnPairEdges[oldPair]:
                newPair = (column2, column3)
                newCrossings = bestWidth[i - 1][oldPair] + selfCrossings[column3] + pairCrossings[newPair]
                if newPair in bestWidth[i]:
                    bestWidth[i][newPair] = min(bestWidth[i][newPair], newCrossings)
                else:
                    bestWidth[i][newPair] = newCrossings


    #print("Results:")
    #for pair in bestWidth[maxWidth - 1]:
    #    print(pair, bestWidth[maxWidth - 1][pair])
"""
