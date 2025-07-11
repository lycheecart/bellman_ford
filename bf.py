#!/usr/bin/env python

INF = pow(10,20)

class Edge():
    def __init__(self, pointA="", pointB="",weight=""):
        self.pointA=pointA
        self.pointB=pointB
        self.weight=int(weight)

    def hasSameNodes(self, edge):
        return self.pointA == edge.pointA and self.pointB == edge.pointB

class BellmanForder():
    def __init__(self):
        self.edges = []
        self.nodes = set()
        self.costs = {}
        self.paths = {} #nodeLabel: list #i have thrown the specific paths in as an 'extra'
        self.origin = "0" #TODO user sets origin

    def loadGraph(self, filename):
        with open(filename) as file:
            for line in file:
                eList = line.split()
                pointA = eList[0]
                pointB = eList[1]
                weight = eList[2]
                self.edges.append(Edge(pointA=pointA, pointB=pointB, weight=weight))

    def updateEdge(self, edge):
        self.nodes.add(edge.pointA)
        self.nodes.add(edge.pointB)

        for e in self.edges:
            if e.hasSameNodes(edge):
                e.weight = edge.weight
                return
        self.edges.append(edge)

    def initSolver(self):
        for edge in self.edges:
            self.nodes.add(edge.pointA)
            self.nodes.add(edge.pointB)
        for node in self.nodes:
            if node == self.origin:
                self.costs[node] = 0
                self.paths[node] = [node]
            else:
                self.costs[node] = INF
                self.paths[node] = []

    def solve(self):
        #mostly stolen from wikipedia
        predecessors = {} #this is for negative cycle detection
        for i in range (len(self.nodes)-1):
            for edge in self.edges:
                if self.costs[edge.pointA] + edge.weight < self.costs[edge.pointB]:
                    self.costs[edge.pointB] = self.costs[edge.pointA] + edge.weight
                    self.paths[edge.pointB] = self.paths[edge.pointA] + [edge.pointB]
                    predecessors[edge.pointB] = edge.pointA 
        #negative cyc detection
        visited = {}
        for n in self.nodes:
            visited[n] = False
        for edge in self.edges:
            if self.costs[edge.pointA] + edge.weight < self.costs[edge.pointB]:
                predecessors[edge.pointB] = edge.pointA
                visited[edge.pointB] = True
                vn = edge.pointA
                while visited[vn] == False:
                    visited[vn] = True
                    vn = predecessors[vn]
                cycle = [vn]
                pvn = predecessors[vn]
                while pvn != vn:
                    cycle += [pvn]
                    pvn = predecessors[pvn]
                exit("negative cycle " + str(cycle))


    def displayCosts(self):
        for ck in sorted(self.costs.keys()):
            if self.costs[ck] == INF:
                costStr = "∞"
            else:
                costStr = str(self.costs[ck])
            view = ck + ": " + costStr 
            print(view, end=" ")
            print(self.paths[ck])


    def deleteEdge(self, pointA, pointB):
        self.edges = list(filter(lambda edge: edge.pointA != pointA and edge.pointB != pointB, self.edges))
        #should initSolver again

def main():
    bfer = BellmanForder()
    bfer.loadGraph("./dg.txt")
    bfer.initSolver()
    bfer.solve()
    bfer.displayCosts()

    while True:
        new_edge_str = input(">new edge: point_a point_b weight\n>")
        new_edge_list = new_edge_str.split()
        edge = Edge(pointA=new_edge_list[0], pointB=new_edge_list[1], weight=int(new_edge_list[2])) #FIXME no error checking
        bfer.updateEdge(edge)
        bfer.initSolver()
        bfer.solve()
        bfer.displayCosts()

if __name__ == "__main__":
    main()
