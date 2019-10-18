
# Author: Timothy Johnson
# This program creates an SMT formula to determine a knight's tour on a chessboard
# of the given size with the minimum number of turns.

# To run this, you'll need to install both pysmt and a compatible solver. I've used z3.
# - pip install pysmt
# - pip install z3-solver
# Note: The z3 Python bindings may work only with Python 2.

from pysmt.shortcuts import Symbol, And, Or, Not, Implies, LT, LE, Equals, GT, GE, Min, Max, Plus, Minus, Times, Int, Bool
from pysmt.shortcuts import get_model, get_unsat_core
from pysmt.typing import INT


class Graph:        
    def __init__(self, size):
        self.size = size
        self.squareCount = self.size**2
        if size > 0:
            self.buildEdges()
        
    
    def subgraph(self, nodes):
        # Build subgraph for testing purposes
        subgraph = Graph(0)
        subgraph.size = -1
        subgraph.squareCount = len(nodes)
        subgraph.indexMap = {}
        subgraph.inEdgeMap = {(square, index) : [] for square in nodes for index in range(4)}
        subgraph.outEdgeMap = {(square, index) : [] for square in nodes for index in range(4)}
        subgraph.allEdges = []
        for edge in self.allEdges:
            square1, cellIndex1, square2, cellIndex2 = self.indexMap[edge]
            if square1 in nodes and square2 in nodes:
                subgraph.indexMap[edge] = self.indexMap[edge]
                subgraph.inEdgeMap[(square2, cellIndex2)].append(edge)
                subgraph.outEdgeMap[(square1, cellIndex1)].append(edge)
                subgraph.allEdges.append(edge)
        return subgraph
        
        
    def buildEdges(self):
        edgeCount = 0
        self.indexMap = {}
        self.inEdgeMap = {(square, index) : [] for square in range(self.squareCount) for index in range(4)}
        self.outEdgeMap = {(square, index) : [] for square in range(self.squareCount) for index in range(4)}
        self.allEdges = []
        directions = [(1, 2, 0), (-1, -2, 0), (-1, 2, 1), (1, -2, 1), (2, 1, 2), (-2, -1, 2), (-2, 1, 3), (2, -1, 3)]
        for square1 in range(self.squareCount):
            row1 = square1  / self.size
            column1 = square1 % self.size
            for direction in directions:
                row2 = row1 + direction[0]
                column2 = column1 + direction[1]
                cellIndex2 = direction[2]
                if row2 >= 0 and row2 < self.size and column2 >= 0 and column2 < self.size:
                    for cellIndex1 in range(4):
                        newEdge = Symbol('edge' + str(edgeCount), INT)
                        square2 = row2 * self.size + column2
                        self.indexMap[newEdge] = (square1, cellIndex1, square2, cellIndex2)
                        self.inEdgeMap[(square2, cellIndex2)].append(newEdge)
                        self.outEdgeMap[(square1, cellIndex1)].append(newEdge)
                        self.allEdges.append(newEdge)
                        edgeCount += 1
                        # print 'New edge: ', (square1, cellIndex1, square2, cellIndex2)
        
        
    def getIncomingList(self, square):
        # Combine lists of edges for all vertices in the cell
        return [edge for cellIndex in range(4) for edge in self.inEdgeMap[(square, cellIndex)]]
        
        
    def getOutgoingList(self, square):
        return [edge for cellIndex in range(4) for edge in self.outEdgeMap[(square, cellIndex)]]
            
    
    def getAllEdges(self):
        return self.allEdges
        
        
    def getTurnEdges(self):
        turnEdges = []
        for edge in self.getAllEdges():
            square1, cellIndex1, square2, cellIndex2 = self.indexMap[edge]
            if not cellIndex1 == cellIndex2:
                turnEdges.append(edge)
        return turnEdges
        
        
