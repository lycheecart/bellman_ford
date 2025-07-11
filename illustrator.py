#!/usr/bin/env python

import graphviz

class Illustrator():
    def illustrate(self, filename=""):
        graph = graphviz.Digraph(name=filename, filename=filename+".gv", format="png")
        with open(filename) as file:
            for line in file:
                eList = line.split()
                pointA = eList[0]
                pointB = eList[1]
                weight = eList[2]
                graph.edge(pointA, pointB,label=weight)
        graph.view()


def main():
    il = Illustrator()
    il.illustrate("./graph_a.txt")
    il.illustrate("./graph_b.txt")
    il.illustrate("./graph_c.txt")

if __name__ == "__main__":
    main()
