# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 16:17:40 2022

@author: HP
"""
import os
import pandas as pd
# THINK 
"""
istanbuldan çıkan bir arabaya bindin, ağrıya gittin 15 saat sürdü, ondan sonra tekrar başka bir şehire 
gitmek istiyorsun, ama zaten 15 saat bu arabada olduğun için başka bir arabaya binemeyeceksin, ve 
biniş zamanı geçmiş arabalara da binemeyeceksin. Buna uygun bir şekilde modeli tasarla.
Ayrıca bu demek oluyor ki, ileriki tarihli datayı da elinde tutman gerekli, ya da route çizdikçe data toplayacaksın.
"""

dir_path = os.path.dirname(os.path.realpath(__file__))
input_directory = dir_path + "\\data"
data = pd.read_excel(input_directory+"\\ALL_journey"+".xlsx")

vertices = set( list(data["destination"]) + list(data["from"]))


# A class to represent the adjacency list of the node
 
 
class AdjNode:
    def __init__(self, data):
        self.vertex = data
        self.next = None
 
class Edge:
    def __init__(self,start,destination):
        self.start = start
        self.destination = destination
    def add_cost_information(self,price, distance):
        self.price = price
        self.distance = distance
        
# A class to represent a graph. A graph
# is the list of the adjacency lists.
# Size of the array will be the no. of the
# vertices "V"
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None] * self.V
 
    # Function to add an edge in an undirected graph
    def add_edge(self, src, dest):
        # Adding the node to the source node
        node = AdjNode(dest)
        node.next = self.graph[src]
        self.graph[src] = node
 
        # Adding the source node to the destination as
        # it is the undirected graph
        node = AdjNode(src)
        node.next = self.graph[dest]
        self.graph[dest] = node
 
    # Function to print the graph
    def print_graph(self):
        for i in range(self.V):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.graph[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")
 
 
# Driver program to the above graph class
if __name__ == "__main__":
    V = 5
    graph = Graph(V)
    graph.add_edge(0, 1)
    graph.add_edge(0, 4)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
 
    graph.print_graph()