def findTour(graph, maxTurns, nodes=[]):
    if len(nodes) == 0:
        nodes = range(graph.squareCount)
        invNodes = range(graph.squareCount)
    else:
        invNodes = {nodes[i] : i for i in range(len(nodes))}

    #print 'Edge list:'
    #for edge in graph.getAllEdges():
    #    print graph.indexMap[edge]
        
    yVals = [Symbol('y' + str(i), INT) for i in nodes]
    size = Symbol('size', INT)
    sizeCheck = Equals(size, Int(graph.squareCount))
    
    # Set domain so the edge variables are zero or one, and the y[i]'s range from 0 to size**2 - 1
    domains = And(And([And(GE(edge, Int(0)), LE(edge, Int(1))) for edge in graph.getAllEdges()]),
                    And([And(GE(yVal, Int(0)), LT(yVal, size)) for yVal in yVals]))
    
    # Each cell is arrived at and departed from exactly once
    departures = And([Equals(Plus(graph.getOutgoingList(i)), Int(1)) for i in nodes])
    arrivals = And([Equals(Plus(graph.getIncomingList(i)), Int(1)) for i in nodes])
    
    # Each vertex in each cell is arrived at and departed from the same number of times
    cellCheck = Bool(True)
    for i in nodes:
        for cellIndex in range(4):
            inEdges = graph.inEdgeMap[(i, cellIndex)]
            outEdges = graph.outEdgeMap[(i, cellIndex)]
            if len(inEdges) > 0 and len(outEdges) > 0:
                cellCheck = And(cellCheck, Equals(Plus(inEdges), Plus(outEdges)))
            elif len(inEdges) > 0:
                cellCheck = And(cellCheck, Equals(Plus(inEdges), Int(0)))
            elif len(outEdges) > 0:
                cellCheck = And(cellCheck, Equals(Plus(outEdges), Int(0)))
          
    
    # Tour ordering
    # We choose zero as the starting point, and start our loop late so the position in our tour
    # will not have to increase when it returns to the beginning.
    ordering = Equals(yVals[nodes[0]], Int(0))
    for square2 in nodes[1:]:
        for edge in graph.getIncomingList(square2):
            square1, _, square2, _ = graph.indexMap[edge]
            ordering = And(ordering, Implies(Equals(edge, Int(1)), Equals(yVals[invNodes[square2]], Plus(yVals[invNodes[square1]], Int(1)))))
    
    # Turn count
    turnCount = LE(Plus([edge for edge in graph.getTurnEdges()]), Int(maxTurns))
    
    formula = And(sizeCheck, domains, arrivals, departures, cellCheck, ordering, turnCount)
    model = get_model(formula)
    if model:
        edgeVals = [model.get_py_value(edge) for edge in graph.getAllEdges()]
        for edge in graph.getAllEdges():
            edgeVal = model.get_py_value(edge)
            if edgeVal == 1:
                print 'Edge: ', graph.indexMap[edge]
        yVals = [model.get_py_value(yVals[i]) for i in range(len(nodes))]
        print yVals
        return yVals
    else:
        print 'No tour found!'
        return None
    

def binarySearch(size):
    # I only know how to check decision problems with pysmt, so we binary search for the best number of turns.
    graph = Graph(size)
    minTurns = 0
    maxTurns = graph.squareCount + 1
    while maxTurns - minTurns > 0:
        checkTurns = (minTurns + maxTurns) / 2
        ordering = findTour(graph, checkTurns)
        if ordering:
            print 'Tour found with ' + str(checkTurns) + ' turns.'
            maxTurns = checkTurns
        else:
            print 'No tour found with ' + str(checkTurns) + ' turns.'
            minTurns = checkTurns + 1

    ordering = findTour(graph, minTurns)
    if ordering:
        print 'Optimal tour found!'
        for i in range(size):
            for j in range(size):
                print ordering[i*size + j],
            print 
    else:
        print('There is no possible tour.')

if __name__ == '__main__':
    binarySearch(6)